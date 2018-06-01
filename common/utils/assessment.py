# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q, Sum

from apps.core.models import Area, Element, Destination
from apps.control.models import Record, Plan, Funding


class RowInfo:

    def __init__(self, name, plan, bank, book, **kwargs):
        self.name = name
        self.plan = plan
        self.bank = bank
        self.book = book
        self.extra = kwargs
        self._calculate_values()

    def _calculate_values(self):
        if self.plan:
            self.bank_percent = abs(self.bank * 100 / self.plan)
            self.book_percent = abs(self.book * 100 / self.plan)
        else:
            self.bank_percent = 101 if self.bank else 0
            self.book_percent = 101 if self.book else 0
        self.available = self.plan - self.book
        self.available_bank = self.plan - self.bank

    def expand(self, row_info):
        self.plan += row_info.plan
        self.bank += row_info.bank
        self.book += row_info.book
        self._calculate_values()


def _month_filters(year, month, specific):
    month = int(month)
    month_filter = Q(date__month=month)
    if not specific:
        for i in range(1, month):
            month_filter |= Q(date__month=month-i)
    month_filter = Q(date__year=year, plan=year)&(month_filter)
    # If December and not specific, add any other records out of the year's scope
    if month == 12 and not specific:
        month_filter = Q(plan=year)
    return month_filter


def assess_records(records):
    positive = records.filter(concept__positive=True).aggregate(sum=Sum('amount'))['sum'] or 0
    negative = records.filter(concept__positive=False).aggregate(sum=Sum('amount'))['sum'] or 0
    return positive - negative


def area_plan_grid(area, year, width):
    year_range = range(year-width, year+1)
    bundle = Plan.objects.filter(destination__area=area, year__in=year_range).values('destination', 'year').annotate(sum=Sum('amount'))
    pregrid = {}
    for destination in area.destinations.all():
        matrix = []
        for y in year_range:
            matrix.append([0, 0, 0])
        pregrid[destination.pk] = matrix
    for item in bundle:
        pregrid[item['destination']][item['year']-year-1][0] += item['sum']
    bundle = Record.objects.filter(destination__area=area, plan__in=year_range).exclude(status=False)\
                .values('destination', 'status', 'concept__positive', 'plan').annotate(sum=Sum('amount'))
    for item in bundle:
        sign = 1 if item['concept__positive'] else -1
        amount = sign * -item['sum']
        pregrid[item['destination']][item['plan']-year-1][2] += amount
        if item['status']:
            pregrid[item['destination']][item['plan']-year-1][1] += amount
    grid = []
    ttl = {
        'destination': 'Total',
        'data': [],
    }
    for y in year_range:
        ttl['data'].append(RowInfo('', 0, 0, 0))
    for destination in area.destinations.all():
        data = {
            'destination': destination,
            'data': [],
        }
        for i in range(len(pregrid[destination.pk])):
            row_info = RowInfo('', *pregrid[destination.pk][i])
            data['data'].append(row_info)
            ttl['data'][i].expand(row_info)
        grid.append(data)
    grid.append(ttl)
    return grid


def assess_area(area, year, month, specific):
    data = {}
    month_filters = _month_filters(year, month, specific)
    for destination in area.destinations.filter(plans__year=year).annotate(plan=Sum('plans__amount')):
        data[destination.pk] = [0, 0, 0]
        data[destination.pk][0] = destination.plan
    bundle = Record.objects.filter(destination__area=area).exclude(status=False).filter(month_filters) \
                .values('destination','status','concept__positive') \
                .annotate(sum=Sum('amount'))
    for item in bundle:
        sign = 1 if item['concept__positive'] else -1
        amount = sign * -item['sum']
        if item['destination'] not in data:
            data[item['destination']] = [0, 0, 0]
        data[item['destination']][2] += amount
        if item['status']:
            data[item['destination']][1] += amount
    results = []
    for destination in area.destinations.filter(pk__in=data):
        results.append(RowInfo(destination, *data[destination.pk]))
    ttl_plan = 0
    ttl_bank = 0
    ttl_book = 0
    for item in results:
        ttl_plan += item.plan
        ttl_bank += item.bank
        ttl_book += item.book
    results.append(RowInfo('Total', ttl_plan, ttl_bank, ttl_book))
    return results


