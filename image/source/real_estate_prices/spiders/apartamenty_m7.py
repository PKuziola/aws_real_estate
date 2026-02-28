import scrapy
import json
from datetime import date
from bs4 import BeautifulSoup
from ..items import RealEstatePricesItem
from scrapy.loader import ItemLoader


class ApartamentyM7Spider(scrapy.Spider):
    name = "apartamenty_m7"
    allowed_domains = ["https://m7apartamenty.pl/apartamenty/"]
    start_urls = [
        "https://backend.quptos.sensevr.pl/api/0/investment/290/all_units?variants=false&show_hidden=true"
    ]

    def parse(self, response):
        apartment_data = json.loads(response.text)
        
        for apartment in apartment_data:
            # filter out other investments, eg. Apartamenty Gutenberga
            if apartment.get("stage_id") in [803, 804, 816]:
                loader = ItemLoader(item=RealEstatePricesItem())

                loader.add_value("date", date.today())
                loader.add_value("flat_name", apartment["display_name"])
                loader.add_value("flat_area", apartment["area"])
                loader.add_value("flat_rooms", str(apartment["room_count"]))
                loader.add_value("flat_floor", str(apartment["floor_number"]))
                loader.add_value(
                    "flat_available", 1 if apartment["sales_status"] == "free" else 0
                )
                loader.add_value("investment_name", "Apartamenty M7")
                loader.add_value("investment_url", "https://m7apartamenty.pl/")
                loader.add_value("developer_name", "Archicom")
                loader.add_value("flat_details_url", apartment["unitplan_url"])
                loader.add_value("flat_price", apartment["cost"])
                loader.add_value("flat_price_per_sqm", apartment["cost_per_unit_area"])
                loader.add_value(
                    "flat_promotion", 1 if apartment["promo"] == True else 0
                )

                yield loader.load_item()
