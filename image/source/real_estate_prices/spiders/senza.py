import scrapy
import json
from datetime import date
from bs4 import BeautifulSoup
from ..items import RealEstatePricesItem
from scrapy.loader import ItemLoader


class SenzaSpider(scrapy.Spider):
    name = "senza"
    allowed_domains = ["https://marvipol.pl/osiedle-senza/"]
    start_urls = ["https://marvipol.pl/feed_562.json"]

    def parse(self, response):
        json_data = json.loads(response.text)

        for apartment in json_data:
            loader = ItemLoader(item=RealEstatePricesItem())

            loader.add_value("date", date.today())
            loader.add_value("flat_name", apartment["Numer_produktu"])
            loader.add_value("flat_area", apartment["Powierzchnia"])
            loader.add_value("flat_rooms", str(apartment["Liczba_pokoi"]))
            loader.add_value("flat_floor", str(apartment["Pietro"]))
            loader.add_value(
                "flat_price",
                (
                    float(apartment["Promocja"])
                    if apartment["Promocja"] != ""
                    else float(apartment["Wartosc_brutto_tylko_lokal"])
                ),
            )
            loader.add_value(
                "flat_available",
                1 if apartment["ProductStatus"] == "DO_SPRZEDAZY" else 0,
            )
            loader.add_value(
                "flat_price_per_sqm", float(apartment["Cena_m2_brutto_tylko_lokal"])
            )
            loader.add_value("investment_name", "Osiedle Senza")
            loader.add_value("investment_url", "https://marvipol.pl/osiedle-senza/")
            loader.add_value("flat_details_url", "N/A")
            loader.add_value("developer_name", "Marvipol")
            loader.add_value("flat_promotion", 1 if apartment["Promocja"] != "" else 0)

            yield loader.load_item()
