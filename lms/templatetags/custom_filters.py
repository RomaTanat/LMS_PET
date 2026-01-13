from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """
    Returns the value split by the argument.
    Usage: {{ value|split:"/" }}
    """
    if value:
        return value.split(arg)
    return []
