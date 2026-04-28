from datetime import date
import scrapy
import pandas as pd
import json
from bs4 import BeautifulSoup
from ..items import RealEstatePricesItem
from scrapy.loader import ItemLoader

def price_per_sqm_func(area = str,price = str):
    price = int(price.replace('.',''))    
    area = float(area.replace(',', '.'))
    if price > 0: 
        return round(price/area,2)
    else:
        return None               

class KolejNa19Spider(scrapy.Spider):
    name = "kolej_na_19"
    allowed_domains = ["kolejna19.pl"]
    start_urls = ["https://kolejna19.pl/wp-json/wp/v2/pages/101"]

    def parse(self, response):
                     
        json_data = response.json()
        content = json_data['content']['rendered']
        soup = BeautifulSoup(content, 'html.parser')        

        table_body = soup.find('tbody')
        
        if table_body:            
            rows = table_body.find_all('tr')
            for row in rows:                
                cells = row.find_all('td')
                temp_flat_details = [cell.get_text(strip=True) for cell in cells]                
                
                loader = ItemLoader(item=RealEstatePricesItem())
                loader.add_value('date', date.today())
                loader.add_value('flat_name', temp_flat_details[0]) 
                loader.add_value('flat_area', temp_flat_details[1])
                loader.add_value('flat_rooms', temp_flat_details[2])
                loader.add_value('flat_floor', temp_flat_details[3])                
                loader.add_value('flat_price', temp_flat_details[5])
                loader.add_value('flat_details_url', f'https://kolejna19.pl/karty/{temp_flat_details[0]}.pdf')
                loader.add_value('flat_available', 1 if temp_flat_details[7] == 'wolne' else 0)             
                loader.add_value('flat_price_per_sqm', price_per_sqm_func(temp_flat_details[1],temp_flat_details[5]))
                loader.add_value('investment_name', 'Kolej na 19')
                loader.add_value('investment_url', 'https://kolejna19.pl')
                loader.add_value('developer_name', 'Polski Holding Nieruchomości S.A.')
                loader.add_value('flat_promotion', 'N/A')               

                yield loader.load_item()
        
