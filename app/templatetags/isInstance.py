from django import template

register = template.Library()

@register.filter
def isInstance(value, type):
    return isinstance(value, type)