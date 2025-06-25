import scrapy
import json
from datetime import date
from bs4 import BeautifulSoup
from ..items import RealEstatePricesItem
from scrapy.loader import ItemLoader


class HiMokotowSpider(scrapy.Spider):
    name = "hi_mokotow"
    allowed_domains = ["https://cordiapolska.pl/inwestycje/hi-mokotow/"]
    start_urls = ["https://api.resimo.pl/api/track/v4/jeff/crm/client/11/investment/388/apartments?token=SkVGRjQ6WVNMQUIx&building_list=HM_1_A%3BHM_1_B%3BHM_1_C&additional_fields=symbol,type,status_text,additional_elements,show_on_web"] 
 
    def parse(self, response):
        json_data = json.loads(response.text)
        apartment_data = json_data[0]["apartments"]

        for apartment in apartment_data:
            loader = ItemLoader(item=RealEstatePricesItem())            
            
            if apartment['type']=='Flat / Apartment':
                loader.add_value('date', date.today())
                loader.add_value('flat_name', apartment['name'])            
                loader.add_value('flat_area', apartment['area'])
                loader.add_value('flat_rooms', str(apartment['rooms']))
                loader.add_value('flat_floor', str(apartment['floor']))                
                loader.add_value('flat_available', 1 if apartment['status'] == 'available' else 0)                                 
                loader.add_value('investment_name', 'Hi Mokotów')
                loader.add_value('investment_url', 'https://cordiapolska.pl/inwestycje/hi-mokotow/')
                loader.add_value('developer_name', 'Cordia')
                loader.add_value("flat_details_url", apartment['webUrl'])
                loader.add_value('flat_price', None)
                loader.add_value('flat_price_per_sqm', None)
                loader.add_value('flat_promotion', None)
                yield loader.load_item()                

