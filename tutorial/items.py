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
    desc = scrapy.Field()
    url = scrapy.Field()

class UrlItem(scrapy.Item):
    region = scrapy.Field()
    url = scrapy.Field()

class BuildingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    region = scrapy.Field()
    address = scrapy.Field()
    character = scrapy.Field()
    size = scrapy.Field()
    fee = scrapy.Field()
    url = scrapy.Field()