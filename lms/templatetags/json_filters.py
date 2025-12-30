from django import template
import json

register = template.Library()

@register.filter
def json_loads(value):
    try:
        return json.loads(value)
    except Exception:
        return None
