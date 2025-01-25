import scrapy
import os
import re
from dotenv import load_dotenv
from vehicle_data.items import VehicleDataItem

load_dotenv()

# Spider for crawling JDM parts catalogue site.
# Sites must be passed in as an environment variable.
class JDMVehiclesSpider(scrapy.Spider):
    name = "JDMVehicles"
    allowed_domains = [re.match(r"https?://(?:www\.)?([^/]+)", url).group(1) for url in os.getenv("JDM_VEHICLE_DATA_URLS").split(",")]
    start_urls = os.getenv("JDM_VEHICLE_DATA_URLS").split(",")

    def __init__(self, db=None, *args, **kwargs):
        super(JDMVehiclesSpider, self).__init__(*args, **kwargs)

        # Exit the spider if no database is given to write to
        if db is None:
            raise scrapy.exceptions.CloseSpider(reason="Mandatory argument 'db' is missing")

        self.database = db
    
    def parse(self, response):
        # Grab the text from the main page
        # Random text on the page that works
        make = response.css("#main > div.colmask_wide > div.col_wide > h4 > b:nth-child(1)::text").get().title()
        region = make.split(" ")[-1]
        
        # Query the models links for URLs
        models = response.css("ul.category2 li h4 a").getall()
        
        # Iterate over models and form requests for next level
        for link in models:
            # Grab the text from the main page
            selector = scrapy.Selector(text=link)
            model = selector.css("a::text").get().title()
            model_path = selector.css("a::attr(href)").get()
            
            # Form the request from the link and path in the anchor tag
            vehicle_path = response.url[:-1]
            url_req = response.url[:-1] + model_path
            
            # Pass it on to the next level
            meta = {
                "region": region, 
                "make": make,
                "model": model,
                "vehicle_path": vehicle_path
            }

            callback = self.parse_frames

            yield scrapy.Request(url=url_req, callback=callback, meta=meta)

    def parse_frames(self, response):
        # Get all the frames for the given model page
        frames = response.css("ul.category2 li h4 a").getall()

        # Iterate over all the frames and form URL requests for the next level
        for frame in frames:
            # Grab the text from the frames page
            selector = scrapy.Selector(text=frame)
            
            # Split up the frame chasiss e.g. "E-DC2"
            frame_chasiss = selector.css("a::text").get().split('-')
            frame = frame_chasiss[0] if len(frame_chasiss) > 1 else ""
            chasiss = frame_chasiss[-1]
            
            # URL to the vehicle page
            frames_chasiss_path = selector.css("a::attr(href)").get()
            url_req = os.path.dirname(response.url[:-1]) + frames_chasiss_path
            
            # Pass on the meta object with new field
            meta = response.meta.copy()
            meta["frame"] = frame.upper()
            meta["chasiss"] = chasiss.upper()
            
            callback = self.parse_vehicles
            
            yield scrapy.Request(url=url_req, callback=callback, meta=meta)
    
    def parse_vehicles(self, response):
        # Get the main table on the page
        table = response.css("table.table tbody tr").getall()
        vehicles = table[1:]
        selector = scrapy.Selector(text=table[0])
        
        # Get the option column headers.
        # We have to parse the asterisks in the rows to determine the options.
        options = selector.css("th::text").getall()

        # Iterate over all the vehicles and prepare the main Item
        for vehicle in vehicles:
            # Get the vehicle data for the row
            selector = scrapy.Selector(text=vehicle)
            vehicle_data = selector.css("td::text, a::text").getall()
            
            # Find the column with the frame number information
            frame_num = vehicle_data[0].split(" - ")

            # Prepare the VehicleDataItem
            vehicle_data_item = VehicleDataItem()
            vehicle_data_item["region_display"] = response.meta["region"]
            vehicle_data_item["make_display"] = response.meta["make"]
            vehicle_data_item["model_display"] = response.meta["model"]
            vehicle_data_item["frame_display"] = response.meta["frame"]
            vehicle_data_item["chasiss_display"] = response.meta["chasiss"]
            vehicle_data_item["frame_num_from"] = frame_num[0]
            vehicle_data_item["frame_num_to"] = frame_num[1]
            vehicle_data_item["doors"] = vehicle_data[1]

            # Default transmission to AT if it doesn't explicitly say MT
            # Just going to guess at the speeds for now and will need cleaning
            vehicle_data_item["transmission_code"] = vehicle_data[2].upper()
            vehicle_data_item["transmission_auto"] = False if "MT" in vehicle_data_item["transmission_code"] else True
            vehicle_data_item["transmission_speeds"] = 4 if vehicle_data_item["transmission_auto"] == True else 5
            
            # Make the trim all caps if it doesn't have any vowels
            # LS vs Type R - Just a guess but we'll have to clean it up
            vehicle_data_item["trim_display"] = vehicle_data[3].title() if any(vowel in vehicle_data[3].lower() for vowel in 'aeiou') else vehicle_data[3].upper()
            
            # Final URL for the vehicle to scrape later
            vehicle_data_item["vehicle_path"] = response.meta["vehicle_path"] + selector.css('a::attr(href)').get()
            
            # Parase out the options for the car
            vehicle_data_item["options"] = list()
            
            # Basically matches up the asterisks in each row to the text index of the headers
            # Then tries to guess all caps like "LSD" vs "Air Conditioning" - will need some clean up
            for i in range(len(vehicle_data[4:])):
                if vehicle_data[4 + i] == '*':
                    vehicle_data_item["options"].append(options[4 + i].title() if any(vowel in options[4 + i].lower() for vowel in 'aeiou') else options[4 + i])
            
            yield vehicle_data_item
