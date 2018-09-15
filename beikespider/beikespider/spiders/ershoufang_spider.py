#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian

import time
from scrapy.spiders import Spider
from bs4 import BeautifulSoup
from beikespider.items import *
from beikespider.libs.url import *


class ErShouFangSpider(Spider):
    name = 'ershoufang'
    allowed_domains = 'ke.com'
    start = time.time()
    start_urls = []
    city = None

    def __init__(self):
        # 只有第一次进来才初始化url列表
        if len(ErShouFangSpider.start_urls) == 0:
            url = URL(ErShouFangSpider.name)
            ErShouFangSpider.start_urls = url.start_urls
            ErShouFangSpider.city = url.city

    def closed(self, reason):
        """
        结束的时候计时
        :param reason:
        :return:
        """
        print("-" * 50)
        print("total time cost:{0} seconds".format(time.time() - self.start))
        print("-" * 50)

    def parse(self, response):
        """
        针对每一个URL进行处理
        :param response:
        :return:
        """
        item = BeikespiderErShouFangItem()
        html = response.body
        soup = BeautifulSoup(html, "lxml")

        # 获得有小区信息的panel
        xiaoqu_items = soup.find_all('li', class_="clear")
        print("----\nlen: {0}\n----\n".format(len(xiaoqu_items)))
        for xiaoqu_elem in xiaoqu_items:
            title = xiaoqu_elem.find('div', class_="title")
            name = title.text.replace("\n", "")

            price = xiaoqu_elem.find('div', class_="totalPrice")
            price = price.text.strip()

            # 继续清理数据

            print("{0} {1}".format(name, price))
            item['name'] = name
            item['price'] = price
            yield item


