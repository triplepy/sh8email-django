from django import template
from django.template.defaultfilters import stringfilter
from lxml.html.clean import Cleaner

register = template.Library()


@register.filter
@stringfilter
def clean_html(html):
    cleaner = Cleaner(safe_attrs_only=False)
    return cleaner.clean_html(html)
