from django import template

register = template.Library()


@register.simple_tag()
def lookup(obj, field):
    return getattr(obj, field)

