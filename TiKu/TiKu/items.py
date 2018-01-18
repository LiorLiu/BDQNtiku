# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TikuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id=scrapy.Field()
    #试题图片 id
    answer=scrapy.Field()
    #试题答案
    sort_id=scrapy.Field()
    #试题分类id
