# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VehicleDataItem(scrapy.Item):
    region_display = scrapy.Field()
    region_uri = scrapy.Field()
    make_display = scrapy.Field()
    make_uri = scrapy.Field()
    make_path = scrapy.Field()
    model_display = scrapy.Field()
    model_uri = scrapy.Field()
    model_path = scrapy.Field()
    frame_display = scrapy.Field()
    frame_uri = scrapy.Field()
    frame_path = scrapy.Field()
    frame_num_from = scrapy.Field()
    frame_num_to = scrapy.Field()
    year = scrapy.Field()
    doors = scrapy.Field()
    transmission_code = scrapy.Field()
    transmission_speeds = scrapy.Field()
    transmission_auto = scrapy.Field()
    trim_display = scrapy.Field()
    trim_uri = scrapy.Field()
    variant_display = scrapy.Field()
    variant_uri = scrapy.Field()
    vehicle_path = scrapy.Field()
    # vehicle_area_code = scrapy.Field()
    options = scrapy.Field()
    option_display = scrapy.Field()
    option_uri = scrapy.Field()
    pass
