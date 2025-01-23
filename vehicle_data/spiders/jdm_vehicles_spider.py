import scrapy
import os
import re
from dotenv import load_dotenv

load_dotenv()

class JDMVehiclesSpider(scrapy.Spider):
    name = "JDMVehicles"
    allowed_domains = [re.match(r"https?://(?:www\.)?([^/]+)", url).group(1) for url in os.getenv('JDM_VEHICLE_DATA_URLS').split(',')]
    start_urls = os.getenv('JDM_VEHICLE_DATA_URLS').split(',')

    def parse(self, response):

        return
        # for quote in response.css("div.quote"):
        #     yield {
        #         "text": quote.css("span.text::text").get(),
        #         "author": quote.css("small.author::text").get(),
        #         "tags": quote.css("div.tags a.tag::text").getall(),
        #     }