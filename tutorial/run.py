# -*- coding: utf-8 -*-

from scrapy import cmdline

if __name__ == "__main__":
    # name = "hz58"
    # name = "hzzje"
    name = "o571"
    cmd = "scrapy crawl {0}".format(name)
    cmdline.execute(cmd.split())