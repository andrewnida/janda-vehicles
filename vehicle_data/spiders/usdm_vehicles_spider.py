import scrapy
import os
import re
from dotenv import load_dotenv
from vehicle_data.items import VehicleDataItem

load_dotenv()

class USDMVehiclesSpider(scrapy.Spider):
    name = "USDMVehicles"
    allowed_domains = [re.match(r"https?://(?:www\.)?([^/]+)", url).group(1) for url in os.getenv('USDM_VEHICLE_DATA_URLS').split(',')]
    start_urls = os.getenv('USDM_VEHICLE_DATA_URLS').split(',')

    def __init__(self, db=None, *args, **kwargs):
        super(USDMVehiclesSpider, self).__init__(*args, **kwargs)

        if db is None:
            raise scrapy.exceptions.CloseSpider(reason="Mandatory argument 'db' is missing")

        self.database = db
    
    def parse(self, response):
        make = response.css("#root > header > div > div.com-header-middle > ul > li:nth-child(1) > a::text").get().title().split(' ')[0]
        region = response.css("#root > footer > div.com-footer-content > div > div.com-footer-inner-links > ul > li:nth-child(5) > ul > li:nth-child(1) > div::text").get().rsplit(",", 1)[1].strip(" .")
        models = response.css("#root > div > div.cal-home-bottom.container > div.ab-link-list.home-link-list > div.ab-link-list-body > div > a").getall()
        
        for link in models:
            selector = scrapy.Selector(text=link)
            model = selector.css("a::text").get()
            model_path = selector.css("a::attr(href)").get()
            url_req = response.url[:-1] + model_path
            
            meta = {
                "region": region, 
                "make": make,
                "model": model,
            }

            callback = self.parse_models

            yield scrapy.Request(url=url_req, callback=callback, meta=meta)
            
            if os.getenv("DEBUG"):
                break

    def parse_models(self, response):
        years = response.css("#root > div > div.cal-home-bottom.container > div.ab-link-list.home-link-list > div.ab-link-list-body > div > a").getall()

        for y in years:
            selector = scrapy.Selector(text=y)
            year = selector.css("a::text").get()

            year_path = selector.css("a::attr(href)").get()
            url_req = os.path.dirname(response.url[:-1]) + year_path
            meta = response.meta.copy()
            meta["year"] = year
            callback = self.parse_vehicles

            yield scrapy.Request(url=url_req, callback=callback, meta=meta)

            if os.getenv("DEBUG"):
                break

    def parse_vehicles(self, response):
        tables = response.css(".vehicle-option > .list > div").getall()
        
        for table in tables:
            selector = scrapy.Selector(text=table)
            vehicles = selector.css("div > .content > .text").getall()

            for vehicle in vehicles:
                selector = scrapy.Selector(text=vehicle)
                vehicle_model = re.findall(r'\([^)]*\)|\S+', selector.css('.text > li > a::text').get())
                transmission_code = vehicle_model[-1]
                trim = vehicle_model[2].title() if any(vowel in vehicle_model[2].lower() for vowel in 'aeiou') else vehicle_model[2]
                variant = (vehicle_model[3][1:-1]).title() if '(' in vehicle_model[3] else ""
                area_code = vehicle_model[-2]
                vehicle_path = selector.css('.text > li > a::attr(href)').get()

                vehicle_data_item = VehicleDataItem()
                vehicle_data_item["region_display"] = response.meta["region"]
                vehicle_data_item["make_display"] = response.meta["make"]
                vehicle_data_item["model_display"] = response.meta["model"]
                vehicle_data_item["year"] = response.meta["year"]
                vehicle_data_item["doors"] = vehicle_model[0]
                vehicle_data_item["transmission_code"] = transmission_code[1:]
                vehicle_data_item["transmission_auto"] = False if "MT" in vehicle_data_item["transmission_code"] else True
                vehicle_data_item["transmission_speeds"] = transmission_code[0]
                vehicle_data_item["trim_display"] = trim
                vehicle_data_item["variant_display"] = variant
                vehicle_data_item["area_code_display"] = area_code.upper()
                vehicle_data_item["vehicle_path"] = os.path.dirname(response.url[:-1]) + vehicle_path
                vehicle_data_item["options"] = list()
                
                yield vehicle_data_item
