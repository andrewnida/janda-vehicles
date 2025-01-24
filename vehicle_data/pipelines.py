# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from database.DatabaseManager import DatabaseManager

class VehicleDataPipeline:
    def __init__(self):
        self.databaseManager = DatabaseManager()

    def process_item(self, item, spider):
        database = getattr(spider, 'database', None)
        self.databaseManager.set_database(database)
        self.databaseManager.insert_vehicle(item)

        return item

    def close_spider(self, spider):
        self.databaseManager.dispose()