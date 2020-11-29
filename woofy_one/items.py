# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from itemloaders.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags


def remove_whitespace(value):
    return value.strip()


class ProductItem(scrapy.Item):
    """
        product_items = {
            "product_url": "product_url",
            "product_name": "product_name",
            "product_description": "product_description",
            "product_meta": [
                {"price": 1000, "size_format": "10 kg", "discount": 0.15},
                {"price": 500, "size_format": "5 kg"}
            ]
        }
    """
    product_url = scrapy.Field(
        output_processor=TakeFirst()
    )
    product_name = scrapy.Field(
        output_processor=Join()
    )
    # product_description = scrapy.Field()
    detail_name = scrapy.Field(output_processor=Join())
    brand = scrapy.Field(output_processor=Join())
    price = scrapy.Field()
    description = scrapy.Field(
        input_processor=MapCompose(remove_whitespace),
        output_processor=Join()
    )
    size_format = scrapy.Field()
    discount_percent = scrapy.Field()
    detail_description = scrapy.Field(
        input_processor=MapCompose(remove_whitespace),
        output_processor=Join()
    )
    detail_ingredients = scrapy.Field(
        input_processor=MapCompose(remove_whitespace),
        output_processor=Join()
    )

    nutritional_facts = scrapy.Field()
    nutritional_facts_img_url = scrapy.Field()

    customer_review_header = scrapy.Field(
        input_processor=MapCompose(remove_whitespace),
    )
    customer_review_rating = scrapy.Field()
    customer_review = scrapy.Field(
        input_processor=MapCompose(remove_whitespace),
    )



class ProductItemMeta(scrapy.Item):
    detail_name = scrapy.Field(output_processor=Join())
    brand = scrapy.Field(output_processor=Join())
    description = scrapy.Field(
        input_processor=MapCompose(remove_whitespace),
        output_processor=Join()
    )
    # options = scrapy.Field(serializer=list)
    price = scrapy.Field()
    size_format = scrapy.Field(serializer=str)
    discount_percent = scrapy.Field(serializer=str)

