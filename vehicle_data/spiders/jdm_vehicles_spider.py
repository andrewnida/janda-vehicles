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

    def parse(self, response):
        make = response.css("#main > div.colmask_wide > div.col_wide > h4 > b:nth-child(1)::text").get().title()
        region = make.split(" ")[-1]
        models = response.css("ul.category2 li h4 a").getall()
        make_path = response.url
        
        for link in models:
            selector = scrapy.Selector(text=link)
            model = selector.css("a::text").get().title()
            model_path = selector.css("a::attr(href)").get()
            url_req = response.url[:-1] + model_path
            
            meta = {
                "region": region, 
                "make": make,
                "make_path": make_path,
                "model": model,
                "model_path": model_path,
            }
            callback = self.parse_frames

            yield scrapy.Request(url=url_req, callback=callback, meta=meta)
            
            break # remove in production

    def parse_frames(self, response):
        frames = response.css("ul.category2 li h4 a").getall()

        for frame in frames:
            selector = scrapy.Selector(text=frame)
            frame = selector.css("a::text").get()
            frame_path = selector.css("a::attr(href)").get()
            url_req = os.path.dirname(response.url[:-1]) + frame_path
            meta = response.meta.copy()
            meta["frame"] = frame.upper()
            meta["frame_path"] = frame_path
            callback = self.parse_vehicles
            
            yield scrapy.Request(url=url_req, callback=callback, meta=meta)

            break # remove in production
    
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
            vehicle_data_item["region"] = response.meta["region"]
            vehicle_data_item["make"] = response.meta["make"]
            vehicle_data_item["make_path"] = response.meta["make_path"]
            vehicle_data_item["model"] = response.meta["model"]
            vehicle_data_item["model_path"] = response.meta["model_path"]
            vehicle_data_item["vehicle_path"] = selector.css('a::attr(href)').get()
            vehicle_data_item["frame"] = response.meta["frame"]
            vehicle_data_item["frame_path"] = response.meta["frame_path"]
            vehicle_data_item["frame_num_from"] = frame_num[0]
            vehicle_data_item["frame_num_to"] = frame_num[1]
            vehicle_data_item["doors"] = vehicle_data[1]
            vehicle_data_item["transmission_code"] = vehicle_data[2].upper()
            vehicle_data_item["trim"] = vehicle_data[3].title()
            vehicle_data_item["options"] = list()
            
            for i in range(len(vehicle_data[4:])):
                if vehicle_data[4 + i] == '*':
                    vehicle_data_item["options"].append(options[4 + i])
            
            yield vehicle_data_item
