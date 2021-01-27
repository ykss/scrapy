import scrapy
from selenium import webdriver
from item.items import AlgumonItem
import time
from scrapy import Selector


class ItemSpider(scrapy.Spider):
    name = "item" # 크롤링 제목

    def start_requests(self): # 어떤 웹사이트에서 수집할지 정의하는 역할
        urls = [
            'https://algumon.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def __init__(self):
        scrapy.Spider.__init__(self)
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        self.browser = webdriver.Chrome('./chromedriver', chrome_options=options)        

    def parse(self, response): # 응답 중 어떤 부분을 크롤링할지 정하는 것
        self.browser.get(response.url)
        SCROLL_PAUSE_TIME = 2
        # 스크롤 높이
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        cnt = 0
        while True:
            cnt += 1
            # 맨아래까지 스크롤 다운                                   
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # 로딩 기다림
            time.sleep(SCROLL_PAUSE_TIME)                                                
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")  
            time.sleep(SCROLL_PAUSE_TIME)
            # 새로운 높이 계산하고 만약 이전 높이와 같으면 반복 종료           
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height or cnt == 15 :                                                
                break
            last_height = new_height
        html = self.browser.find_element_by_css_selector("body")
        html = self.browser.find_element_by_xpath('//*').get_attribute('outerHTML')
        selector = Selector(text=html)
        itemLists = selector.css('ul.product > li')
        # print("ITEMLIST::", itemLists)
        item = AlgumonItem()
        for itemlist in itemLists:
            item['name'] = itemlist.css('span.item-name > a::text').get().strip()
            item['link'] = "https://algumon.com" + itemlist.css('.item-name > a ::attr(href)').get()
            item['image'] = itemlist.css('div > a > img::attr(src)').get()
            item['price'] = itemlist.css('p.deal-price-info > small::text').get()
            item['site'] = itemlist.css('span.site::text').get()
            yield item
