from django import template

register = template.Library()


@register.filter
def get_at_index(arr, index):
    return arr[index]
