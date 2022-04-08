from src.tests.models import BelbinTest, MBTITest, LSQTest


def validate_block_sum(data):
    if sum(map(int, data)) != 10:
        return False
    else:
        return True


def update_belbin(roles, profile):
    for role in roles:
        profile.belbin.add(
            BelbinTest.objects.get(role=role))
    profile.save()


def update_mbti(roles, profile):
    for role in roles:
        profile.mbti.add(
            MBTITest.objects.get(role=role))
    profile.save()


def update_lsq(roles, profile):
    for role in roles:
        profile.belbin.add(
            LSQTest.objects.get(role=role))
    profile.save()
