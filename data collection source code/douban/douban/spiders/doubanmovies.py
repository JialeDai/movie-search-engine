import scrapy
from ..items import DoubanItem
from scrapy.http import Request
import requests
from lxml import etree
from googletrans import Translator

detailedLink = []
totallist = []
timelist = []
plotlist = []
imdburllist = []
imdbratinglist = []
class DoubanmoviesSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    offset = 0
    url = 'https://movie.douban.com/top250?start='
    start_urls = [url+str(offset)]
    def parse(self,response):
        item = DoubanItem()
        info = response.xpath("//div[@class='info']")
        counter = 0
        # print(len(info))
        for each in info:
            index = (self.offset%25)
            # item['title'] = each.xpath(".//span[@class='title'][1]/text()").extract()[0]
            # item['content'] = each.xpath(".//div[@class='bd']/p[1]/text()").extract()[0]
            # item['rating_num'] = each.xpath(".//span[@class='rating_num']/text()").extract()[0]
            # item['image'] = each.xpath("//div[@class='item']/div[@class='pic']/a/img/@src").extract()[index]
            # #item['quote'] = each .xpath(".//span[@class='inq']/text()").extract()[0]
            # item['next_url'] = each.xpath(".//*[@class='hd']//a/@href").extract()[0] #ok
            detailedLink.append(each.xpath(".//*[@class='hd']//a/@href").extract()[0])
            #item['list_url'] = 'https://movie.douban.com/top250?start='+str(self.offset)
            #yield scrapy.Request(item['next_url'],callback=self.parse_detail,meta={'item':item})
            # totaldic[each.xpath(".//span[@class='title'][1]/text()").extract()[0]] = {'content':each.xpath(".//div[@class='bd']/p[1]/text()").extract()[0],'rating_num':each.xpath(".//span[@class='rating_num']/text()").extract()[0],'image':each.xpath("//div[@class='item']/div[@class='pic']/a/img/@src").extract()[index]}
            totallist.append({'title':each.xpath(".//span[@class='title'][1]/text()").extract()[0],'content':each.xpath(".//div[@class='bd']/p[1]/text()").extract()[0],'rating_num':each.xpath(".//span[@class='rating_num']/text()").extract()[0],'image':each.xpath("//div[@class='item']/div[@class='pic']/a/img/@src").extract()[index],'dteailed links':each.xpath(".//*[@class='hd']//a/@href").extract()[0]})
            # yield item
            self.offset +=1
            # 249
        if self.offset <=24:
            yield scrapy.Request(self.url+str(self.offset),callback = self.parse)
        print(detailedLink)
        # print(totallist)
        
        translator = Translator()

        for link in detailedLink:
            url = link
            requests.adapters.DEFAULT_RETRIES = 150
            session = requests.session()
            data = requests.get(url,timeout = 20).text
            s = etree.HTML(data)
            session.keep_alive = False
            time = s.xpath("//span[@property='v:runtime']//@content")
            plot = s.xpath("//*[@id='link-report']/span[@property='v:summary']/text()")
            imdburl = s.xpath("//*[@id='info']/a/@href")[0]
            imdburllist.append(imdburl)
            plotlist.append(plot)
            # engplotlist.append(translator.translate(plot[0]).text)
            timelist.append(time)
        print(timelist)
        print(plotlist)
        print(imdburllist)

        for link in imdburllist:
            url = link
            requests.adapters.DEFAULT_RETRIES = 150
            session = requests.session()
            data = requests.get(url,timeout = 20).text
            s = etree.HTML(data)
            session.keep_alive = False
            imdbrating = s.xpath("//*[@id='title-overview-widget']//span[@itemprop='ratingValue']/text()")
            imdbratinglist.append(imdbrating)

        for each in totallist:
            each["time"] = timelist[totallist.index(each)]
        print(imdbratinglist)

        print (totallist)

        # for each in totallist:
        #     item['title'] = each['title']
        #     item['content'] = each['content']
        #     item['rating_num'] = each['rating_num']
        #     item['image'] = each['image']
        #     yield item
   



    # def parse_detail(self,response):#详情页的解析函数
    #     item={}
    #     item = response.meta['item']
    #     print('============================='+item['next_url']+'==============================')
        #item['image'] = response.xpath("//*[@id='mainpic']/a/img/@src").extract()[0] 
    
        # item['name']=detail.xpath('./div/h3/text()').extract_first()
        # item['类别']=detail.xpath('./div/ul/li[1]/text()').extract_first()
        #print(item['类别'])

        # info=detail.xpath('./div/ul/li[2]/text()').extract_first().split('/')
        # #print(info)
        # for i in range(len(info)):
        #     # item['来源']=info[0].replace('\n','').strip()
        #     # item['时长']=info[1].strip()
        
        # yield item
        # yield scrapy.Request(item['list_url'],callback = self.parse,meta = {'itemfromdatail':item})

