# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class WebcrawlerPipeline:
    def process_item(self, item, spider):
        return item

class MarkdownPipeline:
    def open_spider(self, spider):
        self.file = open('C:/Users/shaik/Desktop/Projects Workspace/WebCrawler/README.md', 'a', encoding='utf-8')
        # Write the table header if the file is new
        self.file.seek(0, 2)  # Move to the end of the file
        if self.file.tell() == 0:
            self.file.write("| Position | Company | Location | Job Type | Job Mode | Job Requisition ID | Years of Experience | Job Link |\n")
            self.file.write("| --- | --- | --- | --- | --- | --- | --- | --- |\n")

    def process_item(self, item, spider):
        # Log the item data for debugging
        print(f"Processing item: {item}")
        # Construct a Markdown table row from the item data
        row = f"| {item.get('position', '')} | {item.get('company', '')} | {item.get('location', '')} | {item.get('job_type', '')} | {item.get('job_mode', '')} | {item.get('job_requisition_id', '')} | {item.get('years_of_experience', '')} | [Job Link]({item.get('job_link', '')}) |\n"
        self.file.write(row)
        return item

    def close_spider(self, spider):
        self.file.close()
