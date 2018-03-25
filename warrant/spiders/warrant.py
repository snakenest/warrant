# -*- coding: utf-8 -*-
from __future__ import absolute_import
import scrapy
from warrant.items import WarrantItem
import pdb

class warrantSpider(scrapy.Spider):
    name = 'warrant'
    #allowed_domains = ['example.com']
    #start_urls = ['http://vip.stock.finance.sina.com.cn/quotes_service/view/hk_warrant_search.php?stock_symbol=01918&publisher=&class=a']
    start_urls = ['http://www.bhly.gov.cn/index.php?g=&m=article&a=index&id=6810']
    debugged = False
    #pattern = '//div[@class = "tbl_wrap"]/table/tbody//tr/th[1]/a/text()'
    pattern = '//table//tbody//tr[@height = "26"]'

    def parse(self, response):
        #print response.xpath(self.pattern).extract()
        #if not self.debugged:
        #    self.debugged = True
        #    from scrapy.shell import inspect_response
        #    inspect_response(response, self)

            for ele in response.xpath(self.pattern):
                codes = ele.xpath('./td[@width = "46"]/text()').extract()
                names = ele.xpath('./td[@width = "144"]/text()').extract()
                prices = ele.xpath('./td[@width = "232"]/text()').extract()
                excise_prices = ele.xpath('./td[@width = "72"][1]/text()').extract()
                ratios = ele.xpath('./td[@width = "72"][2]/text()').extract()
                expiration_dates = ele.xpath('./td[@width = "53"]/text()').extract()
                yield WarrantItem(code = codes, name = names, price = prices, excise_price = excise_prices,
                                  ratio = ratios, expiration_date = expiration_dates)
                #pdb.set_trace()


