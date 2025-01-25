# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# Used as a general purpose item for both JDM and USDM
# Not all are used for each but thse are the only two types
class VehicleDataItem(scrapy.Item):
    region_display = scrapy.Field()
    region_uri = scrapy.Field()
    make_display = scrapy.Field()
    make_uri = scrapy.Field()
    model_display = scrapy.Field()
    model_uri = scrapy.Field()
    frame_display = scrapy.Field()      # JDM
    frame_uri = scrapy.Field()          # JDM
    chasiss_display = scrapy.Field()    # JDM
    chasiss_uri = scrapy.Field()        # JDM
    year = scrapy.Field()               # USDM
    frame_num_from = scrapy.Field()     # JDM
    frame_num_to = scrapy.Field()       # JDM
    doors = scrapy.Field()
    transmission_code = scrapy.Field()
    transmission_speeds = scrapy.Field()
    transmission_auto = scrapy.Field()
    trim_display = scrapy.Field()
    trim_uri = scrapy.Field()
    variant_display = scrapy.Field()    # USDM
    variant_uri = scrapy.Field()        # USDM
    area_code_display = scrapy.Field()  # USDM
    area_code_uri = scrapy.Field()      # USDM
    vehicle_path = scrapy.Field()
    options = scrapy.Field()            # JDM
    option_display = scrapy.Field()     # Used for loop as current option in sql template
    option_uri = scrapy.Field()         # Same
    pass
