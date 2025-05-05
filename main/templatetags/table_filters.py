from django import template
from django.template.base import VariableDoesNotExist

register = template.Library()

@register.filter
def get_item(obj, key):
    """
    Template filter to get an attribute from an object, supporting nested attributes
    """
    try:
        # Handle nested attributes (e.g., 'idclass.nom')
        if '.' in key:
            attrs = key.split('.')
            value = obj
            for attr in attrs:
                value = getattr(value, attr)
            return value
        # Handle direct attributes
        return getattr(obj, key)
    except (AttributeError, VariableDoesNotExist):
        return ''