import os
import sys
from multiprocessing import Process
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def _run_spiders():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    for spider_name in process.spider_loader.list():
        process.crawl(spider_name)
    process.start()


def real_estate_scraper(event, _context):
    sys.path.append('/var/task')
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'source.real_estate_prices.settings'

    p = Process(target=_run_spiders)
    p.start()
    p.join()


if __name__ == "__main__":
    real_estate_scraper(None, None)
