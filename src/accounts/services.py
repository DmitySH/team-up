from src.accounts.models import ProfileProjectStatus, Status


def update_password(user, new_pw):
    user.set_password(new_pw)
    user.save()


def accept_slot_invite(slot, profile):
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
    if slot in profile.get_applied_slots():
        apply = ProfileProjectStatus.objects.get(
            worker_slot=slot,
            profile=profile,
            status=Status.objects.get(
                value='Ожидает'))
        apply.delete()
        return True

    return False
