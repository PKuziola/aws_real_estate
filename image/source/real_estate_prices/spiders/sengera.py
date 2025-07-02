import scrapy
import json
from datetime import date
from bs4 import BeautifulSoup
from ..items import RealEstatePricesItem
from scrapy.loader import ItemLoader


class SengeraSpider(scrapy.Spider):
    name = "sengera"
    allowed_domains = ["https://marvipol.pl/sengera-1/"]
    start_urls = ["https://ehomer.pl/api/v4/get-flats/205?lang=pl"]

    def parse(self, response):
        json_data = json.loads(response.text)

        for apartment in json_data["items"]:
            loader = ItemLoader(item=RealEstatePricesItem())

            loader.add_value("date", date.today())
            loader.add_value("flat_name", apartment["id"])
            loader.add_value("flat_area", apartment["area"])
            loader.add_value("flat_rooms", str(apartment["num_rooms"]))
            loader.add_value("flat_floor", str(apartment["floor"]))

            loader.add_value(
                "flat_price",
                (
                    float(apartment["price"])
                    if apartment["promo_price"] is None
                    else float(apartment["promo_price"])
                ),
            )

            loader.add_value(
                "flat_available",
                1 if apartment["availability"] == "available" else 0,
            )

            loader.add_value(
                "flat_price_per_sqm",
                (
                    float(apartment["price_sqm"])
                    if apartment["promo_price"] is None
                    else float(apartment["price"]) / float(apartment["area"])
                ),
            )

            loader.add_value("investment_name", "Sengera")
            loader.add_value("investment_url", "https://marvipol.pl/sengera-1/")
            loader.add_value("flat_details_url", str(apartment["pdf"]))
            loader.add_value("developer_name", "Marvipol")
            loader.add_value(
                "flat_promotion", 1 if apartment["promo_price"] is not None else 0
            )

            yield loader.load_item()
