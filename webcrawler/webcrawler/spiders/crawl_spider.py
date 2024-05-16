import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import logging
class CustomSpider(CrawlSpider):
    name = "crawler"
    allowed_domains = ["takeofftalent.com"]
    start_urls = ["https://www.takeofftalent.com/"]

    rules = (
        Rule(LinkExtractor(allow="2024/04")),
    )

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
        job_details = {}
        position = response.xpath('//h3[contains(text(), "Position:")]/text()').get()
        if position:
            job_details['position'] = position.replace('Position:', '').strip()
        else:
            job_details['position'] = ''

        # Company
        company = response.xpath('//h3[contains(text(), "Company:")]/text()').get()
        if company:
            job_details['company'] = company.replace('Company:', '').strip()
        else:
            job_details['company'] = ''

        # Location
        location = response.xpath('//h3[contains(text(), "Location:")]/text()').get()
        if location:
            job_details['location'] = location.replace('Location:', '').strip()
        else:
            job_details['location'] = ''

        # Job Type
        job_type = response.xpath('//h3[contains(text(), "Job type:")]/text()').get()
        if job_type:
            job_details['job_type'] = job_type.replace('Job type:', '').strip()
        else:
            job_details['job_type'] = ''

        # Job Mode
        job_mode = response.xpath('//h3[contains(text(), "Job mode:")]/text()').get()
        if job_mode:
            job_details['job_mode'] = job_mode.replace('Job mode:', '').strip()
        else:
            job_details['job_mode'] = ''

        # Job Requisition ID
        job_id = response.xpath('//h3[contains(text(), "Job requisition id:")]/text()').get()
        if job_id:
            job_details['job_id'] = job_id.replace('Job requisition id:', '').strip()
        else:
            job_details['job_id'] = ''

        # Years of Experience
        years_of_experience = response.xpath('//h3[contains(text(), "Years of experience:")]/text()').get()
        if years_of_experience:
            job_details['years_of_experience'] = years_of_experience.replace('Years of experience:', '').strip()
        else:
            job_details['years_of_experience'] = ''

        # Job Link
        job_link = response.xpath('//*[@id="overlay-content"]/p[2]/a/@href').get()
        if job_link:
            job_details['job_link'] = job_link.strip()
        else:
            job_details['job_link'] = ''

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