import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from ..items import QuotetutorialItem

class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    page_number = 2
    start_urls = ['https://quotes.toscrape.com/login']
    # start_urls = ['https://quotes.toscrape.com/page/1/']
    # start_urls = ['https://quotes.toscrape.com/']
    
    def parse(self, response):
        token = response.css('form input::attr(value)').extract_first()
        return FormRequest.from_response(response, formdata={
            'csrf_token': token,
            'username': 'user',
            'password': 'password'
        }, callback=self.start_scraping)
    
    def start_scraping(self, response):
        # open_in_browser(response)
        all_div_quotes = response.css('div.quote')
        
        for quote in all_div_quotes:
            items = QuotetutorialItem()
            title = quote.css('span.text::text').extract()
            author = quote.css('.author::text').extract()
            tag = quote.css('.tag::text').extract()
            
            items['title'] = title
            items['author'] = author
            items['tag'] = tag
            
            yield items
        
        next_page = 'https://quotes.toscrape.com/page/' + str(QuoteSpider.page_number) + '/'
        if QuoteSpider.page_number < 11:
            QuoteSpider.page_number += 1
            yield response.follow(next_page, callback = self.start_scraping)
            
    
    # BACK UP OLD CODE
    # def parse(self, response):
    #     # title = response.css('title::text').extract()
    #     # yield {'titletext': title}
        
    #     all_div_quotes = response.css('div.quote')
        
    #     # title = all_div_quotes.css('span.text::text').extract()
    #     # author = all_div_quotes.css('.author::text').extract()
    #     # tag = all_div_quotes.css('.tag::text').extract()
        
    #     for quote in all_div_quotes:
    #         items = QuotetutorialItem()
    #         title = quote.css('span.text::text').extract()
    #         author = quote.css('.author::text').extract()
    #         tag = quote.css('.tag::text').extract()
            
    #         items['title'] = title
    #         items['author'] = author
    #         items['tag'] = tag
            
    #         yield items
        
    #     next_page = 'https://quotes.toscrape.com/page/' + str(QuoteSpider.page_number) + '/'
    #     if QuoteSpider.page_number < 11:
    #         QuoteSpider.page_number += 1
    #         yield response.follow(next_page, callback = self.parse)
        
    #     # next_page = response.css('li.next a::attr(href)').get()
    #     # if next_page is not None:
    #     #     yield response.follow(next_page, callback = self.parse)
            
            
            
    #         # yield {
    #         #     'title' : title,
    #         #     'author' : author,
    #         #     'tag' : tag
    #         # }