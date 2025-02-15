import scrapy
import requests
from datetime import date
from ..items import RealEstatePricesItem
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
import json


class ParkSkandynawiaSpider(scrapy.Spider):
    name = "park_skandynawia"
    allowed_domains = ["https://mieszkaj.skanska.pl/nasze-projekty/park-skandynawia/"]
    start_urls = ["https://ehomer.pl/api/v4/get-flats/119?lang=pl"]

    def parse(self, response):
        json_data = json.loads(response.text)
        apartment_data = json_data["items"]

        for apartment in apartment_data:

            loader = ItemLoader(item=RealEstatePricesItem())

            loader.add_value("date", date.today())
            loader.add_value("investment_name", "Park Skandynawia")
            loader.add_value("developer_name", "Skanska")
            loader.add_value(
                "investment_url",
                "https://mieszkaj.skanska.pl/nasze-projekty/park-skandynawia/",
            )

            loader.add_value("flat_name", apartment["name"])
            loader.add_value("flat_area", str(apartment["area"]))
            loader.add_value("flat_rooms", str(apartment["num_rooms"]))
            loader.add_value("flat_floor", str(apartment["floor"]))
            loader.add_value("flat_details_url", apartment["pdf"])
            loader.add_value(
                "flat_available", 1 if apartment["availability"] == "available" else 0
            )
            loader.add_value("flat_price", apartment["price"])
            loader.add_value(
                "flat_price_per_sqm", round(apartment["price"] / apartment["area"], 2)
            )

            yield loader.load_item()
