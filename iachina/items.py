# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IachinaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    insurance_type=scrapy.Field()
    company_name=scrapy.Field()
    product_type=scrapy.Field()
    product_name=scrapy.Field()
    clause_name=scrapy.Field()
    clause_url=scrapy.Field()
    content=scrapy.Field()

