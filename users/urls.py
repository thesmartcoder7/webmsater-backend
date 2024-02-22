from django.urls import path
from users.views import *

urlpatterns = [
    path('', all_users, name='webmaster_users'),
    path('check_user/', check_user, name='webmaster_user_check')
]
