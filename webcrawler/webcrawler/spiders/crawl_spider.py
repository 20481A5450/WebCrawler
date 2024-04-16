import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

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
        job_details['position'] = response.xpath('//h3[contains(text(), "Position:")]/text()').get()
        job_details['company'] = response.xpath('//h3[contains(text(), "Company:")]/text()').get()
        job_details['location'] = response.xpath('//h3[contains(text(), "Location:")]/text()').get()
        job_details['job_type'] = response.xpath('//h3[contains(text(), "Job type:")]/text()').get()
        job_details['job_mode'] = response.xpath('//h3[contains(text(), "Job mode:")]/text()').get()
        job_details['job_id'] = response.xpath('//h3[contains(text(), "Job requisition id:")]/text()').get()
        job_details['years_of_experience'] = response.xpath('//h3[contains(text(), "Years of experience:")]/text()').get()

        # Print the job details to the console (for demonstration)
        print(f"Position: {job_details['position']}")
        print(f"Company: {job_details['company']}")
        print(f"Location: {job_details['location']}")
        print(f"Job Type: {job_details['job_type']}")
        print(f"Job Mode: {job_details['job_mode']}")
        print(f"Job ID: {job_details['job_id']}")
        print(f"Years of Experience: {job_details['years_of_experience']}")

        print("\n") # Adds a blank line for readability

        # Save the job details to a file (optional)
        with open('job_details.txt', 'a') as file:
            file.write(f"Position: {job_details['position']}\n")
            file.write(f"Company: {job_details['company']}\n")
            file.write(f"Location: {job_details['location']}\n")
            file.write(f"Job Type: {job_details['job_type']}\n")
            file.write(f"Job Mode: {job_details['job_mode']}\n")
            file.write(f"Job ID: {job_details['job_id']}\n")
            file.write(f"Years of Experience: {job_details['years_of_experience']}\n")
            file.write("\n")
        
        # Yield job details for further processing (optional)
        yield job_details
