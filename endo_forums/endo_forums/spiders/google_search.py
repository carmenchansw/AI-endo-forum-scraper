"""
Attribution Note : 
This file contains code adapted and customised from the open-source project : 
https://github.com/ian-kerins/google-scraper-python-scrapy/tree/master
Original Author : Ian Kerins
"""

import os
import scrapy
from urllib.parse import urlencode, urlparse
import json
from datetime import datetime
from dotenv import load_dotenv

# 🚨 FIX 1: Run load_dotenv() so Python actually processes the .env file
load_dotenv()
API_KEY = os.getenv('SCRAPER_API_KEY')

def get_url(url):
    if not API_KEY:
        raise ValueError("API_KEY not found! Ensure SCRAPER_API_KEY is set in your .env file.")
    payload = {'api_key': API_KEY, 'url': url, 'autoparse': 'true', 'country_code': 'us'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url

def create_google_url(query, site=''):
    google_dict = {'q': query, 'num': 100}
    if site:
        web = urlparse(site).netloc
        google_dict['as_sitesearch'] = web
    return 'http://www.google.com/search?' + urlencode(google_dict)


class GoogleSpider(scrapy.Spider):
    # 🚨 FIX 2: Explicitly match the spider name for your command line execution
    name = 'google_search'
    
    # 🚨 FIX 3: Include google domains so Scrapy doesn't filter them out as offsite
    allowed_domains = ['api.scraperapi.com', 'google.com', 'www.google.com']
    
    custom_settings = {
        'ROBOTSTXT_OBEY': False, 
        'LOG_LEVEL': 'INFO',
        'CONCURRENT_REQUESTS_PER_DOMAIN': 5, 
        'RETRY_TIMES': 5
    }

    def start_requests(self):
        queries = ['scrapy'] 
        for query in queries:
            url = create_google_url(query)
            yield scrapy.Request(get_url(url), callback=self.parse, meta={'pos': 0})

    def parse(self, response):
        if not response.text:
            self.logger.error("Empty response text received.")
            return

        try:
            di = json.loads(response.text)
        except json.JSONDecodeError:
            self.logger.error("Failed to decode response as JSON.")
            return

        if 'organic_results' not in di:
            self.logger.error(f"Missing 'organic_results'. Keys found: {list(di.keys())}")
            return

        pos = response.meta['pos']
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        for result in di['organic_results']:
            item = {
                'title': result.get('title', 'No Title'), 
                'snippet': result.get('snippet', 'No Snippet'), 
                'link': result.get('link', ''), 
                'position': pos, 
                'date': dt
            }
            pos += 1
            yield item
            
        next_page = di.get('pagination', {}).get('nextPageUrl')
        if next_page:
            yield scrapy.Request(get_url(next_page), callback=self.parse, meta={'pos': pos})