from django.urls import path
from core.views.profile_list import ProfileList
from core.views.profile_create import ProfileCreate
from core.views.profile_update import ProfileUpdate
from core.views.profile_delete import profile_delete


urlpatterns = [
    path('', ProfileList.as_view(), name='list_profile'),
    path('profile_novo/', ProfileCreate.as_view(), name='create_profile'),
    path('profile_editar/<int:pk>/', ProfileUpdate.as_view(), name='update_profile'),
    path('profile_delete/<int:pk>/', profile_delete, name='delete_profile'),

]
