import scrapy
import json
import re
from datetime import date
from ..items import RealEstatePricesItem
from scrapy.loader import ItemLoader


def strip_html(text):
    return re.sub(r'<[^>]+>', '', text).strip()

def parse_area(area_str):
    clean = strip_html(area_str)
    m = re.search(r'[\d,]+', clean)
    return m.group(0) if m else clean

def parse_floor(floor_str):
    clean = strip_html(floor_str)
    if clean.lower() == 'parter':
        return '0'
    m = re.match(r'^(\d+)', clean)
    return m.group(1) if m else clean

def parse_rooms(rooms_str):
    m = re.match(r'^(\d+)', rooms_str.strip())
    return m.group(1) if m else rooms_str

def parse_price(price_str):
    digits = re.sub(r'[^\d]', '', price_str)
    return float(digits) if digits else None


class MetroWilanowskaSpider(scrapy.Spider):
    name = "metro_wilanowska"
    custom_settings = {
        "DOWNLOAD_DELAY": 2,
        "CONCURRENT_REQUESTS": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "RETRY_HTTP_CODES": [403, 429, 500, 502, 503, 504],
        "RETRY_TIMES": 3,
    }
    page_url = "https://www.domd.pl/pl-pl/warszawa/lista-inwestycji/apartamenty-metro-wilanowska/wyniki-wyszukiwania-wilanowska?&city=warszawa&language=pl-pl&type=mk&viewType=list"
    api_url = "https://www.domd.pl/iapi/search/search?city=warszawa&language=pl-pl&type=mk&resultsFor=5e4f940d-1737-f111-b83b-0050560172af"

    def start_requests(self):
        yield scrapy.Request(self.page_url, callback=self.parse_page)

    def parse_page(self, _response):
        yield scrapy.Request(
            self.api_url,
            headers={
                "Referer": self.page_url,
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "application/json, text/plain, */*",
            },
            callback=self.parse,
        )

    def parse(self, response):
        data = json.loads(response.text)
        flats = data["investments"][0]["flats"]

        for flat in flats:
            if flat["type"] == "help" or flat["flat"] is None:
                continue

            area = parse_area(flat["area"])
            detail_url = "https://www.domd.pl" + flat["more"]["href"]

            yield scrapy.Request(
                detail_url,
                callback=self.parse_flat,
                cb_kwargs={
                    "flat_name": flat["flat"],
                    "area": area,
                    "rooms": parse_rooms(flat["rooms"]),
                    "floor": parse_floor(flat["floor"]),
                    "available": 0 if flat["not_actual"] else 1,
                    "detail_url": detail_url,
                    "is_promo": flat["price"]["isPromo"],
                },
            )

    def parse_flat(self, response, flat_name, area, rooms, floor, available, detail_url, is_promo):
        price_raw = response.css(".m-FlatCard__info-priceRight span::text").get()
        price_per_sqm_raw = response.css(".m-FlatCard__info-priceLeft span::text").get()

        price = parse_price(price_raw) if price_raw else None
        price_per_sqm = parse_price(price_per_sqm_raw) if price_per_sqm_raw else None

        loader = ItemLoader(item=RealEstatePricesItem())
        loader.add_value("date", date.today())
        loader.add_value("flat_name", flat_name)
        loader.add_value("flat_area", area)
        loader.add_value("flat_rooms", rooms)
        loader.add_value("flat_floor", floor)
        loader.add_value("flat_available", available)
        loader.add_value("flat_details_url", detail_url)
        loader.add_value("investment_name", "Metro Wilanowska")
        loader.add_value("investment_url", "https://www.domd.pl/pl-pl/warszawa/lista-inwestycji/apartamenty-metro-wilanowska")
        loader.add_value("developer_name", "Dom Development")
        loader.add_value("flat_price", price)
        loader.add_value("flat_price_per_sqm", price_per_sqm)
        loader.add_value("flat_promotion", 1 if is_promo else 0)

        yield loader.load_item()
