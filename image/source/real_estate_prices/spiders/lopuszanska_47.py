import scrapy
import json
from datetime import date
from bs4 import BeautifulSoup
from ..items import RealEstatePricesItem
from scrapy.loader import ItemLoader


class Lopuszanska47Spider(scrapy.Spider):
    name = "lopuszanska_47"
    allowed_domains = ["https://www.sgi.pl/warszawa/lopuszanska-47/"]
    start_urls = ["https://api.resimo.pl/api/track/v1/allinone/client/80/investment/437/apartments/?token=SU5fT05FXzE6WXNsYWJfYWxs&building_list=A,B,C%3BD,E,F,G%3BH,I,J,K%3BL,M,N&additional_fields=web_url,status_text"]

    def parse(self, response):
        json_data = json.loads(response.text)
        apartment_data = sum([item["apartments"] for item in json_data], [])

        for apartment in apartment_data:
            loader = ItemLoader(item=RealEstatePricesItem())          

            loader.add_value('date', date.today())
            loader.add_value('flat_name', apartment['name'])            
            loader.add_value('flat_area', apartment['area'])
            loader.add_value('flat_rooms', str(apartment['rooms']))
            loader.add_value('flat_floor', str(apartment['floor']))                
            loader.add_value('flat_available', 1 if apartment['status'] == 'available' else 0)                                 
            loader.add_value('investment_name', 'Łopuszańska 47')
            loader.add_value('investment_url', 'https://www.sgi.pl/warszawa/lopuszanska-47/')
            loader.add_value('developer_name', 'SGI')
            loader.add_value("flat_details_url", apartment['webUrl'])

            if apartment['status']!='available':
                loader.add_value('flat_price', None)
                loader.add_value('flat_price_per_sqm', None)
                loader.add_value('flat_promotion', None)
                yield loader.load_item()
            else:
                loader.add_value('flat_price', float(apartment['promotionPrice']) if apartment['promotionPrice'] is not None else float(apartment['price']))
                loader.add_value('flat_price_per_sqm', round(float(apartment['promotionPrice']) / float(apartment['area']), 2) if apartment['promotionPrice'] is not None else round(float(apartment['price']) / float(apartment['area']), 2))
                loader.add_value('flat_promotion', 0 if apartment['promotionPrice'] is None else 1) 
                yield loader.load_item()     

