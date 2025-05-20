# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonelectronicsItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    rank = scrapy.Field()
    price = scrapy.Field()
    imagelink = scrapy.Field()
    pass
