# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst
from datetime import datetime

def fix_price(value):
    if isinstance(value, int):
        return float(value)
    elif isinstance(value, float):
        return value
    return float(int(value.replace('.','')))

def convert_flat_area_float(value):
    return float(value.replace(',', '.'))

def adjust_flat_promotion(value):
    if value == 'N/A':
        return None
    return value 
    
class RealEstatePricesItem(scrapy.Item):
    date = scrapy.Field(output_processor = TakeFirst()) 
    flat_name = scrapy.Field(output_processor = TakeFirst())
    flat_area = scrapy.Field(
        input_processor = MapCompose(convert_flat_area_float),
        output_processor = TakeFirst()
    )
    flat_rooms = scrapy.Field(output_processor = TakeFirst())
    flat_floor = scrapy.Field(output_processor = TakeFirst())    
    flat_price = scrapy.Field(
        input_processor = MapCompose(fix_price),
        output_processor = TakeFirst()
    )
    flat_details_url = scrapy.Field(output_processor = TakeFirst())
    flat_available = scrapy.Field(output_processor = TakeFirst())
    flat_price_per_sqm = scrapy.Field(output_processor = TakeFirst())
    investment_name = scrapy.Field(output_processor = TakeFirst())
    investment_url = scrapy.Field(output_processor = TakeFirst())
    developer_name = scrapy.Field(output_processor = TakeFirst())
    flat_promotion = scrapy.Field(
        input_processor = MapCompose(adjust_flat_promotion),
        output_processor = TakeFirst()
    )  
