# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class ProductItem(scrapy.Item):
    """
        product_items = {
            "product_name": "product_name",
            "product_description": "product_description",
            "product_meta": [
                {"price": 1000, "size_format": "10 kg", "discount": 0.15},
                {"price": 500, "size_format": "5 kg"}
            ]
        }
    """
    product_name = scrapy.Field()
    product_description = scrapy.Field()
    product_item_meta = scrapy.Field()


class ProductItemMeta(ProductItem):
    price = scrapy.Field()
    size_format = scrapy.Field()
    discount_percent = scrapy.Field(serializer=str)

