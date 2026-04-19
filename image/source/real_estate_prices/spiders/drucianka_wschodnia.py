import scrapy
import json
from datetime import date
from bs4 import BeautifulSoup
from ..items import RealEstatePricesItem
from scrapy.loader import ItemLoader


class DruciankaWschodniaSpider(scrapy.Spider):
    name = "drucianka_wschodnia"
    allowed_domains = ["www.sgi.pl", "api.resimo.pl"]
    start_urls = [
        "https://api.resimo.pl/api/track/v1/allinone/client/80/investment/765/apartments/?token=SU5fT05FXzE6WXNsYWJfYWxs"
    ]

    def parse(self, response):
        json_data = json.loads(response.text)
        for building in json_data:
            for apartment in building["apartments"]:
                loader = ItemLoader(item=RealEstatePricesItem())

                loader.add_value("date", date.today())
                loader.add_value("flat_name", apartment["name"])
                loader.add_value("flat_area", apartment["area"])
                loader.add_value("flat_rooms", str(apartment["rooms"]))
                loader.add_value("flat_floor", str(apartment["floor"]))
                loader.add_value(
                    "flat_available", 1 if apartment["status"] == "available" else 0
                )
                loader.add_value("investment_name", "Drucianka Wschodnia")
                loader.add_value(
                    "investment_url", "https://www.sgi.pl/warszawa/drucianka-wschodnia/"
                )
                loader.add_value("developer_name", "SGI")
                loader.add_value("flat_details_url", "N/A")

                if apartment["status"] != "available":
                    loader.add_value("flat_price", None)
                    loader.add_value("flat_price_per_sqm", None)
                    loader.add_value("flat_promotion", None)
                else:
                    loader.add_value(
                        "flat_price",
                        (
                            float(apartment["promotionPrice"])
                            if apartment["promotionPrice"] is not None
                            else float(apartment["price"])
                        ),
                    )
                    loader.add_value(
                        "flat_price_per_sqm",
                        (
                            round(
                                float(apartment["promotionPrice"])
                                / float(apartment["area"]),
                                2,
                            )
                            if apartment["promotionPrice"] is not None
                            else round(
                                float(apartment["price"]) / float(apartment["area"]), 2
                            )
                        ),
                    )
                    loader.add_value(
                        "flat_promotion",
                        0 if apartment["promotionPrice"] is None else 1,
                    )

                yield loader.load_item()
