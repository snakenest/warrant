# -*- coding: utf-8 -*-
import scrapy


class warrantSpider(scrapy.Spider):
    name = 'warrant'
    #allowed_domains = ['example.com']
    start_urls = ['http://vip.stock.finance.sina.com.cn/quotes_service/view/hk_warrant_search.php?stock_symbol=01918&publisher=&class=a']
    debugged = False

    def parse(self, response):
        if not self.debugged:
            self.debugged = True
            from scrapy.shell import inspect_response
            inspect_response(response, self)
        print response.xpath('//div[@class = "tbl_wrap"]').extract()
