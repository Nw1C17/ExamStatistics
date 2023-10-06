from django import template

register = template.Library()


@register.simple_tag
def define(val=None):
    if len(val) > 1:
        return 1
    else:
        return 2
