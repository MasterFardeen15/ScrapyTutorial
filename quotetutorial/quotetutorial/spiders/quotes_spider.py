import scrapy
from ..items import QuotetutorialItem

class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['https://quotes.toscrape.com/']
    
    def parse(self, response):
        # title = response.css('title::text').extract()
        # yield {'titletext': title}
        
        all_div_quotes = response.css('div.quote')
        
        # title = all_div_quotes.css('span.text::text').extract()
        # author = all_div_quotes.css('.author::text').extract()
        # tag = all_div_quotes.css('.tag::text').extract()
        
        for quote in all_div_quotes:
            items = QuotetutorialItem()
            title = quote.css('span.text::text').extract()
            author = quote.css('.author::text').extract()
            tag = quote.css('.tag::text').extract()
            
            items['title'] = title
            items['author'] = author
            items['tag'] = tag
            
            yield items
            
        next_page = response.css('li.next a::attr(href)').get()
        
        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)
            
            
            
            # yield {
            #     'title' : title,
            #     'author' : author,
            #     'tag' : tag
            # }