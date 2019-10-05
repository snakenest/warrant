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
import datetime


class warrantSpider(scrapy.Spider):
# class warrantSpider(CrawlSpider):
    name = 'warrant'
    #allowed_domains = ['example.com']
    start_urls = [ 'https://xueqiu.com/S/03333/warrants' ]
    # rules = [ Rule( LinkExtractor( allow="" ), callback = "parse", follow = True ) ]
    # pattern = '//tbody//tr[style="background:#f7fbff"]'

    # def parse(self, response):
    #     yield scrapy.Request("", self.parse_result )

    def parse(self, response):
       return scrapy.FormRequest.from_response(response,
                                               # formdata = {"bond_type":"C", "expiration_date":""},
                                               # cookie = {acw_tc=2760825115701824789182996e4fe30581840b280d2a284247e4c611bfdc25; s=c414295n4b; device_id=258373d5a3c500bb05167911072e7845; __utmz=1.1570182209.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); aliyungf_tc=AQAAABCuM1BZVAAAb96MtDhkQpUsSqPi; Hm_lvt_1db88642e346389874251b5a1eded6e3=1570182210,1570241864; __utma=1.1267085133.1570182209.1570206244.1570241864.4; __utmc=1; remember.sig=K4F3faYzmVuqC0iXIERCQf55g2Y; xq_a_token.sig=8NI427AkiIfVYmZmVPpj6NGXVnY; xqat.sig=fTnxYqGeWX7_4eLdQ9RtBdQ-ji4; xq_r_token.sig=qjimIorxo_6mBwRyiBEfGy1xwt8; xq_is_login.sig=J3LxgPVPUzbBg3Kee_PquUfih7Q; u.sig=2LCFm9PagHRwy6mHTDtUlz0j4Lg; bid=81cadd301d31d03370661687f006f8bb_k1cyr0pi; __utmt=1; snbim_minify=true; captcha_id=TElA0553pST6TZFHovoHtVI9fcz52z; captcha_id.sig=5li3K6VxCZi80cYVXyzqZfbJk30; xq_a_token=28b9c4a9c63a9578e94261e1e44d8372ec454774; xqat=28b9c4a9c63a9578e94261e1e44d8372ec454774; xq_r_token=2a17e7aaabb0d3645000542a9666ef9563afa10e; xq_is_login=1; u=1576652359; __utmb=1.13.9.1570244147214; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1570244335}
                                               callback = self.parse_result,
                                               method = "GET",
                                               url = "https://stock.xueqiu.com/v5/stock/hk/warrant/query.json?symbol=03333&orderby=percent&order=desc&page=1&size=100&bond_type=C&expiration_date=")


    def parse_result(self, response):
        py_dict = json.loads( response.body )
        py_list = py_dict["data"]["items"]
        for ele in py_list:
            cost_per_share = float(str(ele["current"])) * float(str(ele["conversion_ratio"]))
            breakeven_point = cost_per_share + float(str(ele["strike_price"]))
            shares_20000 = int( 20/cost_per_share ) * 1000
            earnings_24 = ( 24 - breakeven_point ) * shares_20000
            ele["breakeven_point"] = breakeven_point
            ele["earnings_24"] = earnings_24
            ele["expiration_date"] = datetime.datetime.fromtimestamp( ele["expiration_date"]/1000)
            WarrantItem = ele
            yield WarrantItem
        # for ele in response.xpath(self.pattern):
        #
        #         codes = ele.xpath('./td[1]/a/text()')[0]
        #         names = ele.xpath('./td[2]/a/text()')[0]
        #         excise_prices = ele.xpath('./td[9]/text()')[0]
        #         prices = ele.xpath('./td[3]/text()')[0]
        #         ratios = ele.xpath('./td[17]/text()')[0]
        #         expiration_dates_raw = ele.xpath('./td[8]/text()')[0]
        #         expiration_dates = int( expiration_dates_raw[0:4] + expiration_dates_raw[6:8] + expiration_dates_raw[10:12] )
        #         outstanding_ratio = ele.xpath('./td[10]/text()')[0]
        #         cost_per_share = float(str(prices)) * float(str(ratios))
        #         # pdb.set_trace()
        #         breakeven_point = cost_per_share + float(str(excise_prices))
        #         shares_20000 = int( 20/cost_per_share ) * 1000
        #         earnings_24 = ( 24 - breakeven_point ) * shares_20000
        #         yield WarrantItem(code = codes, name = names, price = prices, excise_price = excise_prices,
        #                           ratio = ratios, street_cargo_ratio = street_cargo_ratio, expiration_date = expiration_dates, breakeven_point = breakeven_point, earnings_24 = earnings_24 )



    # def parse_result(self, response):
    #     for ele in response.xpath(self.pattern):
    #         # if  not ele.xpath('./td[1]/text()') == []:
    #         #     pass
    #         # else:
    #             codes = ele.xpath('./td[1]/a/text()')[0]
    #             names = ele.xpath('./td[2]/a/text()')[0]
    #             excise_prices = ele.xpath('./td[9]/text()')[0]
    #             prices = ele.xpath('./td[3]/text()')[0]
    #             ratios = ele.xpath('./td[17]/text()')[0]
    #             expiration_dates_raw = ele.xpath('./td[8]/text()')[0]
    #             expiration_dates = int( expiration_dates_raw[0:4] + expiration_dates_raw[6:8] + expiration_dates_raw[10:12] )
    #             outstanding_ratio = ele.xpath('./td[10]/text()')[0]
    #             cost_per_share = float(str(prices)) * float(str(ratios))
    #             # pdb.set_trace()
    #             breakeven_point = cost_per_share + float(str(excise_prices))
    #             shares_20000 = int( 20/cost_per_share ) * 1000
    #             earnings_24 = ( 24 - breakeven_point ) * shares_20000
    #             yield WarrantItem(code = codes, name = names, price = prices, excise_price = excise_prices,
    #                               ratio = ratios, street_cargo_ratio = street_cargo_ratio, expiration_date = expiration_dates, breakeven_point = breakeven_point, earnings_24 = earnings_24 )



    # def __init__(self):
    #     super(warrantSpider,self).__init__()
    #     chrome_options = Options()
    #     chrome_options.add_argument('--headless')
    #     chrome_options.add_argument('--disable-gpu')
    #     chrome_options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    #     #chrome_options.binary_location = '/opt/google/chrome/chrome'
    #     # opener = webdriver.Chrome(chrome_options=chrome_options)
    #     self.driver = webdriver.Chrome(executable_path="F:\\chromedriver_win32\\chromedriver.exe", chrome_options = chrome_options )

    # def parse(self, response):
    #     self.driver.get(response.url)
    #     while True:
    #         temp = self.driver.page_source
    #         response = etree.HTML(temp, parser=etree.HTMLParser(encoding='utf-8'))
    #         # pdb.set_trace()
    #         for WarrantItem in self.parse_result(response):
    #             yield  WarrantItem
    #         res = self.isElementPresent('下一页')
    #         if res == False:
    #             break
    #         else:
    #             # next_page = self.driver.find_element_by_xpath("//a[contains(text(),'下一页')]")
    #             next_page = self.driver.find_element_by_link_text("下一页")
    #             next_page.click()
    #             time.sleep(2)
    #     self.driver.close()

    # def parse_result(self, response):
    # # def parse(self, response):
    # #     print response
    #
    #     for ele in response.xpath(self.pattern):
    #
    #         # if  ele.xpath('./td[1]/text()').extract()[0].encode("utf-8") == '窝轮代码':
    #         if  not ele.xpath('./td[1]/text()') == []:
    #             pass
    #         else:
    #             codes = ele.xpath('./td[1]/a/text()')[0]
    #             names = ele.xpath('./td[2]/a/text()')[0]
    #             excise_prices = ele.xpath('./td[5]/text()')[0]
    #             prices = ele.xpath('./td[7]/text()')[0]
    #             ratios = ele.xpath('./td[8]/text()')[0]
    #             expiration_dates = int( ele.xpath('./td[10]/text()')[0] )
    #             cost_per_share = float(str(prices)) * float(str(ratios))
    #             # pdb.set_trace()
    #             breakeven_point = cost_per_share + float(str(excise_prices))
    #             shares_20000 = int( 20/cost_per_share ) * 1000
    #             earnings_24 = ( 24 - breakeven_point ) * shares_20000
    #             yield WarrantItem(code = codes, name = names, price = prices, excise_price = excise_prices,
    #                               ratio = ratios, expiration_date = expiration_dates, breakeven_point = breakeven_point, earnings_24 = earnings_24 )
    #
    #
    # def isElementPresent(self, value):
    #
    #     try:
    #         element = self.driver.find_element_by_link_text(value)
    #     #原文是except NoSuchElementException, e:
    #     except NoSuchElementException as e:
    #         #打印异常信息
    #         print e.msg
    #         #发生了NoSuchElementException异常，说明页面中未找到该元素，返回False
    #         return False
    #     else:
    #         #没有发生异常，表示在页面中找到了该元素，返回True
    #         return True