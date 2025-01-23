from pathlib import Path

import scrapy


class JDMVehiclesSpider(scrapy.Spider):
    name = "JDMVehicles"
    start_urls = [
        "https://honda.epc-data.com/",
        # "https://www.hondaacuraonline.com/",
    ]

    # def start_requests(self):
    #     urls = [
    #         "https://quotes.toscrape.com/page/1/",
    #         "https://quotes.toscrape.com/page/2/",
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        return
        # for quote in response.css("div.quote"):
        #     yield {
        #         "text": quote.css("span.text::text").get(),
        #         "author": quote.css("small.author::text").get(),
        #         "tags": quote.css("div.tags a.tag::text").getall(),
        #     }