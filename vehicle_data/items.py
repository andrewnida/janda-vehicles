# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VehicleDataItem(scrapy.Item):
    region = scrapy.Field()
    make = scrapy.Field()
    make_path = scrapy.Field()
    model = scrapy.Field()
    model_path = scrapy.Field()
    vehicle_path = scrapy.Field()
    frame = scrapy.Field()
    frame_path = scrapy.Field()
    frame_num_from = scrapy.Field()
    frame_num_to = scrapy.Field()
    year = scrapy.Field()
    doors = scrapy.Field()
    transmission_code = scrapy.Field()
    trim = scrapy.Field()
    variant = scrapy.Field()
    area_code = scrapy.Field()
    options = scrapy.Field()
    pass
