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
