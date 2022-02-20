from django import template
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.filter(name='toman_format')
def toman_format(value):
    value = str(value)
    length = len(value)
    if length > 9:
        if {value[-1], value[-2], value[-3], value[-4], value[-5], value[-6], value[-7], value[-8], value[-9]} == {str(0)}:
            return f'{value[:-9]} {_("MilliardToman")}'
        elif {value[-1], value[-2], value[-3], value[-4], value[-5], value[-6]} == {str(0)}:
            return f'{value[:-6]} {_("MilliardToman")}'
        else:
            return f'{value} {_("Toman")}'
    elif 9 >= length > 6:
        if {value[-1], value[-2], value[-3], value[-4], value[-5], value[-6]} == {str(0)}:
            return f'{value[:-6]} {_("MillionToman")}'
        elif {value[-1], value[-2], value[-3]} == {str(0)}:
            return f'{value[:-3]} {_("MillionToman")}'
        else:
            return f'{value} {_("Toman")}'
    elif 6 >= length > 3 and value[-1] == str(0) and value[-2] == str(0) and value[-3] == str(0):
        return f'{value[:-3]} {_("HezarToman")}'
    else:
        return f'{value} {_("Toman")}'
