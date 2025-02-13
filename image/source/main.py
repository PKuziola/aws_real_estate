import os
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .real_estate_prices.spiders.kolej_na_19 import KolejNa19Spider 
from .real_estate_prices.spiders.modern_mokotow import ModernMokotowSpider 
from .real_estate_prices.spiders.stacja_wola import StacjaWolaSpider 
from .real_estate_prices.spiders.zelazna_54 import Zelazna54Spider
from .real_estate_prices.spiders.murapol_urcity import MurapolUrcitySpider
from .real_estate_prices.spiders.dom_hygge_twin import DomHyggeTwinSpider
from .real_estate_prices.spiders.oval_sky import OvalSkySpider
from .real_estate_prices.spiders.stilla import StillaSpider

def real_estate_scraper(event, contxt):
    
    sys.path.append('/var/task')
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'source.real_estate_prices.settings'
    
    process = CrawlerProcess(get_project_settings())

    process.crawl(KolejNa19Spider)
    process.crawl(ModernMokotowSpider)
    process.crawl(StacjaWolaSpider)
    process.crawl(Zelazna54Spider)
    process.crawl(MurapolUrcitySpider)
    process.crawl(DomHyggeTwinSpider)
    process.crawl(OvalSkySpider)
    process.crawl(StillaSpider)    

    process.start()
