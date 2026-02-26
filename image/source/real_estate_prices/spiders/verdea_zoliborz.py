import scrapy
import json
from datetime import date
from ..items import RealEstatePricesItem
from scrapy.loader import ItemLoader


class VerdeaZoliborzSpider(scrapy.Spider):
    name = "verdea_zoliborz"
    allowed_domains = ["matexipolska.pl"]
    start_urls = [
        "https://matexipolska.pl/page-data/en/warszawa/verdea-zoliborz/page-data.json"
    ]

    def parse(self, response):
        json_data = json.loads(response.text)
        apartment_data = json_data["result"]["data"]["allFlats"]["nodes"]

        for apartment in apartment_data:
            loader = ItemLoader(item=RealEstatePricesItem())

            loader.add_value("date", date.today())
            loader.add_value("flat_name", apartment["name"])
            loader.add_value("flat_area", apartment["area"])
            loader.add_value("flat_rooms", apartment["rooms"])
            loader.add_value("flat_floor", apartment["floor"])
            loader.add_value("flat_details_url", apartment["PNG"])
            loader.add_value("flat_available", 1 if apartment["status"] == "1" else 0)
            loader.add_value(
                "flat_promotion", 1 if apartment["isPromotion"] == True else 0
            )
            loader.add_value("investment_name", "Verdea Żoliborz")
            loader.add_value(
                "investment_url", "https://matexipolska.pl/warszawa/verdea-zoliborz"
            )
            loader.add_value("developer_name", "MATEXI")

            if apartment["isPromotion"] == False:
                loader.add_value("flat_price", apartment["price"])
                loader.add_value(
                    "flat_price_per_sqm",
                    round(
                        apartment["price"] / float(apartment["area"].replace(",", ".")),
                        2,
                    ),
                )
            else:
                loader.add_value("flat_price", apartment["pricePromotion"])
                loader.add_value(
                    "flat_price_per_sqm",
                    round(
                        apartment["pricePromotion"]
                        / float(apartment["area"].replace(",", ".")),
                        2,
                    ),
                )

            yield loader.load_item()
