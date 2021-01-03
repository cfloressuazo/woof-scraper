import scrapy
from scrapy.loader import ItemLoader
from woofy_one.items import ProductItem
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class QuotesSpider(scrapy.Spider):
    name = "bestforpets"
    allowed_domains = ['bestforpets.cl']
    # start_urls = ['https://bestforpets.cl/tienda/alimento-para-perros']

    def start_requests(self):
        yield SeleniumRequest(
            url='https://bestforpets.cl/tienda/alimento-para-perros',
            callback=self.parse,
        )

    def parse(self, response, **kwargs):
        selector = response.selector.xpath('//div[@class="product_name"]')
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
