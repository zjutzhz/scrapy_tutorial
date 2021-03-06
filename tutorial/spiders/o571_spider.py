# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import BuildingItem, UrlItem
from scrapy.http import Request
from selenium import webdriver
import time
import urllib
import re


class O571Spider(scrapy.Spider):
    name = "o571"
    allowed_domain = ["o571.com"]
    start_urls = [
        "http://www.o571.com/show/show.asp"
    ]
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36"}

    def __init__(self):
        self.driver = webdriver.Chrome()
        # 翻页请求
        self.query_string_list = []

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

        print "loading main page"
        self.driver.get(response.url)

        while True:
            elements = self.driver.find_elements_by_xpath("//div/span/select[@name='JumpPage']")
            if len(elements) > 0:
                for i, element in enumerate(elements):
                    options = element.find_elements_by_tag_name("option")
                    print "page%d=%d" % (i, len(options))

                    self.region_page_info["page%d" % (i + 1)] = len(options)

                    # for j in range(len(options)):
                    #     self.query_string_list.append({"page%d" % (i + 1): "%d" % (j + 1)})
                break
            else:
                pass
            time.sleep(0.5)

        self.driver.close()
        yield Request(url=self.start_urls[0], callback=self.parse_main,
                      headers=self.headers)
        self.generateQueryString()
        for query_string in self.query_string_list:
            yield Request(url=self.start_urls[0] + "?" + urllib.urlencode(query_string), callback=self.parse_main,
                          headers=self.headers)

    def parse_main(self, response):
        '''
        用于爬取列表首页
        :param response:
        :return:
        '''

        time.sleep(10)
        title_list = [table_region.extract() for table_region in
                      response.xpath("//td[@class='show_info']/span/font/text()")]

        table_list = [table for table in response.xpath("//table[@class='show_name mt5 box1']")]

        for i in range(0, len(table_list)):

            for buildInfo in table_list[i].xpath(".//td"):
                if len(buildInfo.xpath(".//a/@href").extract()) > 0:
                    building_url = buildInfo.xpath(".//a/@href").extract()[0]
                    if len(building_url) > 0:
                        if building_url in self.used_buildings:
                            print "skip used url"
                        else:
                            self.used_buildings.add(building_url)
                            # urlItem = UrlItem()
                            # urlItem["url"] = building_url
                            # urlItem["region"] = title_list[i]
                            # yield urlItem
                            print "current count: %d" % len(self.used_buildings)
                            yield Request(url=building_url, callback=self.parse_build, headers=self.headers,
                                          meta={"region": title_list[i]})
                else:
                    print "missing building url in "
                    print buildInfo.extract()

    def parse_build(self, response):
        '''
        用于解析物业信息页面并爬取相关信息
        :param response:
        :return:
        '''

        table_base_info = response.xpath("//div[@class='bis_actinfo clearfix']/ul/li").extract()

        if len(table_base_info) > 0:
            time.sleep(10)
            # 物业地址
            address = self.xml_tag_regax_exp.sub("", table_base_info[7])
            # 城区商圈
            business = self.xml_tag_regax_exp.sub("", table_base_info[5])
            # 行业特点
            character = self.xml_tag_regax_exp.sub("", table_base_info[13])
            # 物业名称
            name = response.xpath("//div[@id='content']/h2/text()").extract()[0]
            # 物业描述
            desc = self.xml_tag_regax_exp.sub("", response.xpath("//div[@class='tab_detail_item']/p").extract()[0])

            item = BuildingItem()
            item["region"] = response.meta["region"]
            item["name"] = name
            item["business"] = business
            item["character"] = character
            item["address"] = address
            item["desc"] = desc
            item["url"] = response.url

            yield item
        else:
            self.driver = webdriver.Chrome()
            self.driver.get(response.url)

            while True:
                elements = self.driver.find_elements_by_xpath("//div[@class='bis_actinfo clearfix']/ul/li")
                if len(elements) > 0:
                    address = self.xml_tag_regax_exp.sub("", elements[7].text)
                    # 城区商圈
                    business = self.xml_tag_regax_exp.sub("", elements[5].text)
                    # 行业特点
                    character = self.xml_tag_regax_exp.sub("", elements[13].text)
                    # 物业名称
                    name = self.xml_tag_regax_exp.sub("", elements[1].text)
                    # 物业描述
                    desc = self.xml_tag_regax_exp.sub("",
                                                      self.driver.find_element_by_xpath(
                                                          "//div[@class='tab_detail_item']/p").text)

                    item = BuildingItem()
                    item["region"] = response.meta["region"]
                    item["name"] = name
                    item["business"] = business
                    item["character"] = character
                    item["address"] = address
                    item["desc"] = desc
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
