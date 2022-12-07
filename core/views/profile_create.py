from django.views.generic import CreateView
from core.models.profile import Profile
from django.urls import reverse_lazy


class ProfileCreate(CreateView):
    model = Profile
    fields = '__all__'
    def get_success_url(self):
       return reverse_lazy("list_profile")