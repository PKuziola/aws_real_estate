import scrapy
import json
from datetime import date
from bs4 import BeautifulSoup
from ..items import RealEstatePricesItem
from scrapy.loader import ItemLoader


class SadybaSpotSpider(scrapy.Spider):
    name = "sadyba_spot"
    allowed_domains = ["https://sadybaspot.pl/"]
    start_urls = [
        "https://sadybaspot.pl/page-data/sq/d/1329188290.json"
    ]

    def parse(self, response):

        json_data = json.loads(response.text)
        apartment_data = json_data["data"]["wp"]["flats"]
      
        for apartment in apartment_data:
            if apartment["numberofrooms"] != None:
                loader = ItemLoader(item=RealEstatePricesItem())

                loader.add_value("date", date.today())
                loader.add_value("investment_name", "Sadyba Spot")
                loader.add_value("developer_name", "unidevelopment")
                loader.add_value("investment_url", "https://sadybaspot.pl/")

                loader.add_value("flat_name", apartment["name"])
                loader.add_value("flat_area", str(apartment["propertysize"]))
                loader.add_value("flat_rooms", str(apartment["numberofrooms"]))
                loader.add_value("flat_floor", str(apartment["floor"]))
                loader.add_value("flat_details_url", "N/A")
                loader.add_value(
                    "flat_available", 1 if apartment["status"] == "Wolne" else 0
                )
            
                if apartment["promotionpriceforapartment"] == 0:
                    loader.add_value("flat_price", apartment["priceforapartment"])
                    loader.add_value("flat_price_per_sqm", apartment["pricepersqm"])
                    loader.add_value("flat_promotion", 0)
                else:
                    loader.add_value("flat_price", apartment["promotionpriceforapartment"])
                    loader.add_value("flat_price_per_sqm", apartment["promotionpriceforapartment"]/apartment["propertysize"])
                    loader.add_value("flat_promotion", 1)

            yield loader.load_item()
