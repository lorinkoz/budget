# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ldap.functions import initialize as ldap_init

from .models import User

SERVER_UHO = 'ldap://10.26.0.39:389'
SERVER_CSM = 'ldap://10.26.32.5:389'

DOMAINS = {
    'fh.uho.edu.cu': SERVER_CSM,
    'facinf.uho.edu.cu': SERVER_UHO,
    'facing.uho.edu.cu': SERVER_UHO,
    'facii.uho.edu.cu': SERVER_UHO,
    'ict.uho.edu.cu': SERVER_UHO,
    'vrea.uho.edu.cu': SERVER_UHO,
    'vru.uho.edu.cu': SERVER_UHO,
}


class OpenLdapUHOBackend():

    def get_user(self, id):
        return User.objects.filter(pk=id).first()

    def authenticate(self, username=None, password=None):
        # We get the user from the database
        user = User.objects.filter(email=username).first()
        # If user is not in database, we block authentication
        if not user:
            return None
        # At this point, we have a user in database and we need to verify LDAP
        # First, split uid and domain from email
        if '@' in username:
            uid, domain = username.split('@')
        else:
            uid = username
            domain = ''
        # Get the respective server
        ldap_server = DOMAINS.get(domain, SERVER_UHO)
        if not ldap_server:
            return None
        # Initialize the LDAP handler
        ldapc = ldap_init(ldap_server)
        # We first bind anonymously to get the user's data
        try:
            r = ldapc.bind('', '')
            r = ldapc.search('dc=uho,dc=edu,dc=cu', 2, 'uid=%s' % uid, [b'givenName', b'sn', b'mail'])
            raw_data = ldapc.result(r)
            ldap_dn = raw_data[1][0][0]
            data = raw_data[1][0][1]
        except:
            return None
        # We now try to bind with credentials
        try:
            r = ldapc.bind(ldap_dn, password)
            ldapc.result(r)
            # We unbind the handler
            ldapc.unbind()
        except:
            return None
        # At this point, we have successfully checked that the user can bind to LDAP
        ldap_first_name = data.get('givenName', ['']).pop().strip().decode('utf-8')
        ldap_last_name = data.get('sn', ['']).pop().strip().decode('utf-8')
        ldap_mail = data.get('mail', ['']).pop().strip()
        # If email does not match, we block authentication
        if '@' in username and username != ldap_mail:
            return None
        # At this point authentication is successful
        # We update the user instance with the provided data
        user.display_name = ' '.join([ldap_first_name, ldap_last_name]).strip()
        user.set_password(password)
        user.save()
        # And we return the user instance, finally
        return user
