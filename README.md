# Janda Parts Scraper

Janda Parts Scraper is a solution I made to gather data from diffrent websites to complile a comprehensive parts and vehicle catalogue for Janda cars. It aims to take Japnese and US variations and combine them into a single database which I need for a future project.

- **Python** CLI application
- Normalized **PostgreSQL** Databases
- **Scrapy** web scraping framework with which strategically minimizes network requsts
- First phase needed to store vehicles with details and links for further parts scraping

## Installation

Dependencies attached in the requirements.txt file. Virtual environment files are not included and can be used however needed.

```bash
pip install -r requirements.txt
```

Environment variables can be configured in an `.env` file using the following variables:

```bash
PG_USER='user'
PG_PASSWORD='password'
PG_HOST='xxx.xxx.xxx.xxx'
PG_DEFAULT_DB='postgres'
JDM_VEHICLE_DATA_URLS='https://www.website.com/'
USDM_VEHICLE_DATA_URLS='https://www.anotherone.com/,https://www.onemore.com/'
```

## How to use

Run the `setup.py` script to initialize the database. The program will prompt for a database name and will confirm overwriting for an existing database.
not included and can be used however needed.

```bash
python setup.py
```

Now, the Scrapy spiders can be called for each of the regional markets to scrape. The `jdm_vehicles_spider.py` and `usdm_vehicles_spider.py` are used for each country and can be called using Scrapy's CLI.

**Note**: The databased used in setup must be passed as an argument to Scrapy as `db=*database name*`. For example:

```bash
scrapy crawl JDMVehicles -a db=janda
```

## More info

Spiders can be run in parallel as inserts are used with transactions and guaranteed.

All identifying information to the websites and vehicles used have been removed for obvious reasons. Scraping sessions were limited in scope and spaced out at reasonable intervals.
