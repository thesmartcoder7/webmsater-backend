import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from urllib.robotparser import RobotFileParser

class SitemapGenerator:
    def __init__(self):
        self.visited_urls = set()
        self.sitemap = []

    def crawl_site(self, domain):
        self.domain = domain
        self.robot_parser = self.parse_robots_txt(domain)
        self.crawl_page(domain)
        return self.sitemap

    def crawl_page(self, url):
        if url in self.visited_urls:
            return
        self.visited_urls.add(url)
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            self.sitemap.append(url)
            for link in soup.find_all('a', href=True):
                next_url = urljoin(url, link['href'])
                if self.is_valid_url(next_url):
                    self.crawl_page(next_url)

    def is_valid_url(self, url):
        parsed_url = urlparse(url)
        if parsed_url.netloc != urlparse(self.domain).netloc:
            return False
        if parsed_url.scheme not in ('http', 'https'):
            return False
        if not self.robot_parser.can_fetch('*', url):
            return False
        return True

    def parse_robots_txt(self, domain):
        robot_url = urljoin(domain, '/robots.txt')
        robot_parser = RobotFileParser()
        robot_parser.set_url(robot_url)
        robot_parser.read()
        return robot_parser

    def generate_sitemap(self, domain):
        sitemap = self.crawl_site(domain)

        # Format sitemap as XML
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        for url in sitemap:
            xml += f'  <url>\n    <loc>{url}</loc>\n  </url>\n'
        xml += '</urlset>'

        return xml
