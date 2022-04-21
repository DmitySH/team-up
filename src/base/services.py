from django.core.exceptions import PermissionDenied
from django.shortcuts import _get_queryset
from django.urls import path, include

from config.settings import API_VERSION


def check_auth(request):
    """
    Check if user is authenticated.
    """

    if not request.user.is_authenticated:
        raise PermissionDenied


def check_own_project(request, slug):
    """
    Checks if user has project.
    """

    if request.user.profile.project:
        if request.user.profile.project.title != slug:
            raise PermissionDenied
    else:
        raise PermissionDenied


def check_own_slot(request, slot):
    """
    Check if user owns slot with slot id = slot.
    """
    if request.user.profile.project:
        if slot not in request.user.profile.project.team.all():
            raise PermissionDenied
    else:
        raise PermissionDenied


def check_slug_auth(request, slug):
    """
    Check if user has same username as in request.
    """

    check_auth(request)
    if not request.user.username == slug:
        raise PermissionDenied


def change_labels(form, labels):
    """
    Changes labels in form.
    """

    for i, field in enumerate(form.fields):
        form[field].label = labels[i]


def change_choices(form, choices):
    """
    Changes choices of form.
    """

    for i, field in enumerate(form.fields):
        form.fields[field].choices = choices[i]


def analyze_belbin(data):
    """
    Gets results of belbin test.
    """

    result = {
        'Исполнитель': data[0]['answer6'] + data[1]['answer0'] \
                       + data[2]['answer7'] + data[3]['answer3'] \
                       + data[4]['answer1'] + data[5]['answer5'] \
                       + data[6]['answer4'],
        'Координатор': data[0]['answer3'] + data[1]['answer1'] \
                       + data[2]['answer0'] + data[3]['answer7'] \
                       + data[4]['answer5'] + data[5]['answer2'] \
                       + data[6]['answer6'],
        'Мотиватор': data[0]['answer5'] + data[1]['answer4'] \
                     + data[2]['answer2'] + data[3]['answer1'] \
                     + data[4]['answer3'] + data[5]['answer6'] \
                     + data[6]['answer0'],
        'Генератор идей': data[0]['answer2'] + data[1]['answer6'] \
                          + data[2]['answer3'] + data[3]['answer4'] \
                          + data[4]['answer7'] + data[5]['answer0'] \
                          + data[6]['answer5'],
        'Исследователь ресурсов': data[0]['answer0'] + data[1]['answer2'] \
                                  + data[2]['answer5'] + data[3]['answer6'] \
                                  + data[4]['answer4'] + data[5]['answer7'] \
                                  + data[6]['answer3'],
        'Аналитик-стратег': data[0]['answer7'] + data[1]['answer3'] \
                            + data[2]['answer6'] + data[3]['answer2'] \
                            + data[4]['answer0'] + data[5]['answer4'] \
                            + data[6]['answer1'],
        'Душа команды': data[0]['answer1'] + data[1]['answer5'] \
                        + data[2]['answer4'] + data[3]['answer0'] \
                        + data[4]['answer2'] + data[5]['answer1'] \
                        + data[6]['answer7'],
        'Педант': data[0]['answer4'] + data[1]['answer7'] \
                  + data[2]['answer1'] + data[3]['answer5'] \
                  + data[4]['answer6'] + data[5]['answer3'] \
                  + data[6]['answer2']
    }

    result = {k: v for k, v in
              sorted(result.items(), key=lambda item: -item[1])}
    max_value = max(result.values())
    maxes = list(filter(lambda x: result[x] == max_value, result.keys()))
    if len(maxes) >= 2:
        return maxes
    else:
        keys = list(result.keys())
        return [keys[i] for i in range(2)]


def analyze_mbti(data):
    """
    Gets results of mbti test.
    """

    result = [
        (
            ['Экстраверт', 0],
            ['Интроверт', 0]
        ),
        (
            ['Сенсорик', 0],
            ['Интуит', 0]
        ),
        (
            ['Этик', 0],
            ['Логик', 0]
        ),
        (
            ['Рационал', 0],
            ['Иррационал', 0]
        )
    ]

    for form in data:
        if form['answer1'] == 0:
            result[0][0][1] += 1
        else:
            result[0][1][1] += 1

        if form['answer2'] == 0:
            result[1][0][1] += 1
        else:
            result[1][1][1] += 1

        if form['answer3'] == 0:
            result[1][0][1] += 1
        else:
            result[1][1][1] += 1

        if form['answer4'] == 0:
            result[2][0][1] += 1
        else:
            result[2][1][1] += 1

        if form['answer5'] == 0:
            result[2][0][1] += 1
        else:
            result[2][1][1] += 1

        if form['answer6'] == 0:
            result[3][0][1] += 1
        else:
            result[3][1][1] += 1

        if form['answer7'] == 0:
            result[3][0][1] += 1
        else:
            result[3][1][1] += 1

    return [
        item[0][0] if item[0][1] > item[1][1] else item[1][0] for item in
        result
    ]


def analyze_lsq(data):
    """
    Gets results of lsq tests.
    """

    result = [
        (
            ['Деятель', 0],
            ['Теоретик', 0]
        ),
        (
            ['Прагматик', 0],
            ['Рефлексирующий', 0]
        ),
    ]

    for form in data:
        result[0][0][1] += form['answer1']
        result[1][1][1] += form['answer2']
        result[0][1][1] += form['answer3']
        result[1][0][1] += form['answer4']

    return [
        item[0][0] if item[0][1] > item[1][1] else item[1][0] for item in
        result
    ]


def get_object_or_none(klass, *args, **kwargs):
    """
    Gets object with kwargs or None if no such object.
    """

    queryset = _get_queryset(klass)
    if not hasattr(queryset, 'get'):
        klass__name = klass.__name__ if isinstance(klass,
                                                   type) \
            else klass.__class__.__name__
        raise ValueError(
            "First argument to get_object_or_none must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def add_prefix_to_urls(api_urls, prefix='api/' + API_VERSION):
    """
    Adds prefix to urlpatterns list.
    """

    api_urls = [path(f'{prefix}/', include(api_urls))]
    return api_urls
