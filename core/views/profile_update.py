from django.urls import reverse_lazy
from django.views.generic import UpdateView
from core.models.profile import Profile


class ProfileUpdate(UpdateView):
    model = Profile
    fields = '__all__'

    def get_success_url(self):
       return reverse_lazy("list_profile")
