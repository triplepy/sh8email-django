from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def entitify_paren(origin):
    return origin.replace('(', '&#40;').replace(')', '&#41;')
