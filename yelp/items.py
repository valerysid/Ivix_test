import scrapy


class YelpItem(scrapy.Item):
    name = scrapy.Field()
    rating = scrapy.Field()
    number_of_reviews = scrapy.Field()
    url = scrapy.Field()
    site = scrapy.Field()
    reviews = scrapy.Field()
