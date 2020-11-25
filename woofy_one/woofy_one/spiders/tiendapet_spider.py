
import scrapy
from woofy_one.items import ProductItem, ProductItemMeta


class WoofyOneSpider(scrapy.Spider):
    name = "tiendapet"
    start_urls = [
        'https://www.tiendapet.cl/catalogo/perro/alimentos/'
    ]

    def parse(self, response, **kwargs):

        products = response.xpath('//div[has-class("datos-producto")]')

        for index, product in enumerate(products):
            product_item = ProductItem()
            product_item_meta = ProductItemMeta()
            product_item["product_name"] = product.xpath(
                './/header/h5/text()'
            ).get()
            product_item["product_description"] = product.xpath(
                './/header/small/text()'
            ).get()

            product_meta = product.xpath('.//table[has-class("datos")]/tbody/tr')

            product_item_meta["price"] = product_meta.xpath('.//td[2]/text()').getall()
            product_item_meta["size_format"] = product_meta.xpath(
                'normalize-space(.//td[1]/text())'
            ).getall()
            product_item_meta["discount_percent"] = product_meta.xpath(
                './/span[has-class("tag-descuento")]/text()'
            ).getall()

            product_item["product_item_meta"] = product_item_meta

            yield product_item

