import scrapy
import json
from datetime import date
from ..items import RealEstatePricesItem
from scrapy.loader import ItemLoader

class Aleje138Spider(scrapy.Spider):
    name = "aleje_138"
    allowed_domains = ["www.marvipol.pl"]
    start_urls = ["https://ehomer.pl/api/v4/get-flats/284?lang=pl"]

    def parse(self, response):
        json_data = json.loads(response.text)
        for apartment in json_data["items"]:
            loader = ItemLoader(item=RealEstatePricesItem())

            loader.add_value("date", date.today())
            loader.add_value("flat_name", apartment["name"])
            loader.add_value("flat_area", float(apartment["area"]))
            loader.add_value("flat_rooms", str(apartment["num_rooms"]))
            loader.add_value("flat_floor", str(apartment["floor"]))
            loader.add_value(
                "flat_available", 1 if apartment["availability"] == "available" else 0
            )
            loader.add_value("investment_name", "Aleje 138")
            loader.add_value("investment_url", "https://marvipol.pl/aleje-138/")
            loader.add_value("developer_name", "Marvipol")
            loader.add_value("flat_details_url", apartment["floor_plans"][0]["url"])

            loader.add_value(
                "flat_price",
                (
                    apartment["promo_price"]
                    if apartment["promo_price"] is not None
                    else apartment["price"]
                ),
            )
            loader.add_value(
                "flat_promotion", 1 if apartment["promo_price"] is not None else 0
            )
            loader.add_value(
                "flat_price_per_sqm",
                (
                    round(apartment["promo_price"] / apartment["area"], 2)
                    if apartment["promo_price"] is not None
                    else round(apartment["price"] / apartment["area"], 2)
                ),
            )

            yield loader.load_item()
