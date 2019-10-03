# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WarrantItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    code = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    excise_price = scrapy.Field()
    ratio = scrapy.Field()
    expiration_date = scrapy.Field()
    breakeven_point = scrapy.Field()
    earnings_24 = scrapy.Field()
    pass
