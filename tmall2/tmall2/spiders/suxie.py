# -*- coding: utf-8 -*-
import scrapy
import json
import re
from tmall2.items import Tmall2Item
import logging
logger = logging.getLogger(__name__)


class SuxieSpider(scrapy.Spider):
    name = "suxie"
    allowed_domains = ["m.tmall.com"]
    url = "https://croquis.m.tmall.com/shop/shop_auction_search.do?&sort=s&p="
    offset = 1
    start_urls = [url+str(offset)]
    pattern = re.compile(r"\"price\":{\"priceMoney\":\d*?,\"priceText\":\"(\d*?)\"}")

    def parse(self, response):
        # 获取json格式字符串
        json_response = response.body.decode()
        # logger.warning(json_response)
        # 将json转化成字典类型
        dict_response = json.loads(json_response)
        # logger.warning(dict_response)
        # 获取"items"的值，为一个列表，列表中每一个元素就是一个包含商品信息的字典
        goods_list = dict_response["items"]
        # logger.warning(goods_list)
        if len(goods_list) > 0:
            for goods in goods_list:
                item = Tmall2Item()
                item["goods_id"] = goods.get("item_id", None)
                item["goods_desc"] = goods.get("title", None)
                item["goods_img"] = goods.get("img", None)
                item["goods_sold"] = goods.get("sold", None)
                item["goods_total_sold"] = goods.get("totalSoldQuantity", None)
                item["goods_href"] = goods.get("url", None)
                # logger.warning(item)
                if item["goods_href"] is not None:
                    item["goods_href"] = "https:" + item["goods_href"]
                    yield scrapy.Request(item["goods_href"], callback=self.parse_price, meta={"item": item})
            self.offset += 1
            yield scrapy.Request(self.url+str(self.offset), callback=self.parse)
            logger.warning("当前为第{}页".format(self.offset))
        else:
            logger.warning("最后一页为：{}".format(self.offset-1))

    def parse_price(self, response):
        item = response.meta["item"]
        # 获取商品详情页并转化为字符串
        str_response = response.text
        # 利用正则匹配出价格
        item["goods_price"] = self.pattern.search(str_response)
        # logger.warning(price)
        if item["goods_price"] is not None:
            item["goods_price"] = item["goods_price"].group(1)
            logger.warning(item)
            yield item