def assess_areas(year, month, specific):
    data = {}
    month_filters = _month_filters(year, month, specific)
    for area in Area.objects.filter(destinations__plans__year=year).annotate(plan=Sum('destinations__plans__amount')):
        data[area.pk] = [0, 0, 0]
        data[area.pk][0] = area.plan
    bundle = Record.objects.exclude(status=False).filter(month_filters) \
                .values('destination__area', 'status', 'concept__positive') \
                .annotate(sum=Sum('amount'))
    for item in bundle:
        sign = 1 if item['concept__positive'] else -1
        amount = sign * -item['sum']
        if item['destination__area'] not in data:
            data[item['destination__area']] = [0, 0, 0]
        data[item['destination__area']][2] += amount
        if item['status']:
            data[item['destination__area']][1] += amount
    results = []
    for area in Area.objects.filter(pk__in=data):
        extra = {'slug': area.slug}
        results.append(RowInfo(area, *data[area.pk], **extra))
    ttl_plan = 0
    ttl_bank = 0
    ttl_book = 0
    for item in results:
        ttl_plan += item.plan
        ttl_bank += item.bank
        ttl_book += item.book
    results.append(RowInfo('Total', ttl_plan, ttl_bank, ttl_book))
    return results


def _get_elements_tree():
    tree = {}
    roots = []
    queryset = Element.objects.select_related('parent')
    for element in queryset:
        tree[element.pk] = {'parent':element.parent.pk if element.parent else None, 'children':[], 'scope':[]}
    for element in queryset:
        if element.parent:
            tree[element.parent.pk]['children'].append(element.pk)
        else:
            roots.append(element.pk)
    def _populate_scope(node):
        scope = [node]
        for child in tree[node]['children']:
            scope += _populate_scope(child)
        tree[node]['scope'] = scope
        return scope
    for root in roots:
        _populate_scope(root)
    return tree


def assess_element(element, year, month, specific):
    data = {}
    month_filters = _month_filters(year, month, specific)
    tree = _get_elements_tree()
    for area in Area.objects.filter(destinations__plans__year=year).all():
        data[area.pk] = [0, 0, 0]
        data[area.pk][0] = Plan.objects.filter(year=year, destination__area=area, destination__element__in=tree[element.pk]['scope'])\
            .aggregate(plan=Sum('amount')).get('plan', 0) or 0
    bundle = Record.objects.exclude(status=False).filter(destination__element__in=tree[element.pk]['scope']).filter(month_filters)\
                .values('destination__area', 'status', 'concept__positive') \
                .annotate(sum=Sum('amount'))
    for item in bundle:
        sign = 1 if item['concept__positive'] else -1
        amount = sign * -item['sum']
        if item['destination__area'] not in data:
            data[item['destination__area']] = [0, 0, 0]
        data[item['destination__area']][2] += amount
        if item['status']:
            data[item['destination__area']][1] += amount
    results = []
    for area in Area.objects.filter(pk__in=data):
        extra = {'slug': area.slug}
        results.append(RowInfo(area, *data[area.pk], **extra))
    ttl_plan = 0
    ttl_bank = 0
    ttl_book = 0
    for item in results:
        ttl_plan += item.plan
        ttl_bank += item.bank
        ttl_book += item.book
    results.append(RowInfo('Total', ttl_plan, ttl_bank, ttl_book))
    return results


