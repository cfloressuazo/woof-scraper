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

        selector = scrapy_selector.xpath('//div[@class="product_name"]')
        for idx, product_xpath in enumerate(selector):
            loader = ItemLoader(item=ProductItem(), selector=product_xpath)
            product_url = product_xpath.xpath('.//a/@href').get()
            loader.add_xpath('product_url', './/a/@href')
            loader.add_xpath('product_name', './/a/text()')

            yield scrapy.Request(
                url=product_url,
                callback=self.parse_product,
                meta={'item': loader.load_item()}
            )

    def parse_product(self, response):
        selector = response.selector.xpath('//section[@id="main"]/div[@class="row"]')
        loader = ItemLoader(item=response.meta["item"], selector=selector)

        loader.add_xpath('detail_name', './/h4[@class="name_detail"]/text()')
        loader.add_xpath('brand', './/div[@class="product_manufacturer->name"]/text()')

        loader.add_xpath(
            'description',
            './/div[@class="product-description-short-detail" and '
            '@itemprop="description"]/p/descendant-or-self::*/text() '
        )

        _loader = loader.nested_xpath('//select[@id="group_1"]/option')
        _loader.add_xpath('size_format', './/text()')

        # loader.add_xpath('price', './/span[@itemprop="price"]/text()')

        loader.selector = response.selector.xpath(
            '//div[@class="tabs"]/div[@class="tab-content" and @id="tab-content"]'
        )
        loader.add_xpath(
            'detail_description',
            './/div[@class="elementor-accordion-content elementor-clearfix" and '
            '@data-section="1"]/ol/descendant-or-self::*/text()'
        )
        loader.add_xpath(
            'detail_ingredients',
            './/div[@class="elementor-accordion-content elementor-clearfix" and @data-section="2"]/p/text()'
        )
        loader.add_xpath(
            'nutritional_facts',
            './/div[@class="elementor-accordion-content elementor-clearfix" and '
            '@data-section="3"]/descendant-or-self::*/text()'
        )

        # loader.add_xpath('nutritional_facts_img_url', './/*[@id="collapseThree"]/div/p/img/@src')

        loader.add_xpath(
            'feed_guide',
            './/div[@class="elementor-accordion-content elementor-clearfix" and '
            '@data-section="4"]/p/descendant-or-self::*/text()')

        loader.add_xpath(
            'feed_guide_img_url',
            './/div[@class="elementor-accordion-content elementor-clearfix" and @data-section="4"]//img/@src')

        loader.add_xpath('extra_information_keys','.//dl[@class="data-sheet"]/dt[@class="name"]/text()')
        loader.add_xpath('extra_information_values','.//dl[@class="data-sheet"]/dd[@class="value"]/text()')

        self.log(f'finished parsing product page {response.url}')

        return loader.load_item()
