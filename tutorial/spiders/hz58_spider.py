# -*- coding: utf-8 -*-
import scrapy
# from tutorial.items import BuildingItem, UrlItem
from scrapy.http import Request
from selenium import webdriver
import time
import urllib
import re


class hz58Spider(scrapy.Spider):
    name = "hz58"
    allowed_domain = ["hz.58.com"]
    start_urls = [
        "http://hz.58.com/cheku/"
    ]
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36"}

    def __init__(self):
        self.driver = webdriver.Chrome()
        # 翻页请求
        self.query_url_list = []

        self.region_page_info = {}
        # 已经爬取的写字楼
        self.used_buildings = set()
        # 取出标签里值
        self.xml_tag_regax_exp = re.compile(r"<.*?>")

    # def parse(self, response):
    #     self.driver.get("http://www.o571.com/office/571/571_14119.html")
    #     while True:
    #         elements = self.driver.find_elements_by_xpath("//div[@class='bis_actinfo clearfix']/ul/li")
    #         if len(elements) > 0:
    #             address = self.xml_tag_regax_exp.sub("", elements[7].text)
    #             # 城区商圈
    #             business = self.xml_tag_regax_exp.sub("", elements[5].text)
    #             # 行业特点
    #             character = self.xml_tag_regax_exp.sub("", elements[13].text)
    #             # 物业名称
    #             name = self.xml_tag_regax_exp.sub("", elements[1].text)
    #             # 物业描述
    #             desc = self.xml_tag_regax_exp.sub("",
    #                                               self.driver.find_element_by_xpath(
    #                                                   "//div[@class='tab_detail_item']/p").text)
    #
    #             item = BuildingItem()
    #             item["region"] = response.meta["region"]
    #             item["name"] = name
    #             item["business"] = business
    #             item["character"] = character
    #             item["address"] = address
    #             item["desc"] = desc
    #             item["url"] = response.url
    #
    #             yield item
    #             break
    #         else:
    #             pass
    #     self.driver.close()


    def parse(self, response):
        '''
        获取翻页请求数据
        :param response:
        :return:
        '''

        print("loading main page")
        # self.driver.get(response.url)
        # self.query_url_list.append(response.url)
        # while True:
        #     elements = self.driver.find_elements_by_xpath("//div[@class='pager']/a/span")
        #     if len(elements) > 0:
        #         print("page counts: %s" % elements[len(elements) - 2].text)
        #         for i in range(2, int(elements[len(elements) - 2].text) + 1):
        #             url = "http://hz.58.com/cheku/pn%d/" % i
        #             self.query_url_list.append(url)
        #         break
        #     else:
        #         pass
        #     time.sleep(0.5)
        #
        # self.driver.close()
        #
        # print(self.query_url_list)
        yield Request(url=self.start_urls[0], callback=self.parse_main,
                      headers=self.headers)
        # self.generateQueryString()
        # for query_string in self.query_string_list:
        #     yield Request(url=self.start_urls[0] + "?" + urllib.urlencode(query_string), callback=self.parse_main,
        #                   headers=self.headers)

    def parse_main(self, response):
        '''
        用于爬取列表首页
        :param response:
        :return:
        '''

        time.sleep(10)
        lilists = response.xpath("//ul[@class='house-list-wrap']/li")
        for li in lilists:
            title = li.xpath(".//h2/a/span/text()").extract()[0]
            description = li.xpath(".//p/span/text()").extract()
            area = description[0].strip()
            address = li.xpath(".//p/span/span/text()").extract()[0]
            size = description[2]
            date_time = li.xpath(".//div[@class = 'time']/text()").extract()[0]
            price_day = li.xpath(".//p[@class = 'sum']/b/text()").extract()[0]
            price_day_unit = description[3]
            price_month = description[4]
            print("%s, %s, %s, %s, %s, %s, %s, %s " % (
            title, area, address, size, date_time, price_day, price_day_unit, price_month))

    def parse_build(self, response):
        '''
        用于解析物业信息页面并爬取相关信息
        :param response:
        :return:
        '''

        table_base_info = response.xpath("//div/ul[@class='info']/li").extract()

        if len(table_base_info) > 0:
            time.sleep(10)
            # 区域
            region = table_base_info[0].xpath("//a/text()").extract()[0]
            # 商圈
            area = table_base_info[0].xpath("//a/text()").extract()[1]
            # 地段
            address = table_base_info[1].xpath(".//text()").extract()[0]
            # 类别
            character = table_base_info[2].xpath(".//text()").extract()[0]
            # 面积
            size = table_base_info[3].xpath(".//text()").extract()[0]
            # 租金
            fee = table_base_info[4].xpath(".//text()").extract()[0]

            item = BuildingItem()
            item["title"] = response.meta["title"]
            item["region"] = region
            item["area"] = area
            item["address"] = address
            item["character"] = character
            item["size"] = size
            item["fee"] = fee
            item["url"] = response.url

            yield item
        else:
            self.driver = webdriver.Chrome()
            self.driver.get(response.url)

            while True:
                elements = self.driver.find_elements_by_xpath("//div/ul[@class='info']/li")
                if len(elements) > 0:
                    # 区域
                    region = table_base_info[0].xpath("//a/text()").extract()[0].text
                    # 商圈
                    area = table_base_info[0].xpath("//a/text()").extract()[1].text
                    # 地段
                    address = table_base_info[1].xpath(".//text()").extract()[0].text
                    # 类别
                    character = table_base_info[2].xpath(".//text()").extract()[0].text
                    # 面积
                    size = table_base_info[3].xpath(".//text()").extract()[0].text
                    # 租金
                    fee = table_base_info[4].xpath(".//text()").extract()[0].text

                    item = BuildingItem()
                    item["title"] = response.meta["title"]
                    item["region"] = region
                    item["area"] = area
                    item["address"] = address
                    item["character"] = character
                    item["size"] = size
                    item["fee"] = fee
                    item["url"] = response.url

                    yield item
                    break
                else:
                    pass
            self.driver.close()

    def generateQueryString(self):

        max_page = 0
        for key, value in self.region_page_info.items():
            if value > max_page:
                max_page = value

        for i in range(1, max_page + 1):
            queryString = {}
            for key, value in self.region_page_info.items():
                current_page = i % value
                if current_page == 0:
                    pass
                else:
                    queryString[key] = current_page + 1
            self.query_string_list.append(queryString)
