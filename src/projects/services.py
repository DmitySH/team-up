from fractions import Fraction

from rest_framework.exceptions import ValidationError

from src.accounts.models import ProfileProjectStatus, Status
from src.projects.models import Project, WorkerSlot


def update_or_create_project(profile, data):
    """
    Updates project if exists, else creates it.
    """

    qs = Project.objects.filter(title=data.get('title'))

    if qs.exists() and profile.project != qs.first():
        raise ValidationError('Project title must be unique.', code='unique')

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

    if not profile.project:
        return set()
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


def clear_slot(slot):
    slot.profile = None
    slot.save()


def analyzer(project):
    result = {
        'Вакансий занято': 0,
        'Работников с неизвестными ролями по Белбину': 0,
        'Присутствуют необходимые роли по Белбину': 0,
        'Присутствуют необходимые специализации': 0,
        'Суммарная зарплата': 0,
        'Пересечение ролей по Белбину': 0,
    }

    team_roles = list()
    team_specs = list()

    team = project.team.all()
    for slot in team:
        if slot.profile:
            result['Вакансий занято'] += 1
            profile = slot.profile

            result['Суммарная зарплата'] += slot.salary
            if not profile.belbin.exists():
                result['Работников с неизвестными ролями по Белбину'] += 1
            else:
                roles = profile.belbin.all()
                team_roles.extend(roles)

            if profile.specialization.exists():
                specs = profile.specialization.all()
                team_specs.extend(specs)

    for required_role in project.required_belbin.all():
        if required_role in team_roles:
            result['Присутствуют необходимые роли по Белбину'] += 1

    for role in set(team_roles):
        if team_roles.count(role) > 1:
            result['Пересечение ролей по Белбину'] += 1

    for required_spec in project.required_specialization.all():
        if required_spec in team_specs:
            result['Присутствуют необходимые специализации'] += 1
    result = {
        'Вакансий занято': Fraction(result['Вакансий занято'], len(team),
                                    _normalize=False),
        'Работников с неизвестными ролями по Белбину':
            result['Работников с неизвестными ролями по Белбину'],
        'Присутствуют необходимые роли по Белбину': Fraction(
            result['Присутствуют необходимые роли по Белбину'],
            project.required_belbin.count(),
            _normalize=False),
        'Присутствуют необходимые специализации': Fraction(
            result['Присутствуют необходимые специализации'],
            project.required_specialization.count(),
            _normalize=False),
        'Суммарная зарплата': result['Суммарная зарплата'],
        'Пересечение ролей по Белбину': result['Пересечение ролей по Белбину'],
    }

    for k, v in result.items():
        if isinstance(v, Fraction):
            if v.__float__() < 0.5:
                result[k] = (v, -1)
            elif v.__float__() < 0.7:
                result[k] = (v, 0)
            else:
                result[k] = (v, 1)

    if result['Пересечение ролей по Белбину'] <= 1:
        result['Пересечение ролей по Белбину'] = (
            result['Пересечение ролей по Белбину'], 1)
    elif result['Пересечение ролей по Белбину'] < 4:
        result['Пересечение ролей по Белбину'] = (
            result['Пересечение ролей по Белбину'], 0)
    else:
        result['Пересечение ролей по Белбину'] = (
            result['Пересечение ролей по Белбину'], -1)

    if result[
        'Работников с неизвестными ролями по Белбину'] <= team.count() / 10:
        result['Работников с неизвестными ролями по Белбину'] = (
            result['Работников с неизвестными ролями по Белбину'], 1)
    elif result[
        'Работников с неизвестными ролями по Белбину'] < team.count() / 4:
        result['Работников с неизвестными ролями по Белбину'] = (
            result['Работников с неизвестными ролями по Белбину'], 0)
    else:
        result['Работников с неизвестными ролями по Белбину'] = (
            result['Работников с неизвестными ролями по Белбину'], -1)

    result['Суммарная зарплата'] = (result['Суммарная зарплата'], 0)

    bad_count = 0
    good_count = 0

    for v in result.values():
        if v[1] == 1:
            good_count += 1
        elif v[1] == -1:
            bad_count += 1

    final_result = 0
    if bad_count > 2:
        final_result = -1
    elif good_count >= 4 and bad_count == 0:
        final_result = 1

    return result, final_result
