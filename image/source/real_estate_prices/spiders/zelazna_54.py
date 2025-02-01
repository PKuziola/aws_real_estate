import scrapy
import json
from datetime import date

from ..items import RealEstatePricesItem
from scrapy.loader import ItemLoader

class Zelazna54Spider(scrapy.Spider):
    name = "zelazna_54"
    allowed_domains = ["matexipolska.pl/"]
    start_urls = ["https://matexipolska.pl/page-data/en/warszawa/zelazna-54/page-data.json"]

    def parse(self, response):
        json_data = json.loads(response.text)
        content = json_data['result']['data']['allFlats']['nodes']
        
        for n in content:
            loader = ItemLoader(item=RealEstatePricesItem())
            
            loader.add_value('date', date.today())
            loader.add_value('flat_name', n['name'])            
            loader.add_value('flat_area', n['area'])
            loader.add_value('flat_rooms', n['rooms'])
            loader.add_value('flat_floor', n['floor'])
            loader.add_value('flat_price', n['price'])
            loader.add_value('flat_details_url', n['PNG'])
            loader.add_value('flat_available', 1 if n['status'] == '1' else 0)           
            loader.add_value('flat_price_per_sqm', round(n['price'] / float(n['area'].replace(',', '.')), 2))
            loader.add_value('investment_name', 'Żelazna 54')
            loader.add_value('investment_url', 'https://matexipolska.pl/warszawa/zelazna-54')
            loader.add_value('developer_name', 'MATEXI')
            loader.add_value('flat_promotion', n['pricePromotion'])    

            yield loader.load_item()
        