from django import template

register = template.Library()


@register.filter
def dict_value(dictionary, key):
    return dictionary.get(key)
