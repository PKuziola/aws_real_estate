import scrapy
import requests
from datetime import date
from ..items import RealEstatePricesItem
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
import json

class OvalSkySpider(scrapy.Spider):
    name = "oval_sky"
    allowed_domains = ["https://dekpoldeweloper.pl/"]
    start_urls = ["https://assets.3destate.cloud/assets/apps/dekpol-oval-sky-52dbdd23-co-sm/r/1/config.json?t=1739476113896"]

    def parse(self, response):
        json_data = json.loads(response.text)
        apartment_data = json_data["data"]["config"]["units"]

        for apartment in apartment_data:
            
            if apartment['custom']['isHidden'] == True:
                continue

            loader = ItemLoader(item=RealEstatePricesItem())                   
                                                  
            loader.add_value('date', date.today())
            loader.add_value('investment_name', 'Oval Sky')
            loader.add_value('developer_name', 'Dekpol')
            loader.add_value('investment_url', 'https://dekpoldeweloper.pl/portfolio/ovalsky-warszawa-ul-pradzynskiego/?')

            loader.add_value('flat_name', apartment['name'])
            loader.add_value('flat_area', str(apartment['custom']['area']))
            loader.add_value('flat_rooms', str(apartment['custom']['rooms']))
            loader.add_value('flat_floor', str(apartment['custom']['floor']))
            loader.add_value('flat_promotion', 1 if apartment['custom']['isPromo'] is True else 0)
            loader.add_value('flat_details_url', apartment['custom']['flatFile'])
            loader.add_value('flat_available', 1 if apartment['custom']['status'] == 1 else 0)
            loader.add_value('flat_price_per_sqm', apartment['custom']['pricePerSqm'])
            loader.add_value('flat_price', apartment['custom']['pricePromo'] if apartment['custom']['isPromo'] is True else apartment['custom']['price']) 

            yield loader.load_item()
            