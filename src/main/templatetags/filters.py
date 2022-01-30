from django import template

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


@register.filter(name='leader')
def check_leader(profile):
    return profile.profile_statuses.filter(status__value='Создатель').exists()
