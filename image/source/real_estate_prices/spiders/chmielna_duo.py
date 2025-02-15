import scrapy
import json
from datetime import date
from bs4 import BeautifulSoup
from ..items import RealEstatePricesItem
from scrapy.loader import ItemLoader


class ChmielnaDuoSpider(scrapy.Spider):
    name = "chmielna_duo"
    allowed_domains = ["https://chmielnaduo.pl/"]
    start_urls = [
        "https://3destatesmartmakietaemb.z6.web.core.windows.net/assets/8bdb9b74-419f-4e2e-b68f-4d8e6e7318e0/app.config.json"
    ]

    def parse(self, response):
        json_data = json.loads(response.text)
        apartment_data = json_data["flats"]

        for apartment in apartment_data:

            if apartment["hideFlat"] == True or apartment["availability"] == 3:
                pass
            else:
                loader = ItemLoader(item=RealEstatePricesItem())

                loader.add_value("date", date.today())
                loader.add_value("investment_name", "Chmielna Duo")
                loader.add_value("developer_name", "bpi")
                loader.add_value("investment_url", "https://chmielnaduo.pl/")

                loader.add_value("flat_name", apartment["name"])
                loader.add_value("flat_area", str(apartment["area"]))
                loader.add_value("flat_rooms", str(apartment["rooms"]))
                loader.add_value("flat_floor", str(apartment["floor"]))
                loader.add_value("flat_details_url", apartment["flatFile"])
                loader.add_value(
                    "flat_available", 1 if apartment["availability"] == 1 else 0
                )
                loader.add_value(
                    "flat_promotion", 1 if apartment["isPromo"] is True else 0
                )

                price = apartment.get("price")
                if price is not None:
                    loader.add_value("flat_price", float(apartment["price"]))
                    loader.add_value(
                        "flat_price_per_sqm",
                        round(float(apartment["price"]) / float(apartment["area"]), 2),
                    )

                yield loader.load_item()
