from rest_framework.utils import model_meta

from src.accounts.models import ProfileProjectStatus, Status, ExecutorOffer


def update_password(user, new_pw):
    """
    Updates password of user.
    """

    user.set_password(new_pw)
    user.save()


def only_fields_object_update(obj, data):
    """
    Updates fields of object.
    """

    for attr, value in data.items():
        setattr(obj, attr, value)
    obj.save()


def object_update(obj, data):
    """
    Fully updates object.
    """

    m2m_fields = []
    info = model_meta.get_field_info(obj)

    for attr, value in data.items():
        if attr in info.relations and info.relations[attr].to_many:
            m2m_fields.append((attr, value))
        else:
            setattr(obj, attr, value)

    obj.save()

    for attr, value in m2m_fields:
        field = getattr(obj, attr)
        field.set(value)


def update_or_create_offer(profile, data):
    """
    Updates if exists or creates executor offer for profile.
    """

    offer, created = ExecutorOffer.objects.update_or_create(
        profile=profile,
        defaults={'description':
                      data.get('description'),
                  'salary':
                      data.get('salary'),
                  'work_hours':
                      data.get('work_hours') or 40,
                  'profile':
                      profile}
    )

    return created


def accept_slot_invite(slot, profile):
    """
    Accepts invite to slot.
    """

    if slot in profile.get_invited_slots():
        slot.profile = profile
        other_invites = ProfileProjectStatus.objects.filter(
            worker_slot=slot,
            status=Status.objects.get(
                value='Приглашен'))
        other_invites.delete()
        slot.save()
        return True

    return False


def decline_slot_invite(slot, profile):
    """
    Declines invite to slot.
    """

    if slot in profile.get_invited_slots():
        invite = ProfileProjectStatus.objects.get(
            worker_slot=slot,
            profile=profile,
            status=Status.objects.get(
                value='Приглашен'))
        invite.delete()
        return True

    return False


def retract_slot_apply(slot, profile):
    """
    Retracts invite to slot.
    """

    if slot in profile.get_applied_slots():
        apply = ProfileProjectStatus.objects.get(
            worker_slot=slot,
            profile=profile,
            status=Status.objects.get(
                value='Ожидает'))
        apply.delete()
        return True

    return False
