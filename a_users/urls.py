from django.urls import path
from a_users.views import *

urlpatterns = [
    path('', profile_view, name='profile'),
    path('edit/', profile_edit_view, name='profile_edit'),
    path('onboarding/', profile_edit_view, name='profile_onboarding'),
    path('settings/', profile_settings_view, name='profile_settings'),
    path('emailchange/', profile_emailchange, name='profile_emailchange'),
    path('emailverify/', profile_emailverify, name='profile_emailverify'),
    path('delete/', profile_delete_view, name='profile_delete'),
]