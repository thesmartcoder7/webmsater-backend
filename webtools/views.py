from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from webtools.sitemap import SitemapGenerator


@api_view(['POST'])
def generate_sitemap(request):
    generator = SitemapGenerator()
    sitemap_xml = generator.generate_sitemap(request.data['domain'])

    print(sitemap_xml)
    return Response({
        "xml": sitemap_xml
    })