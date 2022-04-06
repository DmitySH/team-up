from src.accounts.models import ProfileProjectStatus, Status


def check_same_applies(invited_profile, slot):
    same_applies = ProfileProjectStatus.objects.filter(
        profile=invited_profile,
        worker_slot=slot,
        status=Status.objects.get(
            value='Ожидает'))
    if same_applies:
        applied = same_applies.first()
        applied.status = Status.objects.get(
            value='Приглашен')
        applied.save()
    else:
        ProfileProjectStatus.objects.get_or_create(
            profile=invited_profile,
            worker_slot=slot,
            status=Status.objects.get(
                value='Приглашен'))


def create_waiting_status(profile, slot):
    return ProfileProjectStatus.objects.get_or_create(
        profile=profile,
        worker_slot=slot,
        status=Status.objects.get(
            value='Ожидает'))


def get_invited_status(profile, slot):
    return ProfileProjectStatus.objects.filter(
        profile=profile,
        worker_slot=slot,
        status=Status.objects.get(
            value='Приглашен'))


def get_team(profile):
    return profile.project().team.all()
