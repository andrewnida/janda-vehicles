import scrapy
import os
import re
from dotenv import load_dotenv

load_dotenv()

class USDMVehiclesSpider(scrapy.Spider):
    name = "USDMVehicles"
    allowed_domains = [re.match(r"https?://(?:www\.)?([^/]+)", url).group(1) for url in os.getenv('USDM_VEHICLE_DATA_URLS').split(',')]
    start_urls = os.getenv('USDM_VEHICLE_DATA_URLS').split(',')

    def parse(self, response):

        return
        # for quote in response.css("div.quote"):
        #     yield {
        #         "text": quote.css("span.text::text").get(),
        #         "author": quote.css("small.author::text").get(),
        #         "tags": quote.css("div.tags a.tag::text").getall(),
        #     }