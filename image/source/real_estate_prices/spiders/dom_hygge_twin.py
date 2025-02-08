import scrapy
import requests
from datetime import date
from ..items import RealEstatePricesItem
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup

class DomHyggeTwinSpider(scrapy.Spider):
    """Scrapy spider for scraping apartment listings from Dom Hygge Twin."""
    
    name = "dom_hygge_twin"
    start_urls = ["https://hyggemokotow.pl/apartamenty/"]
    url_prefix = "https://hyggemokotow.pl/apartamenty/page/"
    page = 1

    def parse(self, response):
        """Parse the current page and schedule the next page if listings exist."""
        yield from self.parse_page(response)

        # Generate the next page URL
        next_page_url = f"{self.url_prefix}{self.page}/"

        # Proceed only if there are listings on the page
        if response.xpath("//div[contains(@class, 'search-list__item')]"):
            self.page += 1
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_page(self, response):
        """Extract apartment details from the page."""
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Locate the container with apartment listings
        apartments_list = soup.select_one(
            "body > div.search-list > div > div.search-list__left > div.search-list__list"
        )

        if not apartments_list:
            return

        apartments = apartments_list.find_all("div", class_="search-list__item")

        for item in apartments:
            loader = ItemLoader(item=RealEstatePricesItem())

            # Add static values
            loader.add_value("date", date.today())
            loader.add_value("investment_name", "Dom Hygge Twin")
            loader.add_value("investment_url", "https://hyggemokotow.pl/")
            loader.add_value("developer_name", "Dynamic Development")

            # Extract apartment title
            title = item.find("div", class_="title")
            if title:
                loader.add_value("flat_name", title.find("strong").text.strip())

                # Check availability
                status_span = title.find("span", class_="status")
                status = status_span.text.strip() if status_span else None
                loader.add_value("flat_available", 1 if status == "Wolne" else 0)

            # Extract apartment details
            flat_details = item.find("div", class_="info")

            # Extract area
            area_row = flat_details.find("th", string=lambda text: text and "Powierzchnia" in text)
            if area_row:
                powierzchnia = (
                    area_row.find_next("td").text.strip().split()[0].replace(",", ".")
                )
                loader.add_value("flat_area", powierzchnia)
            else:
                powierzchnia = None
                loader.add_value("flat_area", None)

            # Extract floor
            floor_row = flat_details.find("th", string=lambda text: text and "Piętro" in text)
            floor = floor_row.find_next("td").text.strip() if floor_row else None
            loader.add_value("flat_floor", str(floor))

            # Extract rooms count
            rooms_row = flat_details.find("th", string=lambda text: text and "Pokoje" in text)
            rooms = rooms_row.find_next("td").text.strip() if rooms_row else None
            loader.add_value("flat_rooms", str(rooms))

            # Extract price
            price_details = item.find("div", class_="price")
            price = None

            if price_details:
                highlighted_price = price_details.find("span", style=True)
                if highlighted_price:
                    price = highlighted_price.text.strip()  # Discounted price
                    loader.add_value("flat_promotion", 1)
                else:
                    price = price_details.text.strip()  # Regular price
                    loader.add_value("flat_promotion", 0)

                try:
                    price = int(price.replace(" ", "").replace(",", ".").replace("ZŁ", ""))
                except ValueError:
                    price = None

            loader.add_value("flat_price", price)

            # Calculate price per square meter
            try:
                flat_price_per_sqm = round(price / float(powierzchnia), 2)
            except (TypeError, ValueError, ZeroDivisionError):
                flat_price_per_sqm = None

            loader.add_value("flat_price_per_sqm", flat_price_per_sqm)

            # Extract image URL
            flat_img = soup.select_one(".house-popup-slider img")
            flat_img_url = flat_img["src"] if flat_img else None
            loader.add_value("flat_details_url", flat_img_url)

            yield loader.load_item()

   

            
            




