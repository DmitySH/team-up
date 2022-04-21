from src.tests.models import BelbinTest, MBTITest, LSQTest


def validate_block_sum(data):
    """
    Validates sum of block in test.
    """

    if sum(map(int, data)) != 10:
        return False
    else:
        return True


def update_belbin(roles, profile):
    """
    Updates belbin roles.
    """

    for role in roles:
        profile.belbin.add(
            BelbinTest.objects.get(role=role))
    profile.save()


def update_mbti(roles, profile):
    """
    Updates mbti roles.
    """

    for role in roles:
        profile.mbti.add(
            MBTITest.objects.get(role=role))
    profile.save()


def update_lsq(roles, profile):
    """
    Updates lsq roles.
    """

    for role in roles:
        profile.belbin.add(
            LSQTest.objects.get(role=role))
    profile.save()


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
