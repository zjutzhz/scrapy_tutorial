# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from selenium import webdriver
import time
from tutorial.items import GarageItem


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

    def parse(self, response):
        '''
        获取翻页请求数据
        :param response:
        :return:
        '''

        print("loading main page")
        self.driver.get(response.url)
        self.query_url_list.append(response.url)
        while True:
            elements = self.driver.find_elements_by_xpath("//div[@class='pager']/a/span")
            if len(elements) > 0:
                print("page counts: %s" % elements[len(elements) - 2].text)
                for i in range(2, int(elements[len(elements) - 2].text) + 1):
                    url = "http://hz.58.com/cheku/pn%d/" % i
                    self.query_url_list.append(url)
                break
            else:
                pass

        self.driver.close()

        print(self.query_url_list)

        for query_url in self.query_url_list:
            yield Request(url=query_url, callback=self.parse_main, headers=self.headers)

    def parse_main(self, response):
        '''
        用于爬取列表首页
        :param response:
        :return:
        '''

        time.sleep(10)
        lilists = response.xpath("//ul[@class='house-list-wrap']/li")
        for li in lilists:
            try:
                title = li.xpath(".//h2/a/span/text()").extract()[0]
                baseinfo = li.xpath(".//p[@class='baseinfo']/span/text()").extract()
                area = baseinfo[0].strip()
                address = li.xpath(".//p/span/span/text()").extract()[0]
                size = baseinfo[2]
                date_time = li.xpath(".//div[@class = 'time']/text()").extract()[0]
                if len(li.xpath(".//p[@class = 'sum']/span/text()")) == 0:
                    price_day = "na"
                    price_day_unit = "na"
                    price_month = "na"
                    price_month_unit = "na"
                else:
                    price_day = li.xpath(".//p[@class = 'sum']/b/text()").extract()[0]
                    price_day_unit = li.xpath(".//p[@class = 'sum']/span/text()").extract()[0]
                    price_month = li.xpath(".//p[@class = 'unit']/span/text()").extract()[0]
                    price_month_unit = li.xpath(".//p[@class = 'unit']/text()").extract()[1].strip()
                # print("%s, %s, %s, %s, %s, %s, %s, %s, %s " % (
                #     title, area, address, size, date_time, price_day, price_day_unit, price_month, price_month_unit))
                item = GarageItem()
                item["title"] = title
                item["area"] = area
                item["address"] = address
                item["size"] = size
                item["date_time"] = date_time
                item["price_day"] = price_day
                item["price_day_unit"] = price_day_unit
                item["price_month"] = price_month
                item["price_month_unit"] = price_month_unit
                yield item
            except ValueError as e:
                print("Value error", e)
            except Exception as e:
                print(" Unkown error ", e)
