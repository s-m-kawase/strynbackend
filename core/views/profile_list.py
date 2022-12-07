from django.views.generic import ListView
from core.models.profile import Profile


class ProfileList(ListView):
    model = Profile
    fileds = '__all__'

