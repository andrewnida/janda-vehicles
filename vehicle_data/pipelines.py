# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from database.DatabaseManager import DatabaseManager

# Pipeline gets the database argument that was forwarded by the spider
# Then it sets the database for the DatabaseMangaer instance to use later
# Then it tries to insert the vehicle that was just crawled through the DatabaseManager
class VehicleDataPipeline:
    def __init__(self):
        self.databaseManager = DatabaseManager()

    def process_item(self, item, spider):
        database = getattr(spider, 'database', None)
        self.databaseManager.set_database(database)
        self.databaseManager.insert_vehicle(item)

        return item

    # Make sure to clean up the DB connection
    def close_spider(self, spider):
        self.databaseManager.dispose()