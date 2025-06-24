# Author: Nurzatilimani binti Muhamad Ahwan
# Matric No: 24200114

from django import template

register = template.Library()

@register.filter
def get_item(obj, key):
    # If it's a dict, use .get()
    if isinstance(obj, dict):
        return obj.get(key)
    # If it's a Django model instance, use attribute access
    return getattr(obj, key, None)