def assess_elements(year, month, specific):
    month_filters = _month_filters(year, month, specific)
    tree = _get_elements_tree()
    elements = {}
    bundle = Plan.objects.filter(year=year).values('destination__element').annotate(sum=Sum('amount'))
    for item in bundle:
        if item['destination__element'] not in elements:
            elements[item['destination__element']] = [0, 0, 0]
        elements[item['destination__element']][0] += item['sum']
    bundle = Record.objects.filter(plan=year).exclude(status=False).filter(month_filters) \
                .values('destination__element', 'status', 'concept__positive').annotate(sum=Sum('amount'))
    for item in bundle:
        if item['destination__element'] not in elements:
            elements[item['destination__element']] = [0, 0, 0]
        sign = 1 if item['concept__positive'] else -1
        amount = sign * -item['sum']
        elements[item['destination__element']][2] += amount
        if item['status']:
            elements[item['destination__element']][1] += amount
    stack = []
    for node, data in tree.items():
        if data['parent'] is None:
            stack.append(node)
    for s in stack:
        stack += tree[s]['children']
    ttl_plan = 0
    ttl_bank = 0
    ttl_book = 0
    while len(stack):
        i = stack.pop()
        parent = tree[i]['parent']
        if not i in elements:
            elements[i] = [0, 0, 0]
        if parent is None:
            ttl_plan += elements[i][0]
            ttl_bank += elements[i][1]
            ttl_book += elements[i][2]
        else:
            if not parent in elements:
                elements[parent] = [0, 0, 0]
            elements[parent][0] += elements[i][0]
            elements[parent][1] += elements[i][1]
            elements[parent][2] += elements[i][2]
    results = []
    for element in Element.objects.filter(pk__in=elements).select_related('parent'):
        row_info = RowInfo(element, *elements[element.pk], **{'code': element.code})
        results.append(row_info)
    results.append(RowInfo('Total', ttl_plan, ttl_bank, ttl_book))
    return results


def assess_availability(target_year=None, currency=None):
    tree = _get_elements_tree()
    elements = {}
    extra = {}
    if currency:
        extra['currency'] = currency
    for element in Element.objects.filter(parent=None):
        elements[element.pk] = [0, 0, 0]
        funding = Funding.objects.filter(element=element, **extra)
        if target_year:
            funding = funding.filter(date__year=target_year)
        funding = funding.aggregate(sum=Sum('amount'))['sum'] or 0
        elements[element.pk][0] = funding
        records = Record.objects.filter(destination__element__pk__in=tree[element.pk]['scope'], **extra).exclude(status=False)
        if target_year:
            records = records.filter(date__year=target_year)
        bundle =  records.values('status','concept__positive').annotate(sum=Sum('amount'))
        for item in bundle:
            sign = 1 if item['concept__positive'] else -1
            amount = sign * -item['sum']
            elements[element.pk][2] += amount
            if item['status']: elements[element.pk][1] += amount
    results = []
    for element in Element.objects.filter(parent=None):
        results.append(RowInfo(element, *elements[element.pk]))
    ttl_plan = 0
    ttl_bank = 0
    ttl_book = 0
    for item in results:
        ttl_plan += item.plan
        ttl_bank += item.bank
        ttl_book += item.book
    results.append(RowInfo('Total', ttl_plan, ttl_bank, ttl_book))
    return results


def assess_overdrawns(year):
    data = {}
    for destination in Destination.objects.filter(status=True, plans__year=year).annotate(plan=Sum('plans__amount')):
        data[destination.pk] = [0, 0, 0]
        data[destination.pk][0] = destination.plan
    bundle = Record.objects.filter(plan=year).exclude(status=False) \
                .values('destination','status','concept__positive') \
                .annotate(sum=Sum('amount'))
    for item in bundle:
        if item['destination'] not in data:
            data[item['destination']] = [0, 0, 0]
        sign = 1 if item['concept__positive'] else -1
        amount = sign * -item['sum']
        data[item['destination']][2] += amount
        if item['status']:
            data[item['destination']][1] += amount
    results = []
    ttl_plan = 0
    ttl_bank = 0
    ttl_book = 0
    for destination in Destination.objects.filter(status=True, plans__year=year).select_related('area'):
        extra = {'area': destination.area }
        row_info = RowInfo(destination, *data[destination.pk], **extra)
        if row_info.available < 0:
            ttl_plan += data[destination.pk][0]
            ttl_bank += data[destination.pk][1]
            ttl_book += data[destination.pk][2]
            results.append(row_info)
    results.append(RowInfo('Total', ttl_plan, ttl_bank, ttl_book))
    return results
