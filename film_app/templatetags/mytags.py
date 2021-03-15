from django import template

register = template.Library()

@register.filter
def parse_field(value, arg):
    return value[arg]