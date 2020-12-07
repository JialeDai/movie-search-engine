import pymongo
import datetime
from selenium import webdriver
from time import sleep
import requests
from lxml import etree
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
import re
import sys
import time


detaillinklist=[]
doubanratinglist=[]
commentlist=[]
client = pymongo.MongoClient("mongodb+srv://DJL:Djl123456@cluster0-ywxjv.azure.mongodb.net/test?retryWrites=true&w=majority")
db = client['film_web']
catalog_films = db['catalog_films']
result = catalog_films.find(no_cursor_timeout=True, batch_size=5)
# print(list(result)) , batch_size=5

# db_new = client['film_web']
# catalog_films = db['catalog_films']
for each in result:
    if "Douban" in each.keys():
        # if "doubanLink" in each["Douban"].keys():
        #     pass
        # else:
        #     driver = webdriver.PhantomJS(r'D:\\VSCode\\phantomjs-2.1.1-windows\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
        #     driver.get("https://movie.douban.com/")
        #     driver.find_element_by_xpath("//*[@id='inp-query']").send_keys(each['title'])
        #     sleep(6)
        #     driver.find_element_by_xpath("//*[@id='db-nav-movie']/div[1]/div/div[2]/form/fieldset/div[2]/input").click()
        #     try:
        #         WebDriverWait(driver,4).until(expected_conditions.title_contains(each['title']))
        #         bsobj = BeautifulSoup(driver.page_source,features="lxml")
        #         detaillink = bsobj.find('a',{'class':'title-text'})['href']
        #     except:
        #         detaillink = 'no results'
        #     finally:
        #         db.catalog_films.update({'title':each['title']},{'$set':{"Douban":{"rating":each["Douban"]["rating"],"doubanLink":detaillink}}})
        #         driver.close
        pass
    else:
        driver = webdriver.PhantomJS(r'D:\\VSCode\\phantomjs-2.1.1-windows\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
        driver.get("https://movie.douban.com/")
        driver.find_element_by_xpath("//*[@id='inp-query']").send_keys(each['title'])
        sleep(6)
        driver.find_element_by_xpath("//*[@id='db-nav-movie']/div[1]/div/div[2]/form/fieldset/div[2]/input").click()
        try:
            WebDriverWait(driver,4).until(expected_conditions.title_contains(each['title']))
            bsobj = BeautifulSoup(driver.page_source,features="lxml")
            douban = float(bsobj.find('span',{'class':'rating_nums'}).text)
            detaillink = bsobj.find('a',{'class':'title-text'})['href']
            print(douban)
            print(detaillink)
        except:
            douban = -1
            detaillink = 'no results'
            print (douban)
        finally:
            db.catalog_films.update({'title':each['title']},{'$set':{"Douban":{"rating":douban,"doubanLink":detaillink}}})
            driver.close

    
    