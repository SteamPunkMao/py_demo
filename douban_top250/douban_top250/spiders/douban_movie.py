import scrapy
from douban_top250.items import DoubanTop250Item


class DoubanMovieSpider(scrapy.Spider):
    name = 'douban_movie'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        for movie in response.css('ol.grid_view li'):
            item = DoubanTop250Item()
            item['rank'] = movie.css('em::text').get()
            item['title'] = movie.css('.title::text').get()
            item['rating'] = movie.css('.rating_num::text').get()
            item['link'] = movie.css('a::attr(href)').get()
            yield item

        next_page = response.css('.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
