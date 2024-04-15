import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class CustomSpider(CrawlSpider):
    name = "crawler"
    allowed_domains = ["takeofftalent.com"]
    start_urls = ["https://www.takeofftalent.com/"]

    rules = (
        Rule(LinkExtractor(allow="2024/04")),
    )
