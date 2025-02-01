import scrapy
import json
from datetime import date
from bs4 import BeautifulSoup
from ..items import RealEstatePricesItem
from scrapy.loader import ItemLoader


class StacjaWolaSpider(scrapy.Spider):
    name = "stacja_wola"
    allowed_domains = ["stacjawola.archicom.pl/"]
    start_urls = ["https://api.resimo.pl/api/track/v1/allinone/client/18/investment/558/apartments/?token=SU5fT05FXzE6WXNsYWJfYWxs&building_list=B3&additional_fields=symbol,promotion_start,promotion_end,additional_elements,files,show_price"] 

  
    def parse(self, response):
        json_data = json.loads(response.text)
        apartment_data = json_data[0]["apartments"]

        for apartment in apartment_data:
            loader = ItemLoader(item=RealEstatePricesItem())
            
            loader.add_value('date', date.today())
            loader.add_value('flat_name', apartment['name'])            
            loader.add_value('flat_area', apartment['area'])
            loader.add_value('flat_rooms', str(apartment['rooms']))
            loader.add_value('flat_floor', str(apartment['floor']))
            loader.add_value('flat_price', float(apartment['promotionPrice']) if apartment['promotionPrice'] is not None else float(apartment['price']))
            loader.add_value('flat_details_url', apartment['files'][2]['url'])
            loader.add_value('flat_available', 1 if apartment['status'] == 'available' else 0)           
            loader.add_value('flat_price_per_sqm', round(float(apartment['promotionPrice']) / float(apartment['area']), 2) if apartment['promotionPrice'] is not None else round(float(apartment['price']) / float(apartment['area']), 2))            
            loader.add_value('investment_name', 'Stacja Wola')
            loader.add_value('investment_url', 'https://stacjawola.archicom.pl/')
            loader.add_value('developer_name', 'Archicom')
            loader.add_value('flat_promotion', 0 if apartment['promotionStart'] is None else 1)    

            yield loader.load_item()


