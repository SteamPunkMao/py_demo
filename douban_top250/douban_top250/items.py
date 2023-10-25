import scrapy


class DoubanTop250Item(scrapy.Item):
    rank = scrapy.Field()
    title = scrapy.Field()
    rating = scrapy.Field()
    link = scrapy.Field()
