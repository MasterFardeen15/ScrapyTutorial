import scrapy
from ..items import AmazonelectronicsItem

class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon_spider"
    start_urls = [
        "https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/ref=zg_bs_nav_electronics_0"
    ]

    def parse(self, response):
        
        all_div_items = response.css('#gridItemRoot')
        
        for object in all_div_items:
            items = AmazonelectronicsItem()
            
            title = object.css('._cDEzb_p13n-sc-css-line-clamp-3_g3dy1::text').extract()
            rank = object.css('.zg-bdg-text::text').extract()
            price = object.css('._cDEzb_p13n-sc-price_3mJ9Z').css('::text').extract()
            imagelink = object.css('.p13n-product-image').css('::attr(src)').extract()
            
            items['title'] = title
            items['rank'] = rank
            items['price'] = price
            items['imagelink'] = imagelink

            yield items
