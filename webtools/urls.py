from django.urls import path
from webtools.views import *
urlpatterns = [
    path('get_sitemap/', generate_sitemap, name='sitemap_generator'),
    path('domain_check/',domain_check, name="domain_checker")
]
