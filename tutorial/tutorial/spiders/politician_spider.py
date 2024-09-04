import scrapy

from urllib.parse import urlencode

from urllib.parse import urlparse

from pathlib import Path

import json

from datetime import datetime

API_KEY = 'b46adb8c7afe0003aed4fa3d23894129'

def get_url(url):

    payload = {'api_key': API_KEY, 'url': url, 'autoparse': 'true', 'country_code': 'us'}

    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)

    return proxy_url

def create_google_url(query, site=''):

    google_dict = {'q': query, 'num': 100, }

    if site:

        web = urlparse(site).netloc

        google_dict['as_sitesearch'] = web

        return 'http://www.google.com/search?' + urlencode(google_dict)

    return 'http://www.google.com/search?' + urlencode(google_dict)

class PoliticianSpider2(scrapy.Spider):

    name = 'politician'

    allowed_domains = ['api.scraperapi.com']

    custom_settings = {'ROBOTSTXT_OBEY': False, 'LOG_LEVEL': 'INFO',

                       'CONCURRENT_REQUESTS_PER_DOMAIN': 10, 

                       'RETRY_TIMES': 5}

    def start_requests(self):

        queries = ['semir+efendic']

        for query in queries:

            url = create_google_url(query)

            yield scrapy.Request(get_url(url), callback=self.parse, meta={'pos': 0})

    def parse(self, response):

        filename = f"politicalSpider.html"
        page_content = response.body
        
        #print(page_content)

        Path(filename).write_bytes(page_content)
        

        self.log(f"Saved file {filename}")

