import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib.parse import unquote
from yelp.items import YelpItem


class CrawlSpider(CrawlSpider):
    name = "yelp"
    allowed_domains = ["yelp.com"]

    def __init__(self, category, location, **kwargs):
        self.start_urls = [
            f"https://www.yelp.com/search?find_desc={category}&find_loc={location}"]
        super().__init__(**kwargs)

    rules = (
        Rule(LinkExtractor(restrict_css="[role='navigation']"), follow=True),
        Rule(LinkExtractor(restrict_css="h3 a"), callback="parse_item"),
    )

    def parse_item(self, response):
        item = YelpItem()
        item['name'] = response.css('h1::text').get()
        item['rating'] = response.css(
            "[class*='five-stars']::attr(aria-label)").re_first(r'\d+')
        item['number_of_reviews'] = response.css(
            "[class=' css-foyide']::text").re_first(r'\d+')
        item['url'] = response.url

        if site := response.xpath('//*[text()="Business website"]'):
            item['site'] = unquote(site.xpath(
                './../*/a/@href').re_first(r'url=(.*?)&'))

        reviews = response.css(
            '[aria-label="Recommended Reviews"] ul')[1].css('li')
        item['reviews'] = []
        for review in reviews[:5]:
            name, address, *_ = review.css('::text').getall()
            date = review.css('::text').re_first('\d+/\d+/\d+')

            item['reviews'].append(
                {'name': name, 'address': address, 'date': date})

        return item
