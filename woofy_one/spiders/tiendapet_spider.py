import scrapy
from scrapy.loader import ItemLoader
from woofy_one.items import ProductItem, ProductItemMeta


class WoofyOneSpider(scrapy.Spider):
    name = "tiendapet"
    allowed_domains = ['www.tiendapet.cl']
    start_urls = ['https://www.tiendapet.cl/catalogo/perro/alimentos/']

    def parse(self, response, **kwargs):
        selector = response.selector.xpath('//div[has-class("block-producto")]')
        for idx, product_xpath in enumerate(selector):
            loader = ItemLoader(item=ProductItem(), selector=product_xpath)
            product_url = product_xpath.xpath('.//a[has-class("catalogo_click_detail")]/@href').get()

            loader.add_xpath('product_url', './/a[has-class("catalogo_click_detail")]/@href')
            loader.add_xpath('product_name', './/a/@data-prod_name')

            yield scrapy.Request(
                url=product_url,
                callback=self.parse_product,
                meta={'item': loader.load_item()}
            )

        next_page = response.xpath('//a[@rel="next"]/@href').get()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)

            yield scrapy.Request(url=next_page_link, callback=self.parse)

    def parse_product(self, response):
        selector = response.selector.xpath('//section[@class="row"]')
        loader = ItemLoader(item=response.meta["item"], selector=selector)
        # meta_loader = ItemLoader(item=ProductItemMeta(), selector=selector)
        loader.add_xpath('detail_name', './/h1[@itemprop="name"]/text()')
        loader.add_xpath('brand', './/h5[@itemprop="brand"]/text()')
        loader.add_xpath(
            'description',
            './/div[@class="col-xs-12 col-sm-12 col-md-12 col-lg-12"]/p/text()'
        )

        _loader = loader.nested_xpath('//select[@id="__sku"]/option')
        _loader.add_xpath('price', './/@data-priceformat')
        _loader.add_xpath('size_format', './/text()')

        loader.selector = response.selector.xpath('//div[@id="accordion"]/div[@class="panel panel-default"]')
        loader.add_xpath('detail_description', './/div[@id="collapseOne"]/div/descendant-or-self::*/text()')
        loader.add_xpath('detail_ingredients', './/div[@id="collapseTwo"]/div/descendant-or-self::*/text()')
        loader.add_xpath('nutritional_facts', './/div[@id="collapseThree"]/div/descendant-or-self::*/text()')
        loader.add_xpath('nutritional_facts_img_url', './/*[@id="collapseThree"]/div/p/img/@src')

        loader.selector = response.selector.xpath('//*[@id="review"]/div/div/div')
        loader.add_xpath('customer_review_header', './/h3[@class="panel-title"]/text()')
        ratings = []
        for _ in loader.selector:
            rating = ''.join(_.xpath('.//label/text()').getall())
            ratings.append(rating)
        loader.add_value('customer_review_rating', ratings)
        loader.add_xpath('customer_review', './/blockquote[@class="blockquote-reverse"]/p/text()')

        self.log(f'finished parsing product page {response.url}')
        return loader.load_item()

    def parse_product_item_meta(self, response):
        selector = response.selector.xpath('//*[@id="collapseOne"]/')
        loader = ItemLoader(item=response.meta["item"], selector=selector)
        loader.selector = response.selector.xpath('//*[@id="collapseOne"]/')
        loader.add_xpath('detail_description', './/div/descendant-or-self::*/text()')
        self.log('>>>>>>>>>>>>>>>>>>> BEGIN >>>>>>>>>>>>>>>>>>>')
        self.log(loader.load_item())
        self.log('>>>>>>>>>>>>>>>>>>> END >>>>>>>>>>>>>>>>>>>')
        self.log('parsing product item meta')
        return loader.load_item()
