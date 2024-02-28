from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from webtools.sitemap import SitemapGenerator
from webtools.domain import *


@api_view(['POST'])
def generate_sitemap(request):
    generator = SitemapGenerator()
    domain = request.data['domain']
    print(f"Generating Sitemap for {domain}\n")

    sitemap_xml = generator.generate_sitemap(domain)

    print(f"The Sitemap for {domain} has been successfully generated \n")
    return Response({
        "xml": sitemap_xml
    })


@api_view(['POST'])
def domain_check(request):
    print(f'Performing Domain Check on {domain}')
    domain =  request.data['domain']
    response = {}

    ssl_cetificate = get_ssl_certificate(domain=domain)
    cipher_suites = check_cipher_suites(ssl_cetificate)
    security_headers = check_security_headers(domain=domain)
    dns_info = get_dns_configuration(domain)
    domain_health_check = domain_check(domain)
    domain_whois = domain_whois(domain)

    response = {
        'ssl_cetificate': ssl_cetificate,
        'cipher_suites' : cipher_suites,
        'security_headers' : security_headers,
        'dns_info': dns_info,
        'domain_health_check': domain_health_check,
        'domain_whois': domain_whois,
    }

    print(f'Domain Check on {domain} has been successfully completed')

    return Response(response)

