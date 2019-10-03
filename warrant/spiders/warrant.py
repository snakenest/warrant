# -*- coding: utf-8 -*-
from __future__ import absolute_import
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import re
import json
from warrant.items import WarrantItem
import pdb
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
#从selenium.common.exceptions 模块导入 NoSuchElementException类
from selenium.common.exceptions import NoSuchElementException


class warrantSpider(scrapy.Spider):
# class warrantSpider(CrawlSpider):
    name = 'warrant'
    #allowed_domains = ['example.com']
    #start_urls = ['http://vip.stock.finance.sina.com.cn/quotes_service/view/hk_warrant_search.php?stock_symbol=01918&publisher=&class=a']
    #start_urls = ['http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/HK_DelayQuotes.getWarrant?stock_symbol=01918&value=&class=a&publisher=&page=1&num=20&sort=&asc=NaN&pre_min=&pre_max=&str_min=&str_max=&con_min=&con_max=&m_start_year=&m_start_month=&m_end_year=&m_end_month=&r_e=&r_n=']
    #pattern = '//div[@class = "tbl_wrap"]/table/tbody//tr/th[1]/a/text()'

    start_urls = [ 'http://stock.finance.sina.com.cn/hkstock/warrants/03333.html' ]
    # rules = [ Rule( LinkExtractor( allow="\.phtml" ), callback = "parse_result", follow = True ) ]
    pattern = '//div[@id="sub01_c1" and @class="sub01_c"]/table/tbody//tr'

    #start_urls = ['http://www.bhly.gov.cn/index.php?g=&m=article&a=index&id=6810']
    #pattern = '//table//tbody//tr[@height = "26"]'

    # start_urls = ['http://stockhtm.finance.qq.com/hk/others/xgwl.html?q=03333']
    # pattern = ''


    #def parse(self, response):
       # return scrapy.FormRequest.from_response(response,
    #                                            formdata = {"stock_symbol":"01918", "class":"a", "page":"1", "num":"20"},
    #                                            callback = self.after_selection,
    #                                            method = "GET",
    #                                            url = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/HK_DelayQuotes.getWarrant?stock_symbol=01918&value=&class=a&publisher=&page=1&num=20&sort=&asc=NaN&pre_min=&pre_max=&str_min=&str_max=&con_min=&con_max=&m_start_year=&m_start_month=&m_end_year=&m_end_month=&r_e=&r_n=")

    # def parse(self, response):
    #     return scrapy.Request("http://stock.finance.sina.com.cn/hkstock/go/Warrants/type/1/page/2/code/03333" + "\.html", self.parse_result)

    def __init__(self):
        super(warrantSpider,self).__init__()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        #chrome_options.binary_location = '/opt/google/chrome/chrome'
        # opener = webdriver.Chrome(chrome_options=chrome_options)
        self.driver = webdriver.Chrome(executable_path="F:\\chromedriver_win32\\chromedriver.exe", chrome_options = chrome_options )

    def parse(self, response):
        self.driver.get(response.url)
        while True:
            temp = self.driver.page_source
            response = etree.HTML(temp, parser=etree.HTMLParser(encoding='utf-8'))
            # pdb.set_trace()
            for WarrantItem in self.parse_result(response):
                yield  WarrantItem
            res = self.isElementPresent('下一页')
            if res == False:
                break
            else:
                # next_page = self.driver.find_element_by_xpath("//a[contains(text(),'下一页')]")
                next_page = self.driver.find_element_by_link_text("下一页")
                next_page.click()
                time.sleep(2)
                # pdb.set_trace()

        self.driver.close()

    def parse_result(self, response):
    # def parse(self, response):
    #     print response

        for ele in response.xpath(self.pattern):

            # if  ele.xpath('./td[1]/text()').extract()[0].encode("utf-8") == '窝轮代码':
            if  not ele.xpath('./td[1]/text()') == []:
                pass
            else:
                codes = ele.xpath('./td[1]/a/text()')[0]
                names = ele.xpath('./td[2]/a/text()')[0]
                excise_prices = ele.xpath('./td[5]/text()')[0]
                prices = ele.xpath('./td[7]/text()')[0]
                ratios = ele.xpath('./td[8]/text()')[0]
                expiration_dates = int( ele.xpath('./td[10]/text()')[0] )
                cost_per_share = float(str(prices)) * float(str(ratios))
                # pdb.set_trace()
                breakeven_point = cost_per_share + float(str(excise_prices))
                shares_20000 = int( 20/cost_per_share ) * 1000
                earnings_24 = ( 24 - breakeven_point ) * shares_20000
                yield WarrantItem(code = codes, name = names, price = prices, excise_price = excise_prices,
                                  ratio = ratios, expiration_date = expiration_dates, breakeven_point = breakeven_point, earnings_24 = earnings_24 )


                # codes = ele.xpath('./td[@width = "46"]/text()').extract()
                # names = ele.xpath('./td[@width = "144"]/text()').extract()
                # prices = ele.xpath('./td[@width = "232"]/text()').extract()
                # excise_prices = ele.xpath('./td[@width = "72"][1]/text()').extract()
                # ratios = ele.xpath('./td[@width = "72"][2]/text()').extract()
                # expiration_dates = ele.xpath('./td[@width = "53"]/text()').extract()
                # yield WarrantItem(code = codes, name = names, price = prices, excise_price = excise_prices,
                #                   ratio = ratios, expiration_date = expiration_dates)



    def isElementPresent(self, value):

        try:
            element = self.driver.find_element_by_link_text(value)
        #原文是except NoSuchElementException, e:
        except NoSuchElementException as e:
            #打印异常信息
            print e.msg
            #发生了NoSuchElementException异常，说明页面中未找到该元素，返回False
            return False
        else:
            #没有发生异常，表示在页面中找到了该元素，返回True
            return True