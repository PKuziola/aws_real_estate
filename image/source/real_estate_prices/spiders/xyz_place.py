import scrapy
import json
from datetime import date
from bs4 import BeautifulSoup
from ..items import RealEstatePricesItem
from scrapy.loader import ItemLoader

class XYZSpider(scrapy.Spider):
    name = "xyz_place"
    allowed_domains = ["https://matexipolska.pl/warszawa/xyz-place"]
    start_urls = ["https://api.resimo.pl/api/track/v1/allinone/client/12/investment/562/apartments/?token=SU5fT05FXzE6WXNsYWJfYWxs&building_list=30&additional_fields=pdf_url,show_price,additional_elements,type,symbol"] 

    def parse(self, response):
        json_data = json.loads(response.text)
        apartment_data = json_data[0]["apartments"]

        for apartment in apartment_data:
            if apartment['type'] == 'Flat / Apartment':
                loader = ItemLoader(item=RealEstatePricesItem())
                
                loader.add_value('date', date.today())
                loader.add_value('flat_name', apartment['name'])                
                loader.add_value('flat_area', apartment['area'])
                loader.add_value('flat_rooms', str(apartment['rooms']))
                loader.add_value('flat_floor', str(apartment['floor']))
                loader.add_value('flat_available', 1 if apartment['status'] == 'available' else 0)
                loader.add_value('investment_name', 'XYZ Place')
                loader.add_value('investment_url', 'https://matexipolska.pl/warszawa/xyz-place')
                loader.add_value('developer_name', 'MATEXI')
                loader.add_value("flat_details_url", apartment['pdfUrl'])

                if apartment['status'] == 'sold':
                    loader.add_value('flat_price', None)
                    loader.add_value('flat_price_per_sqm', None)
                    loader.add_value('flat_promotion', None)
                    yield loader.load_item()
                else:
                    price = float(apartment['promotionPrice']) if apartment['promotionPrice'] is not None else float(apartment['price'])
                    price_per_sqm = round(price / float(apartment['area']), 2)
                    promotion = 0 if apartment['promotionPrice'] is None else 1
                    loader.add_value('flat_price', price)
                    loader.add_value('flat_price_per_sqm', price_per_sqm)
                    loader.add_value('flat_promotion', promotion)
                    yield loader.load_item()