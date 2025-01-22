from dotenv import load_dotenv
from lib.Janda import Janda
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
# from vehicle_info.spiders.quotes_spider import QuotesSpider

# Check that script is being run directly
if __name__ == "__main__":
    # Load .env file
    load_dotenv()
    
    # Create application instance
    app = Janda()

    # # Prompt the user for a database and create it if necessary
    # janda.select_database()

    # if janda.database:
    #     janda.create_vehicle_tables()

    # # Disconnect from database and clean up
    # janda.dispose()


    # process = CrawlerProcess(get_project_settings())

    # # Add spiders
    # process.crawl(QuotesSpider)

    # # Start spiders
    # process.start()