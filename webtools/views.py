from rest_framework.decorators import api_view
from rest_framework.response import Response
from webtools.sitemap import SitemapGenerator
from webtools.domain import *
from webtools.page_speed_insights import process_psi_data


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
    domain =  request.data['domain']
    response = {}

    print(f'Performing Domain Check on {domain}')

    ssl_cetificate = get_ssl_certificate(domain=domain)
    cipher_suites = check_cipher_suites(ssl_cetificate)
    security_headers = check_security_headers(domain=domain)
    dns_info = get_dns_configuration(domain)
    domain_check = domain_health_check(domain)
    whois_check = doman_whois(domain)

    response = {
        'ssl_cetificate': ssl_cetificate,
        'cipher_suites' : cipher_suites,
        'security_headers' : security_headers,
        'dns_info': dns_info,
        'domain_check': domain_check,
        'whois_check': whois_check,
    }

    print(f'Domain Check on {domain} has been successfully completed')

    return Response(response)


@api_view(['POST'])
def page_insights(request):
    domain =  request.data['domain']
    response = {}

    print(f'Performing PageSpeed analysis Check on {domain}')

    response = {
        'page_insights': process_psi_data(domain)
    }

    print(f'PageSpeed analysis on {domain} has been successfully completed')

    return Response(response)

