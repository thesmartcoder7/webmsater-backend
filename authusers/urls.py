from django.urls import path
from authusers.views import *

urlpatterns = [
    path('', all_users, name='all_users'),
    path('register/', register, name='register_auth_user'),
    path('login/', login, name='login_auth_user'),
    path('user/', check_user, name='get_auth_user'),
    path('logout/', logout, name='logout_auth_user')
]
