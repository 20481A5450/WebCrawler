import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import logging
# class CustomSpider(CrawlSpider):
#     name = "crawler"
#     allowed_domains = ["takeofftalent.com"]
#     start_urls = ["https://www.takeofftalent.com/"]

#     rules = (
#         Rule(LinkExtractor(allow="2024/04")),
#     )

class JobSpider(scrapy.Spider):
    name = "job_spider"
    allowed_domains = ["takeofftalent.com"]
    start_urls = ["https://www.takeofftalent.com/"]

    def parse(self, response):
        # Find all links on the base URL
        links = response.css('a::attr(href)').getall()
        
        # Filter links that point to job detail pages
        for link in links:
            if "2024/04" in link and link.endswith(".html"):
                # Follow each job listing link
                yield response.follow(link, callback=self.parse_job_details)

    def parse_job_details(self, response):
        # Initialize a dictionary to hold job details
        job_details = {}

        # Scrape the required information from the job detail page using CSS or XPath selectors
        job_details['position'] = response.xpath('//h3[contains(text(), "Position:")]/text()').get().replace('Position:', '')
        job_details['company'] = response.xpath('//h3[contains(text(), "Company:")]/text()').get().replace('Company:', '')
        job_details['location'] = response.xpath('//h3[contains(text(), "Location:")]/text()').get().replace('Location:', '')
        job_details['job_type'] = response.xpath('//h3[contains(text(), "Job type:")]/text()').get().replace('Job type:', '')
        job_details['job_mode'] = response.xpath('//h3[contains(text(), "Job mode:")]/text()').get().replace('Job mode:', '')
        job_details['job_id'] = response.xpath('//h3[contains(text(), "Job requisition id:")]/text()').get().replace('Job requisition id:', '')
        job_details['years_of_experience'] = response.xpath('//h3[contains(text(), "Years of experience:")]/text()').get().replace('Years of experience:', '')
        job_details['job_link'] = response.xpath('//*[@id="overlay-content"]/p[2]/a/@href').get().replace('Job requisition id:', '')


        # Print the job details to the console (for demonstration)
        print(f"Position: {job_details['position']}")
        print(f"Company: {job_details['company']}")
        print(f"Location: {job_details['location']}")
        print(f"Job Type: {job_details['job_type']}")
        print(f"Job Mode: {job_details['job_mode']}")
        print(f"Job ID: {job_details['job_id']}")
        print(f"Years of Experience: {job_details['years_of_experience']}")
        print(f"Job Link: {job_details['job_link']}")

        print("\n") # Adds a blank line for readability
        # File path
        fp = "C:/Users/shaik/Desktop/Projects Workspace/WebCrawler/README.md"

        # Open the file in append mode
        try:
            with open(fp, 'a') as file:
                # Write job details to file
                data_row = (f"| {job_details['position']} | {job_details['company']} | {job_details['location']} | "
                        f"{job_details['job_type']} | {job_details['job_mode']} | "
                        f"{job_details['job_id']} | {job_details['years_of_experience']} | {job_details['job_link']} |")
                file.write(data_row + "\n")
        except Exception as e:
            logging.error(f"Error writing to file: {e}")

        # Yield job details for further processing
        yield job_details