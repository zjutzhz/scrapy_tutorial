# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
    # pass
class BuildingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    region = scrapy.Field()
    name = scrapy.Field()
    business = scrapy.Field()
    character = scrapy.Field()
    address = scrapy.Field()
    company = scrapy.Field()
    floor = scrapy.Field()
    size = scrapy.Field()
    fee = scrapy.Field()
    height = scrapy.Field()
    garage = scrapy.Field()
    size_per_floor = scrapy.Field()
    fee_per_garage = scrapy.Field()
    traffic_centre = scrapy.Field()
    traffic = scrapy.Field()
    desc = scrapy.Field()
    url = scrapy.Field()

class UrlItem(scrapy.Item):
    region = scrapy.Field()
    url = scrapy.Field()

class GarageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # title, area, address, size, date_time, price_day, price_day_unit, price_month, price_month_unit
    title = scrapy.Field()
    area = scrapy.Field()
    address = scrapy.Field()
    size = scrapy.Field()
    date_time = scrapy.Field()
    price_day = scrapy.Field()
    price_day_unit = scrapy.Field()
    price_month = scrapy.Field()
    price_month_unit = scrapy.Field()