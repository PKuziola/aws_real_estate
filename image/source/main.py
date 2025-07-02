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
from .real_estate_prices.spiders.chmielna_duo import ChmielnaDuoSpider
from .real_estate_prices.spiders.park_skandynawia import ParkSkandynawiaSpider
from .real_estate_prices.spiders.sadyba_spot import SadybaSpotSpider
from .real_estate_prices.spiders.bukowinska_mokotow import BukowinskaMokotowSpider
from .real_estate_prices.spiders.hi_mokotow import HiMokotowSpider
from .real_estate_prices.spiders.lopuszanska_47 import Lopuszanska47Spider
from .real_estate_prices.spiders.senza import SenzaSpider
from .real_estate_prices.spiders.sengera import SengeraSpider  # Assuming SengeraSpider is defined in the same module

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
    process.crawl(ChmielnaDuoSpider)
    process.crawl(ParkSkandynawiaSpider) 
    process.crawl(SadybaSpotSpider)   
    process.crawl(BukowinskaMokotowSpider)
    process.crawl(HiMokotowSpider)
    process.crawl(Lopuszanska47Spider)
    process.crawl(SenzaSpider)  
    process.crawl(SengeraSpider)  # Assuming SengeraSpider is defined in the same module

    process.start()
