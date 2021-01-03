from time import sleep

import scrapy
from selenium import webdriver
from scrapy.loader import ItemLoader
from woofy_one.items import ProductItem


class BestforpetsSpiderSpider(scrapy.Spider):
    name = 'bestforpets'
    allowed_domains = ['bestforpets.cl']
    start_urls = ['https://bestforpets.cl/tienda/alimento-para-perros']

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.driver = webdriver.Chrome()

    def parse(self, response, **kwargs):
        self.driver.get('https://bestforpets.cl/tienda/alimento-para-perros')

        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            self.driver.execute_script(f"window.scrollTo(0, {new_height});")
            sleep(7)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            self.driver.execute_script(f"window.scrollTo({new_height}, {new_height - 1000});")
            last_height = new_height
            sleep(1.2)

        scrapy_selector = scrapy.selector.Selector(text=self.driver.page_source)

        selector = scrapy_selector.xpath('//*[@class="item col-xs-6 col-sm-6 col-md-4"]')
        for idx, product_xpath in enumerate(selector):
            loader = ItemLoader(item=ProductItem(), selector=product_xpath)
            product_url = product_xpath.xpath('.//div[@class="product-name" and @itemprop="name"]/a/@href')

            loader.add_xpath()
