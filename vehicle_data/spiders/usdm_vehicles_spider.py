import scrapy
import os
import re
from dotenv import load_dotenv
from vehicle_data.items import VehicleDataItem

load_dotenv()

# Spider for crawling USDM parts catalogue site.
# Sites must be passed in as an environment variable.
class USDMVehiclesSpider(scrapy.Spider):
    name = "USDMVehicles"
    allowed_domains = [re.match(r"https?://(?:www\.)?([^/]+)", url).group(1) for url in os.getenv('USDM_VEHICLE_DATA_URLS').split(',')]
    start_urls = os.getenv('USDM_VEHICLE_DATA_URLS').split(',')

    def __init__(self, db=None, *args, **kwargs):
        super(USDMVehiclesSpider, self).__init__(*args, **kwargs)

         # Exit the spider if no database is given to write to
        if db is None:
            raise scrapy.exceptions.CloseSpider(reason="Mandatory argument 'db' is missing")

        self.database = db
    
    def parse(self, response):
        # Grab the text from the main page
        # Random text on the page that works
        make = response.css("#root > header > div > div.com-header-middle > ul > li:nth-child(1) > a::text").get().title().split(' ')[0]
        region = response.css("#root > footer > div.com-footer-content > div > div.com-footer-inner-links > ul > li:nth-child(5) > ul > li:nth-child(1) > div::text").get().rsplit(",", 1)[1].strip(" .")
        
        # Query the models links for URLs
        models = response.css("#root > div > div.cal-home-bottom.container > div.ab-link-list.home-link-list > div.ab-link-list-body > div > a").getall()
        
        # Iterate over models and form requests for next level
        for link in models:
            # Grab the text from the main page
            selector = scrapy.Selector(text=link)
            model = selector.css("a::text").get()
            
            # Form the request from the link and path in the anchor tag
            model_path = selector.css("a::attr(href)").get()
            url_req = response.url[:-1] + model_path
            
            # Pass it on to the next level
            meta = {
                "region": region, 
                "make": make,
                "model": model,
            }

            callback = self.parse_models

            yield scrapy.Request(url=url_req, callback=callback, meta=meta)

    def parse_models(self, response):
        # Get all the years for the given model page
        years = response.css("#root > div > div.cal-home-bottom.container > div.ab-link-list.home-link-list > div.ab-link-list-body > div > a").getall()

        # Iterate over all the years and form URL requests for the next level
        for y in years:
            # Grab the text from the frames page
            selector = scrapy.Selector(text=y)
            year = selector.css("a::text").get()

            # URL to the vehicle page
            year_path = selector.css("a::attr(href)").get()
            url_req = os.path.dirname(response.url[:-1]) + year_path
            
            # Pass on the meta object with new field
            meta = response.meta.copy()
            meta["year"] = year

            callback = self.parse_vehicles

            yield scrapy.Request(url=url_req, callback=callback, meta=meta)

    def parse_vehicles(self, response):
        # Get the main table on the page
        # This has 2 Door vs 4 Door
        tables = response.css(".vehicle-option > .list > div").getall()
        
        # Iterate over the tables for each body style
        for table in tables:
            # Get the vehicles in the table
            selector = scrapy.Selector(text=table)
            vehicles = selector.css("div > .content > .text").getall()

            # Iterate over all the vehicles and prepare the main Item
            for vehicle in vehicles:
                # The vehicle comes as "2 Door RSX (Type S) KA 6MT" and needs to be split up
                selector = scrapy.Selector(text=vehicle)
                vehicle_model = re.findall(r'\([^)]*\)|\S+', selector.css('.text > li > a::text').get())
                
                # Make the last item in the list the transmission code
                # Split up below
                transmission_code = vehicle_model[-1]
                
                # Trim is after the doors
                trim = vehicle_model[2].title() if any(vowel in vehicle_model[2].lower() for vowel in 'aeiou') else vehicle_model[2]
                
                # Variant is after the trim but has "()". Remove them
                variant = (vehicle_model[3][1:-1]).title() if '(' in vehicle_model[3] else ""
                
                # This is the KA part that is the destination origin
                area_code = vehicle_model[-2]
                
                # Finally get the vehicle path to scrape later
                vehicle_path = selector.css('.text > li > a::attr(href)').get()

                # Prepare the VehicleDataItem
                vehicle_data_item = VehicleDataItem()
                vehicle_data_item["region_display"] = response.meta["region"]
                vehicle_data_item["make_display"] = response.meta["make"]
                vehicle_data_item["model_display"] = response.meta["model"]
                vehicle_data_item["year"] = response.meta["year"]
                vehicle_data_item["doors"] = vehicle_model[0]
                
                # Parse out from "6MT"
                # Some are "AXT" and will place holder in speed to fix for later
                vehicle_data_item["transmission_code"] = transmission_code[1:]
                vehicle_data_item["transmission_auto"] = False if "MT" in vehicle_data_item["transmission_code"] else True
                vehicle_data_item["transmission_speeds"] = transmission_code[0]
                
                # Make the trim all caps if it doesn't have any vowels
                # LS vs Type R - Just a guess but we'll have to clean it up
                vehicle_data_item["trim_display"] = trim
                
                vehicle_data_item["variant_display"] = variant
                vehicle_data_item["area_code_display"] = area_code.upper()
                
                # Final URL for the vehicle to scrape later
                vehicle_data_item["vehicle_path"] = os.path.dirname(response.url[:-1]) + vehicle_path
                
                # Pass empty to make looping easier for the sql template in DatabaseManager
                vehicle_data_item["options"] = list()
                
                yield vehicle_data_item
