import scrapy
import json
from datetime import date
from bs4 import BeautifulSoup
from ..items import RealEstatePricesItem
from scrapy.loader import ItemLoader


class RevolaSpider(scrapy.Spider):
    name = "revola"
    allowed_domains = ["https://revola.pl/"]
    start_urls = [
        "https://assets.3destate.cloud/assets/apps/karolkowa-53-abb4bc33-co-sm/r/latest/config.json"
    ]

    def parse(self, response):
        json_data = json.loads(response.text)

        apartments = json_data["data"]["config"]["units"]

        for apartment in apartments:
            if apartment["custom"]["type"] == "mieszkanie":
                loader = ItemLoader(item=RealEstatePricesItem())

                loader.add_value("date", date.today())
                loader.add_value("flat_name", apartment["name"])
                loader.add_value("flat_area", apartment["custom"]["area"])
                loader.add_value("flat_rooms", apartment["custom"]["rooms"])
                loader.add_value("flat_floor", apartment["custom"]["floor"])
                loader.add_value("investment_name", "ReVola")
                loader.add_value("investment_url", "https://revola.pl/")
                loader.add_value("flat_details_url", "N/A")
                loader.add_value("developer_name", "Alides")
                loader.add_value(
                    "flat_promotion", 1 if apartment["custom"]["isPromo"] else 0
                )
                loader.add_value(
                    "flat_available", 0 if apartment["custom"]["isNotAvailable"] else 1
                )
                loader.add_value(
                    "flat_price",
                    (
                        apartment["custom"]["priceOffer"]
                        if apartment["custom"]["isPromo"]
                        else apartment["custom"]["price"]
                    ),
                )
                loader.add_value(
                    "flat_price_per_sqm",
                    (
                        apartment["custom"]["priceOfferPerSqm"]
                        if apartment["custom"]["isPromo"]
                        else apartment["custom"]["priceNormalPerSqm"]
                    ),
                )

                yield loader.load_item()
