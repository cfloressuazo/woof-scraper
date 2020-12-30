import scrapy
from scrapy.loader import ItemLoader
from woofy_one.items import ProductItem


class QuotesSpider(scrapy.Spider):
    name = "bestforpets"
    allowed_domains = ['www.bestforpets.cl']
    start_urls = ['https://bestforpets.cl/tienda/alimento-para-perros']

    def parse(self, response, **kwargs):
        selector = response.selector.xpath('//div[@class="product_name"]')
        for idx, product_xpath in enumerate(selector):
            loader = ItemLoader(item=ProductItem(), selector=product_xpath)
            try:
                product_url = product_xpath.xpath('.//a/@href').get()
                loader.add_xpath('product_url', './/a/@href')
                loader.add_xpath('product_name', './/a/text()')

                yield scrapy.Request(
                    url=product_url,
                    callback=self.parse_product,
                    meta={'item': loader.load_item()}
                )

                # self.log('>>>>>>>>>>>>>>>>>>> BEGIN >>>>>>>>>>>>>>>>>>>')
                # self.log(loader.load_item())
                # self.log('>>>>>>>>>>>>>>>>>>> END >>>>>>>>>>>>>>>>>>>')
            except Exception as e:
                self.log(e)
