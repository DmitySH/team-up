from src.accounts.models import ProfileProjectStatus, Status
from src.projects.models import Project, WorkerSlot


def update_or_create_project(profile, data):
    """
    Updates project if exists, else creates it.
    """

    project, created = Project.objects.update_or_create(
        owner=profile,
        defaults={'description': data.get('description'),
                  'title': data.get('title'),
                  'vacant': data.get('vacant'),
                  'owner': profile,
                  'city': data.get('city') or '',
                  'online': data.get('online'),
                  }
    )

    project.required_specialization.set(data.get(
        'required_specialization'))
    project.required_belbin.set(data.get('required_belbin'))

    return created


def update_or_create_worker_slot(project, data):
    """
    Updates worker slot if exists, else creates it.
    """
    slot, created = WorkerSlot.objects.update_or_create(
        project=project,
        id=data.get('id'),

        defaults={'description': data.get('description'),
                  'salary': data.get('salary'),
                  'work_hours': data.get('work_hours') or 40,
                  }
    )

    slot.specialization.set(data.get(
        'specialization'))
    slot.role.set(data.get('role'))

    return created


def check_same_applies(invited_profile, slot):
    """
    Checks if profile already have same applies to this slot.
    """

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
    """
    Makes user to wait for slot.
    """

    return ProfileProjectStatus.objects.get_or_create(
        profile=profile,
        worker_slot=slot,
        status=Status.objects.get(
            value='Ожидает'))


def get_invited_status(profile, slot):
    """
    Gets all invited profile project statuses with that user and slot.
    """

    return ProfileProjectStatus.objects.filter(
        profile=profile,
        worker_slot=slot,
        status=Status.objects.get(
            value='Приглашен'))


def get_team(profile):
    """
    Gets team of user's project.
    """

    return profile.project.team.all()


def get_applied_for_slot(slot):
    """
    Gets profiles which were applied to slot.
    """

    applies = ProfileProjectStatus.objects.filter(
        worker_slot=slot,
        status=Status.objects.get(
            value='Ожидает')).select_related('profile',
                                             'profile__executor_offer')
    profiles = [apply.profile for apply in applies]
    return profiles


def delete_apply(slot, profile):
    """
    Deletes applies of that user to selected slot.
    """

    if slot in profile.get_applied_slots():
        apply = ProfileProjectStatus.objects.get(
            worker_slot=slot,
            profile=profile,
            status=Status.objects.get(
                value='Ожидает'))
        apply.delete()
