from src.accounts.models import ProfileProjectStatus, Status


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
    else:
        return False
