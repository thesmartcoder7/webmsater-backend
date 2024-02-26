from django.urls import path
from authusers.views import *

urlpatterns = [
    path('', all_users, name='all_users'),
    path('register/', register, name='register_auth_users'),
    path('login/', login, name='login_auth_usres')
]
