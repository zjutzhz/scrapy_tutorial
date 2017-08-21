# -*- coding: utf-8 -*-
import re
import time
import urllib.parse

import scrapy
from scrapy.http import Request
from selenium import webdriver

from tutorial.items import BuildingItem


class o571Spider(scrapy.Spider):
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

    def parse(self, response):
        '''
        获取翻页请求数据
        :param response:
        :return:
        '''

        print("loading main page")
        self.driver.get(response.url)

        while True:
            elements = self.driver.find_elements_by_xpath("//div/span/select[@name='JumpPage']")
            if len(elements) > 0:
                for i, element in enumerate(elements):
                    options = element.find_elements_by_tag_name("option")
                    print("page%d=%d" % (i, len(options)))

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
            print(self.start_urls[0] + "?" + urllib.parse.urlencode(query_string))
            yield Request(url=self.start_urls[0] + "?" + urllib.parse.urlencode(query_string), callback=self.parse_main,
                          headers=self.headers)

    def parse_main(self, response):
        '''
        用于爬取列表首页
        :param response:
        :return:
        '''

        time.sleep(1)
        title_list = [table_region.extract() for table_region in
                      response.xpath("//td[@class='show_info']/span/font/text()")]

        table_list = [table for table in response.xpath("//table[@class='show_name mt5 box1']")]

        for i in range(0, len(table_list)):

            for buildInfo in table_list[i].xpath(".//td"):
                if len(buildInfo.xpath(".//a/@href").extract()) > 0:
                    building_url = buildInfo.xpath(".//a/@href").extract()[0]
                    if len(building_url) > 0:
                        if building_url in self.used_buildings:
                            print("skip used url")
                        else:
                            self.used_buildings.add(building_url)
                            # urlItem = UrlItem()
                            # urlItem["url"] = building_url
                            # urlItem["region"] = title_list[i]
                            # yield urlItem
                            print("current count: %d" % len(self.used_buildings))
                            yield Request(url=building_url, callback=self.parse_build, headers=self.headers,
                                          meta={"region": title_list[i]})
                else:
                    print("missing building url in ")
                    print(buildInfo.extract())

    def parse_build(self, response):
        '''
        用于解析物业信息页面并爬取相关信息
        :param response:
        :return:
        '''
        time.sleep(1)
        try:
            base_lists = response.xpath("//div[@class='bis_actinfo clearfix']/ul/li").extract()

            if len(base_lists) > 0:
                # 物业地址
                address = self.xml_tag_regax_exp.sub("", base_lists[7])
                # 城区商圈
                business = self.xml_tag_regax_exp.sub("", base_lists[5])
                # 行业特点
                character = self.xml_tag_regax_exp.sub("", base_lists[13])
                # 物业名称
                name = response.xpath("//div[@id='content']/h2/text()").extract()[0]
                # 物业描述
                desc = self.xml_tag_regax_exp.sub("", response.xpath("//div[@class='tab_detail_item']/p").extract()[0])

                supporting_lists = response.xpath("//div[@class='box1 pb3 clearfix']/ul/li").extract()

                if len(supporting_lists) > 0:
                    # 物管公司
                    company = self.xml_tag_regax_exp.sub("", supporting_lists[1])
                    # 楼层状况
                    floor = self.xml_tag_regax_exp.sub("", supporting_lists[3])
                    # 总建筑面积
                    size = self.xml_tag_regax_exp.sub("", supporting_lists[5])
                    # 物管费
                    fee = self.xml_tag_regax_exp.sub("", supporting_lists[7])
                    # 标准层高
                    height = self.xml_tag_regax_exp.sub("", supporting_lists[9])
                    # 车位数量
                    garage = self.xml_tag_regax_exp.sub("", supporting_lists[13])
                    # 标准层面积
                    size_per_floor = self.xml_tag_regax_exp.sub("", supporting_lists[15])
                    # 车位费
                    fee_per_garage = self.xml_tag_regax_exp.sub("", supporting_lists[19])
                    # 交通站点
                    traffic_centre = self.xml_tag_regax_exp.sub("", supporting_lists[25])
                    # 轨道公交
                    traffic = self.xml_tag_regax_exp.sub("", supporting_lists[27])
                else:
                    company = "N/A"
                    # 楼层状况
                    floor = "N/A"
                    # 总建筑面积
                    size = "N/A"
                    # 物管费
                    fee = "N/A"
                    # 标准层高
                    height = "N/A"
                    # 车位数量
                    garage = "N/A"
                    # 标准层面积
                    size_per_floor = "N/A"
                    # 车位费
                    fee_per_garage = "N/A"
                    # 交通站点
                    traffic_centre = "N/A"
                    # 轨道公交
                    traffic = "N/A"

                item = BuildingItem()
                item["region"] = response.meta["region"]
                item["name"] = name
                item["business"] = business
                item["character"] = character
                item["address"] = address
                item["company"] = company
                item["floor"] = floor
                item["size"] = size
                item["fee"] = fee
                item["height"] = height
                item["garage"] = garage
                item["size_per_floor"] = size_per_floor
                item["fee_per_garage"] = fee_per_garage
                item["traffic_centre"] = traffic_centre
                item["traffic"] = traffic
                item["desc"] = desc
                item["url"] = response.url

                yield item
            else:
                self.driver = webdriver.Chrome()
                self.driver.get(response.url)

                while True:
                    base_elements = self.driver.find_elements_by_xpath("//div[@class='bis_actinfo clearfix']/ul/li")
                    if len(base_elements) > 0:
                        # 物业地址
                        address = self.xml_tag_regax_exp.sub("", base_elements[7].text)
                        # 城区商圈
                        business = self.xml_tag_regax_exp.sub("", base_elements[5].text)
                        # 行业特点
                        character = self.xml_tag_regax_exp.sub("", base_elements[13].text)
                        # 物业名称
                        name = self.xml_tag_regax_exp.sub("", base_elements[1].text)
                        # 物业描述
                        desc = self.xml_tag_regax_exp.sub("",
                                                          self.driver.find_element_by_xpath(
                                                              "//div[@class='tab_detail_item']/p").text)

                        supporting_elements = self.driver.find_elements_by_xpath(
                            "//div[@class='box1 pb3 clearfix']/ul/li")
                        if len(supporting_elements) > 0:
                            # 物管公司
                            company = self.xml_tag_regax_exp.sub("", supporting_elements[1].text)
                            # 楼层状况
                            floor = self.xml_tag_regax_exp.sub("", supporting_elements[3].text)
                            # 总建筑面积
                            size = self.xml_tag_regax_exp.sub("", supporting_elements[5].text)
                            # 物管费
                            fee = self.xml_tag_regax_exp.sub("", supporting_elements[7].text)
                            # 标准层高
                            height = self.xml_tag_regax_exp.sub("", supporting_elements[9].text)
                            # 车位数量
                            garage = self.xml_tag_regax_exp.sub("", supporting_elements[13].text)
                            # 标准层面积
                            size_per_floor = self.xml_tag_regax_exp.sub("", supporting_elements[15].text)
                            # 车位费
                            fee_per_garage = self.xml_tag_regax_exp.sub("", supporting_elements[19].text)
                            # 交通站点
                            traffic_centre = self.xml_tag_regax_exp.sub("", supporting_elements[25].text)
                            # 轨道公交
                            traffic = self.xml_tag_regax_exp.sub("", supporting_elements[27].text)
                        else:
                            company = "N/A"
                            # 楼层状况
                            floor = "N/A"
                            # 总建筑面积
                            size = "N/A"
                            # 物管费
                            fee = "N/A"
                            # 标准层高
                            height = "N/A"
                            # 车位数量
                            garage = "N/A"
                            # 标准层面积
                            size_per_floor = "N/A"
                            # 车位费
                            fee_per_garage = "N/A"
                            # 交通站点
                            traffic_centre = "N/A"
                            # 轨道公交
                            traffic = "N/A"

                        item = BuildingItem()
                        item["region"] = response.meta["region"]
                        item["name"] = name
                        item["business"] = business
                        item["character"] = character
                        item["address"] = address
                        item["company"] = company
                        item["floor"] = floor
                        item["size"] = size
                        item["fee"] = fee
                        item["height"] = height
                        item["garage"] = garage
                        item["size_per_floor"] = size_per_floor
                        item["fee_per_garage"] = fee_per_garage
                        item["traffic_centre"] = traffic_centre
                        item["traffic"] = traffic
                        item["desc"] = desc
                        item["url"] = response.url

                        yield item
                        break
                    else:
                        pass
                self.driver.close()
        except Exception as e:
            print("Error while parsing url %s " % response.url)

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
