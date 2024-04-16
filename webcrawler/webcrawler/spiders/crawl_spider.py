import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class CustomSpider(CrawlSpider):
    name = "crawler"
    allowed_domains = ["takeofftalent.com"]
    start_urls = ["https://www.takeofftalent.com/"]

    rules = (
        Rule(LinkExtractor(allow="2024/04"), callback="parse"),
    )

    def parse(self, response):
        
        base_xpath = '/html/body/div[1]/div[2]/div/div/div/main/div/div[1]/div/article/div/div/div[3]/div[1]/div/div[1]/div/div'    
        # Extract the `h4` text within the specified XPath
        pos = response.xpath("//*[@id='post-body-1530227354656296947']/div/div[1]/div/div/h3[1]").get()
        com = response.xpath(f'{base_xpath}/h3[2]').get()
        loc = response.xpath(f'{base_xpath}/h3[3]').get()
        j_t = response.xpath(f'{base_xpath}/h3[4]').get()
        j_m = response.xpath(f'{base_xpath}/h3[5]').get()
        j_r = response.xpath(f'{base_xpath}/h3[6]').get()
        yoe = response.xpath(f'{base_xpath}/h3[7]').get()
        # Print the extracted h4 text for debugging
        print(f"Extracted position text: {pos}")
        print(f"Extracted company text: {com}")
        print(f"Extracted location text: {loc}")
        print(f"Extracted job type text: {j_t}")
        print(f"Extracted job mode text: {j_m}")
        print(f"Extracted job requisition id text: {j_r}")
        print(f"Extracted years of experience text: {yoe}")

        
        # You can yield the data as needed
        yield {
            'url': response.url,
            'Position': pos,
            'Company': com,
            'Location': loc,
            'Job Type': j_t,
            'Job Mode': j_m,
            'Job ID': j_r,
            'Years of Experience': yoe
            # Add any other data extractions here...
        }
