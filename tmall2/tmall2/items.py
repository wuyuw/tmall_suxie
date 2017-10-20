# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Tmall2Item(scrapy.Item):
    goods_id = scrapy.Field()
    goods_price = scrapy.Field()
    goods_href = scrapy.Field()
    goods_sold = scrapy.Field()
    goods_total_sold = scrapy.Field()
    goods_img = scrapy.Field()
    goods_desc = scrapy.Field()
