import scrapy
import json
from datetime import date
from ..items import RealEstatePricesItem
from scrapy.loader import ItemLoader

class MurapolUrcitySpider(scrapy.Spider):
    name = "murapol_urcity"
    allowed_domains = ["murapol.pl/oferta/warszawa/murapol-urcity"]
    start_urls = ["https://murapol.pl/api/investments-apartments/structure/14381"]

    def parse(self, response):
        json_data = json.loads(response.text)
        apartment_data = json_data

        for apartment in apartment_data:
            if apartment['category']=='Lokal usługowy':
                pass
            else:
            
                loader = ItemLoader(item=RealEstatePricesItem())

                loader.add_value('date', date.today())
                loader.add_value('flat_name', apartment['sku'])
                loader.add_value('flat_area', apartment['area'])
                loader.add_value('flat_rooms', str(apartment['room']))
                loader.add_value('flat_floor', '0' if apartment['floor'] == 'Parter' else apartment['floor'].split()[1])             
                loader.add_value('flat_details_url', f"https://murapol.pl/{apartment['fileId']}")
                loader.add_value('flat_available', 1 if apartment['status'] == 2 else 0)          
                loader.add_value('investment_name', 'Murapol Urcity')
                loader.add_value('investment_url', 'https://murapol.pl/oferta/warszawa/murapol-urcity')
                loader.add_value('developer_name', 'Murapol')                 
                
                if apartment['currentPromoPriceM2'] < int(apartment['currentPriceM2']):
                    loader.add_value('flat_price', float(float(apartment['area'].replace(',', '.')) * apartment['currentPromoPriceM2']))
                    loader.add_value('flat_price_per_sqm', apartment['currentPromoPriceM2'])
                    loader.add_value('flat_promotion', 1)
                else:
                    loader.add_value('flat_price', float(float(apartment['area'].replace(',', '.')) * int(apartment['currentPriceM2'])))
                    loader.add_value('flat_price_per_sqm', int(apartment['currentPriceM2']))
                    loader.add_value('flat_promotion', 0)

                yield loader.load_item()
                