# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FootballsignaturesItem(scrapy.Item):
    # define the fields for your item here:
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    full_name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    availability = scrapy.Field()
    size = scrapy.Field()
    product_type = scrapy.Field()
    signed_by = scrapy.Field()
    presentation = scrapy.Field()
    dispatch_time = scrapy.Field()
