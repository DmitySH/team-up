from django import template
from ..models import *

register = template.Library()


@register.filter(name='times')
def times(number):
    return range(number)


@register.filter(name='index')
def index_from_one(indexable, i):
    return indexable[i - 1]


@register.filter(name='iter')
def itter(gen):
    return next(gen)
