import types

from django.core.exceptions import PermissionDenied


def check_auth(request):
    if not request.user.is_authenticated:
        raise PermissionDenied


def check_slug_auth(request, slug):
    check_auth(request)
    if not request.user.username == slug:
        raise PermissionDenied


def change_labels(form, labels):
    for i, field in enumerate(form.fields):
        form[field].label = labels[i]


def analize_belbin(data):
    result = {'Исполнитель': data[0]['answer6'] + data[1]['answer0'] \
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
              'Исследователь ресурсов': data[0]['answer0'] \
                                        + data[1]['answer2'] \
                                        + data[2]['answer5'] + data[3][
                                            'answer6'] \
                                        + data[4]['answer4'] + data[5][
                                            'answer7'] \
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
                        + data[6]['answer2']}

    result = {k: v for k, v in
              sorted(result.items(), key=lambda item: -item[1])}
    max_value = max(result.values())
    maxes = list(filter(lambda x: result[x] == max_value, result.keys()))
    if len(maxes) >= 2:
        return maxes
    else:
        keys = list(result.keys())
        return [keys[i] for i in range(2)]
