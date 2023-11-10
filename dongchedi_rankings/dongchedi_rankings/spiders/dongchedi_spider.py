import scrapy
from selenium import webdriver
from dongchedi_rankings.items import DongchediRankingItem
import time

class DongchediSpider(scrapy.Spider):
    name = 'dongchedi_spider'
    start_urls = ['https://www.dongchedi.com/sales']

    def __init__(self, *args, **kwargs):
        # 初始化Selenium WebDriver
        self.driver = webdriver.Chrome()
        super(DongchediSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        # 使用Selenium控制浏览器打开初始URL
        self.driver.get(response.url)
        
        # 获取初始页面的滚动高度
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # 模拟滚动页面以触发更多内容加载
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # 等待加载完成，可以根据网速适当调整

            # 获取新的滚动高度
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            # 如果滚动高度不再增加，说明已经滑到了页面底部
            if new_height == last_height:
                
                # 获取更新后的页面源代码
                updated_html = self.driver.page_source
                updated_response = scrapy.http.HtmlResponse(url=self.driver.current_url, body=updated_html, encoding='utf-8')
        
                # 提取数据
                car_list = updated_response.xpath('//*[@id="__next"]/div[1]/div[2]/div/div[4]/div/div/ol/li')
                for car in car_list:
                    car_name = car.xpath('./div[3]/div[1]/a/text()').get()
                    car_price = car.xpath('./div[3]/p/text()').get()
                    car_image = car.xpath('./div[2]/div/div/img/@src').get()
                    sales_trend = car.xpath('./div[4]/div/p/text()').get()

                    item = DongchediRankingItem()
                    item['CarName'] = car_name.strip()
                    item['PriceRange'] = car_price.strip()
                    item['CarImage'] = 'https:' + car_image.strip()
                    item['SalesTrend'] = sales_trend.strip()

                    yield item

                # 跳出循环，结束爬取
                break

            # 更新滚动高度，准备下一次判断
            last_height = new_height  

        # 完成后关闭浏览器
        self.driver.quit()
