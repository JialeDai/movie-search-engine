from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from ..items import DoubanItem
import scrapy
class Douban(scrapy.Spider):
    name='douban'
    start_urls=['https://www.imdb.com/']

    def parse(self,response):
        re_selector = response.xpath('//*[@id="content"]/h1')
        print(re_selector)
        print  (response.body)
        item=DoubanItem()
        selector=Selector(response)
        Movies=selector.xpath('//div[@class="info"]')
        for eachMovie in Movies:
            title=eachMovie.xpath('//div[@class="hd"]/a/span/text()').extract()
            fullTitle = ''
            for each in title:
                fullTitle += each
            movieInfo = eachMovie.xpath('div[@class="bd"]/p/text()').extract()
            star = eachMovie.xpath('div[@class=db]/div@[class="star"]/span[@class="rating=mun"]/text()').extract()[0]
            quote=eachMovie.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            if quote:
                quote=quote[0]
            else:
               quote = ""
            print (fullTitle)
            print (movieInfo)
            print (star)
            print (quote)