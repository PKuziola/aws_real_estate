import scrapy
import json
from datetime import date
from bs4 import BeautifulSoup
from ..items import RealEstatePricesItem
from scrapy.loader import ItemLoader

class OsiedlePoematuSpider(scrapy.Spider):
    name = "osiedle_poematu"
    allowed_domains = ["https://osiedlepoematu.pl"]
    start_urls = ["https://osiedlepoematu.pl/mieszkania-sprites-3d-dane.json"]

    def parse(self, response):
        json_data = json.loads(response.text)
        print(json_data)

        for stage in json_data["flats"]["flats"]["stages"]:
            # we take only stage II and III
            if (stage["id"] == 382 and stage["name"] == "Etap II") or (
                stage["id"] == 416 and stage["name"] == "Etap III"
            ):
                
                for building in stage["buildings"]:

                    for floor in building["floors"]:
                        floor_number = floor["n"]
                        for flat in floor["flats"]: 
                            loader = ItemLoader(item=RealEstatePricesItem())

                            loader.add_value("date", date.today())
                            loader.add_value("flat_name", flat["name"])
                            loader.add_value("flat_floor", floor_number)
                            loader.add_value("flat_details_url", "NA")
                            loader.add_value("investment_name", "Osiedle Poematu")
                            loader.add_value("developer_name", "ATAL")
                            loader.add_value(
                                "investment_url", "https://osiedlepoematu.pl"
                            )

                            if flat["slugStatus"] == "sold":
                                loader.add_value("flat_available", 0)
                            else:
                                loader.add_value(
                                    "flat_available",
                                    1 if flat["slugStatus"] == "free" else 0,
                                )
                                loader.add_value("flat_area", flat["ar"])
                                loader.add_value("flat_rooms", flat["ro"])

                            if flat.get("promotionFlat"):
                                if flat.get("price_promotion"):
                                    loader.add_value("flat_promotion", 1)
                                    loader.add_value(
                                        "flat_price_per_sqm",
                                        flat["price_per_square_meter_promotion"][
                                            "brutto"
                                        ],
                                    )
                                    loader.add_value(
                                        "flat_price", flat["price_promotion"]["brutto"]
                                    )
                            elif flat.get("price_standard"):
                                loader.add_value(
                                    "flat_price_per_sqm",
                                    flat["price_per_square_meter"]["brutto"],
                                )
                                loader.add_value(
                                    "flat_price", flat["price_standard"]["brutto"]
                                )
                                loader.add_value("flat_promotion", 0)

                            yield loader.load_item()