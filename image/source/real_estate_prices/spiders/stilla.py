import scrapy
import requests
from datetime import date
from ..items import RealEstatePricesItem
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
import json

class StillaSpider(scrapy.Spider):
    name = "stilla"
    allowed_domains = ["https://mieszkaj.skanska.pl/nasze-projekty/stilla/"]
    start_urls = ["https://api.resimo.pl/api/track/v4/jeff/crm/client/42/investment/259/apartments?token=SkVGRjQ6WVNMQUIx&building_list=1&additional_fields="]

    def parse(self, response):
        json_data = json.loads(response.text)
        apartment_data = json_data[0]["apartments"]

        for apartment in apartment_data:
            
            loader = ItemLoader(item=RealEstatePricesItem()) 
            
            loader.add_value('date', date.today())
            loader.add_value('investment_name', 'Stilla')
            loader.add_value('developer_name', 'Skanska')
            loader.add_value('investment_url', 'https://mieszkaj.skanska.pl/nasze-projekty/stilla/')

            loader.add_value('flat_name', apartment['name'])
            loader.add_value('flat_area', apartment['area'])
            loader.add_value('flat_area', str(apartment['rooms']))
            loader.add_value('flat_area', str(apartment['floor']))
            loader.add_value('flat_details_url', apartment['webUrl'])
            loader.add_value('flat_available', 1 if apartment['status'] == 'available' else 0)
            loader.add_value('flat_promotion', 'N/A')
            loader.add_value('flat_price', float(apartment['price']))
            loader.add_value('flat_price_per_sqm', round(float(apartment['price'])/float(apartment['area']),2))

            yield loader.load_item()