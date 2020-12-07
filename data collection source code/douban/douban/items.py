# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    rating_num = scrapy.Field()
    quote = scrapy.Field()
    next_url = scrapy.Field()
    image = scrapy.Field()
    # list_url = scrapy.Field()
    movie_name = scrapy.Field()
    movie_discrpiton = scrapy.Field() 
    movie_writer = scrapy.Field()
    movie_roles = scrapy.Field()
    movie_language = scrapy.Field()
    movie_date = scrapy.Field()
    movie_long = scrapy.Field()
    