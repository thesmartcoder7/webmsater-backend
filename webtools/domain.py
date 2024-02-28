import ssl
import socket
import requests
import dns.resolver
import smtplib
from datetime import datetime
import whois


def get_ssl_certificate(domain):
    try:
        # Create a socket
        sock = socket.create_connection((domain, 443))

        # Wrap the socket with SSL context
        context = ssl.create_default_context()
        with context.wrap_socket(sock, server_hostname=domain) as ssock:
            # Retrieve the SSL certificate
            cert = ssock.getpeercert()
            return cert
    except Exception as e:
        error = {
            'error': f"Error retrieving SSL certificate for {domain}: {e}"
        }
        return error

    

def check_cipher_suites(cert):
    try:
        # Get the list of cipher suites supported by the certificate
        cipher_suites = cert.get('cipher')
        
        if cipher_suites:
            return {"suites": cipher_suites}
        else:
            return {'not-found': 'No cipher suites found in the certificate.'}
    except Exception as e:
        return {'error': f"Error checking cipher suites: {e}"}




def check_security_headers(domain):
    try:
        # Send an HTTP GET request to the specified domain
        response = requests.get(f"https://{domain}")

        # Check for the presence of security headers in the response
        security_headers = {
            "Strict-Transport-Security",
            "X-Content-Type-Options",
            "X-Frame-Options",
            "X-XSS-Protection",
            "Content-Security-Policy",
            "Referrer-Policy",
            "Feature-Policy"
        }
        
        missing_headers = []
        for header in security_headers:
            if header not in response.headers:
                missing_headers.append(header)

        if missing_headers:
            return {'missing-headers':missing_headers}
        else:
            return {'success': "All security headers are present."}
    except Exception as e:
        return {'error':f'Error checking security headers: {e}'}


def get_dns_configuration(domain):
    try:
        # Initialize DNS resolver
        resolver = dns.resolver.Resolver()

        # Define DNS record types to query
        record_types = ['A', 'AAAA', 'CNAME', 'MX', 'TXT', 'NS', 'SOA']

        # Query DNS records for each record type
        records = {key: [] for key in record_types}

        for record_type in record_types:
            try:
                response = resolver.resolve(domain, record_type)
                for rdata in response:
                    records[record_type].append(f'{rdata}')
            except:
                ...
        return {'dns-records': records}
    except Exception as e:
        return {'error':'Error retrieving DNS configuration: {e}'}


def domain_health_check(domain):
    result = {}
    try:
        # DNS resolution check
        dns_resolution = dns.resolver.resolve(domain, 'A')
        result['dns-resolution'] = f"{dns_resolution.response.answer}"

        # SSL certificate check
        ssl_context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with ssl_context.wrap_socket(sock, server_hostname=domain) as ssock:
                check = ''
                if ssock.getpeercert():
                    check = 'SSL Check: Success!'
                else:
                    check = 'SSL Check: Unsuccessful!'
        
        result['ssl-check'] = check

        # Email deliverability check
        mx_records = dns.resolver.resolve(domain, 'MX')
        for mx in mx_records:
            try:
                smtp_server = smtplib.SMTP(mx.exchange.to_text(), timeout=10)
                smtp_server.quit()
                result[f'Email deliverability to {mx.exchange.to_text()}'] = 'Success'
            except Exception as e:
                result[f'Email deliverability to {mx.exchange.to_text()}'] = f'Error - {e}'

        # Website accessibility check
        response = requests.head(f"https://{domain}", timeout=10)
        if response.status_code == 200:
            result['Website accessibility'] = 'Available'
        else:
            result["Website accessibility"] = f"Error - HTTP status code {response.status_code}"


        # Additional checks (you can add more as needed)

    except:
        result['Error'] = 'Domain health check failed'
        ...

    return result
   

def doman_whois(domain):
    whois_info = whois.whois(domain)
    return {"whois-info": whois_info}




if __name__ == "__main__":
    domain = "samuel-martins.com"
    certificate = get_ssl_certificate(domain)
    check_cipher_suites(certificate)
    check_security_headers(domain)
    get_dns_configuration(domain)
    domain_health_check(domain)