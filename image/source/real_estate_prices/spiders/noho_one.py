import scrapy
import json
from datetime import date
from bs4 import BeautifulSoup
from ..items import RealEstatePricesItem
from scrapy.loader import ItemLoader


class NohoOneSpider(scrapy.Spider):
    name = "noho_one"
    allowed_domains = ["https://noho-one.com/"]
    start_urls = [
        "https://api.resimo.pl/api/track/v1/allinone/client/46/investment/660/apartments/?token=SU5fT05FXzE6WXNsYWJfYWxs&building_list=A%3BB%3BC&additional_fields=apartment_id,additional_elements,price_per_square_meter,promotion_price_per_square_meter"
    ]

    def parse(self, response):
        apartment_data = json.loads(response.text)

        for building in apartment_data:
            for apartment in building["apartments"]:
                loader = ItemLoader(item=RealEstatePricesItem())

                loader.add_value("date", date.today())

                loader.add_value("flat_name", apartment["name"])
                loader.add_value(
                    "flat_area", float(apartment["area"].replace(",", "."))
                )
                loader.add_value("flat_rooms", str(apartment["rooms"]))
                loader.add_value("flat_floor", str(apartment["floor"]))
                loader.add_value(
                    "flat_details_url",
                    f"https://jeff.cdn.resimo.io/jeffv4/Noho/One/PDF/{apartment['name']}.PDF",
                )
                loader.add_value(
                    "flat_available", 1 if apartment["status"] == "available" else 0
                )
                loader.add_value("investment_name", "NOHO ONE")
                loader.add_value("investment_url", "https://noho-one.com/")
                loader.add_value("developer_name", "NOHO Investment")

                promo_price = apartment.get("promotionPrice")
                regular_price = float(apartment["price"])

                if promo_price is not None:
                    loader.add_value(
                        "flat_price", float(str(promo_price).replace(",", "."))
                    )
                    loader.add_value(
                        "flat_price_per_sqm",
                        float(
                            str(apartment["promotionPricePerSquareMeter"]).replace(
                                ",", "."
                            )
                        ),
                    )
                    loader.add_value("flat_promotion", 1)
                elif regular_price > 0:
                    loader.add_value(
                        "flat_price", float(str(apartment["price"]).replace(",", "."))
                    )
                    loader.add_value(
                        "flat_price_per_sqm",
                        float(str(apartment["pricePerSquareMeter"]).replace(",", ".")),
                    )
                    loader.add_value("flat_promotion", 0)
                elif apartment["status"] != "available":
                    loader.add_value("flat_price", None)
                    loader.add_value("flat_price_per_sqm", None)
                    loader.add_value("flat_promotion", None)

                yield loader.load_item()
