import scrapy
from scrapy.crawler import CrawlerProcess

from seeds import write_to_db


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "quotes.json", 'encoding': 'utf8'}
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response, *_):
        quote_path = response.xpath('/html//div[@class="quote"]')
        for quote in quote_path:
            name = quote.xpath('span/small/text()').get()
            if "é" in name:
                name = name.replace('é', 'e')
            yield {
                "tags": quote.xpath('div[@class="tags"]/a/text()').extract(),
                "author": name,
                "quote": quote.xpath('span[@class="text"]/text()').get()[1:-1]
            }
        next_link = response.xpath('//li[@class="next"]/a/@href').get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "authors.json", 'encoding': 'utf8'}
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response, *_):
        links = response.xpath('//span[2]/a/@href')
        for link in links:
            yield scrapy.Request(url=self.start_urls[0] + link.get())

        author_path = response.xpath('/html//div[@class="author-details"]')
        for info in author_path:
            name = info.xpath('h3[@class="author-title"]/text()').get().strip()
            if "é" in name:
                name = name.replace('é', 'e')
            yield {
                "fullname": name,
                "born_date": info.xpath('p/span[@class="author-born-date"]/text()').get().strip(),
                "born_location": info.xpath('p/span[@class="author-born-location"]/text()').get().strip(),
                "description": info.xpath('div[@class="author-description"]/text()').get().strip()
            }
        next_link = response.xpath('//li[@class="next"]/a/@href').get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.crawl(AuthorsSpider)
    process.start()
    # Write to MongoDB
    write_to_db()


