import os
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def real_estate_scraper(event, _context):
    sys.path.append('/var/task')
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'source.real_estate_prices.settings'

    settings = get_project_settings()
    process = CrawlerProcess(settings)

    for spider_name in process.spider_loader.list():
        process.crawl(spider_name)
        print('pies')

    process.start()