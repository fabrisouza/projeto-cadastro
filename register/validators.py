import re

from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _


def DV_maker(v):
    if v >= 2:
        return 11 - v
    return 0


def equalsNumbers(value):
    str_value = str(value)
    first_number = str_value[0]

    for i in str_value:
        if i != first_number:
            return False


def validate_CPF(value):

    error_messages = {
        "invalid": _("Número de CPF inválido."),
        "digits_only": _("O campo requer apenas números."),
        "max_digits": _("O campo requer exatamente 11 dígitos."),
    }

    if value in EMPTY_VALUES:
        return u""
    if not value.isdigit():
        value = re.sub("[-\.]", "", value)
    orig_value = value[:]
    try:
        int(value)
    except ValueError:
        raise ValidationError(error_messages["digits_only"])

    if len(value) != 11:
        raise ValidationError(error_messages["max_digits"])

    elif equalsNumbers(value):
        raise ValidationError(error_messages["invalid"])

    orig_dv = value[-2:]

    new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(range(10, 1, -1))])
    new_1dv = DV_maker(new_1dv % 11)
    value = value[:-2] + str(new_1dv) + value[-1]
    new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(range(11, 1, -1))])
    new_2dv = DV_maker(new_2dv % 11)
    value = value[:-1] + str(new_2dv)
    if value[-2:] != orig_dv:
        raise ValidationError(error_messages["invalid"])

    return orig_value
