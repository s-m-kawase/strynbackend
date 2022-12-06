from django.shortcuts import redirect
from core.models.profile import Profile


def profile_delete(request,pk):
    iten = Profile.objects.get(id=pk)
    iten.delete()
    return redirect('list_profile')