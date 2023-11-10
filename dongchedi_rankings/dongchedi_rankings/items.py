import scrapy

class DongchediRankingItem(scrapy.Item):
    CarName = scrapy.Field()
    PriceRange = scrapy.Field()
    CarImage = scrapy.Field()
    SalesTrend = scrapy.Field()
