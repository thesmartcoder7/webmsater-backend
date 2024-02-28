from django.urls import path
from webtools.views import generate_sitemap

urlpatterns = [
    path('get_sitemap/', generate_sitemap, name='sitemap_generator'),
]
