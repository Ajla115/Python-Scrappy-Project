import scrapy

from urllib.parse import urlencode

from urllib.parse import urlparse

from pathlib import Path

import json

import ast

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

        queries = ['selena+gomez']

        for query in queries:

            url = create_google_url(query)

            yield scrapy.Request(get_url(url), callback=self.parse, meta={'pos': 0})

    def parse(self, response):

        # for result in response.css('div.e9EfHf'): 
        #     yield { 
        #         'url': result.css('a::attr(href)').get(),      
        #     } 

        filename = f"politicalSpider.html"
        page_content = response.body
        byte_str = page_content.decode("UTF-8")
        mydata= ast.literal_eval(byte_str)
        
        # print(mydata["knowledge_graph"]["social_media"][1]["link"])

        social_media_list = mydata["knowledge_graph"]["social_media"]
       
        for i in range(len(social_media_list)):
            yield {
                "Social media link" : social_media_list[i]["link"]
                }

        organic_results_list = mydata["organic_results"]
        for i in range(len(organic_results_list)):
            yield {
               "Organic results link" : organic_results_list[i]["link"]
                }

        #run with a command scrapy crawl politician -O politician3.json

        # Path(filename).write_bytes(page_content)
        # self.log(f"Saved file {filename}")

