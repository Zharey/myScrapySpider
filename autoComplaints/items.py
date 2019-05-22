# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AutocomplaintsItem(scrapy.Item):

    tspp= scrapy.Field()
    tscx = scrapy.Field()
    tscxing = scrapy.Field()
    tsjs = scrapy.Field()
    tsbw = scrapy.Field()
    tswt = scrapy.Field()
    tsfw = scrapy.Field()
    fwwt = scrapy.Field()
    tssj = scrapy.Field()
    pass
