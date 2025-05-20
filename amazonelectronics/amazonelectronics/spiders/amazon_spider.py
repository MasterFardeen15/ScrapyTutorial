import scrapy
from ..items import AmazonelectronicsItem
from scrapy.utils.response import open_in_browser


class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon"
    page_number = 2
    start_urls = [
        "https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/ref=zg_bs_nav_electronics_0"
    ]

    def parse(self, response):
        # open_in_browser(response)
        all_div_items = response.css('#gridItemRoot')
        
        for object in all_div_items:
            items = AmazonelectronicsItem()
            
            title = object.css('._cDEzb_p13n-sc-css-line-clamp-4_2q2cc, ._cDEzb_p13n-sc-css-line-clamp-3_g3dy1').css('::text').extract()
            rank = object.css('.zg-bdg-text::text').extract()
            price = object.css('.p13n-sc-price').css('::text').extract()
            imagelink = object.css('.p13n-product-image').css('::attr(src)').extract()
            ratingnum = object.css('.a-size-small::text').extract()
            ratingscore = object.css('.a-icon-alt::text').extract()
            ratingscore[0] = ratingscore[0][:3]

            items['title'] = title
            items['rank'] = rank
            items['price'] = price or "N/A"
            items['imagelink'] = imagelink
            items['ratingnum'] = ratingnum
            items['ratingscore'] = ratingscore

            yield items
            
        next_page = 'https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/ref=zg_bs_pg_' + str(AmazonSpiderSpider.page_number) + '_electronics?_encoding=UTF8&pg=' + str(AmazonSpiderSpider.page_number)
        if AmazonSpiderSpider.page_number < 3:
            AmazonSpiderSpider.page_number += 1
            yield response.follow(next_page, callback = self.parse)
