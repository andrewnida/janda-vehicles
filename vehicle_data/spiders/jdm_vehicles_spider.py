import scrapy
import os
import re
from dotenv import load_dotenv
from vehicle_data.items import VehicleDataItem

load_dotenv()

class JDMVehiclesSpider(scrapy.Spider):
    name = "JDMVehicles"
    allowed_domains = [re.match(r"https?://(?:www\.)?([^/]+)", url).group(1) for url in os.getenv("JDM_VEHICLE_DATA_URLS").split(",")]
    start_urls = os.getenv("JDM_VEHICLE_DATA_URLS").split(",")

    def __init__(self, db=None, *args, **kwargs):
        super(JDMVehiclesSpider, self).__init__(*args, **kwargs)

        if db is None:
            raise scrapy.exceptions.CloseSpider(reason="Mandatory argument 'db' is missing")

        self.database = db
    
    def parse(self, response):
        make = response.css("#main > div.colmask_wide > div.col_wide > h4 > b:nth-child(1)::text").get().title()
        region = make.split(" ")[-1]
        models = response.css("ul.category2 li h4 a").getall()
        
        for link in models:
            selector = scrapy.Selector(text=link)
            model = selector.css("a::text").get().title()
            model_path = selector.css("a::attr(href)").get()
            vehicle_path = response.url[:-1]
            url_req = response.url[:-1] + model_path
            
            meta = {
                "region": region, 
                "make": make,
                "model": model,
                "vehicle_path": vehicle_path
            }
            callback = self.parse_frames

            yield scrapy.Request(url=url_req, callback=callback, meta=meta)
            
            if os.getenv("DEBUG"):
                break

    def parse_frames(self, response):
        frames = response.css("ul.category2 li h4 a").getall()

        for frame in frames:
            selector = scrapy.Selector(text=frame)
            frame_chasiss = selector.css("a::text").get().split('-')
            frame = frame_chasiss[0] if len(frame_chasiss) > 1 else ""
            chasiss = frame_chasiss[-1]
            frames_chasiss_path = selector.css("a::attr(href)").get()
            url_req = os.path.dirname(response.url[:-1]) + frames_chasiss_path
            meta = response.meta.copy()
            meta["frame"] = frame.upper()
            meta["chasiss"] = chasiss.upper()
            callback = self.parse_vehicles
            
            yield scrapy.Request(url=url_req, callback=callback, meta=meta)

            if os.getenv("DEBUG"):
                break
    
    def parse_vehicles(self, response):
        table = response.css("table.table tbody tr").getall()
        vehicles = table[1:]
        selector = scrapy.Selector(text=table[0])
        options = selector.css("th::text").getall()

        for vehicle in vehicles:
            selector = scrapy.Selector(text=vehicle)
            vehicle_data = selector.css("td::text, a::text").getall()
            frame_num = vehicle_data[0].split(" - ")

            vehicle_data_item = VehicleDataItem()
            vehicle_data_item["region_display"] = response.meta["region"]
            vehicle_data_item["make_display"] = response.meta["make"]
            vehicle_data_item["model_display"] = response.meta["model"]
            vehicle_data_item["frame_display"] = response.meta["frame"]
            vehicle_data_item["chasiss_display"] = response.meta["chasiss"]
            vehicle_data_item["frame_num_from"] = frame_num[0]
            vehicle_data_item["frame_num_to"] = frame_num[1]
            vehicle_data_item["doors"] = vehicle_data[1]
            vehicle_data_item["transmission_code"] = vehicle_data[2].upper()
            vehicle_data_item["transmission_auto"] = False if "MT" in vehicle_data_item["transmission_code"] else True
            vehicle_data_item["transmission_speeds"] = 4 if vehicle_data_item["transmission_auto"] == True else 5
            vehicle_data_item["trim_display"] = vehicle_data[3].title() if any(vowel in vehicle_data[3].lower() for vowel in 'aeiou') else vehicle_data[3].upper()
            vehicle_data_item["vehicle_path"] = response.meta["vehicle_path"] + selector.css('a::attr(href)').get()
            vehicle_data_item["options"] = list()
            
            for i in range(len(vehicle_data[4:])):
                if vehicle_data[4 + i] == '*':
                    vehicle_data_item["options"].append(options[4 + i].title() if any(vowel in options[4 + i].lower() for vowel in 'aeiou') else options[4 + i])
            
            yield vehicle_data_item
