# -*- coding: utf-8 -*-
from scrapy.exporters import CsvItemExporter
from datetime import datetime
import codecs


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

def create_valid_csv(self, item):
    for key, value in item.items():
        item[key] = value.encoding("utf-8")


class TutorialPipeline(object):
    def __init__(self):
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.file = open("output_%s_.csv" % date_str, 'w')
        # self.file = codecs.open("output_%s_.csv" % date_str, 'w', "utf-8")
        self.exporter = CsvItemExporter(self.file, encoding="utf-8")
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        # create_valid_csv(item)
        for key, value in item.items():
            if isinstance(value, str):
                # print "####################   UNICODE   ##################"
                item[key] = value.encode("utf-8")
                print(value.encode("utf-8"))
            else:
                item[key] = value.decode("ascii").encode("utf-8")
                print(value.decode("ascii").encode("utf-8"))
                # print "####################   STR   ##################"
                # pass

        self.exporter.export_item(item)

        return item
