from django.urls import path
from authusers.views import *

urlpatterns = [
    path('', home, name='auth_users.home'),
   
]
