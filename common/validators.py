# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.validators import ValidationError, RegexValidator, MinValueValidator


def zero_validator(value):
    if value <= 0:
        raise ValidationError("Debe especificar un valor estrictamente positivo.")


positive_validator = MinValueValidator(0)

code_validator = RegexValidator(r"^[\w-]+$", "El código solo puede tener letras o números.")
