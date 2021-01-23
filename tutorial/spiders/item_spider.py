import scrapy


class ItemSpider(scrapy.Spider):
    name = "item" # 크롤링 제목

    def start_requests(self): # 어떤 웹사이트에서 수집할지 정의하는 역할
        urls = [
            'https://algumon.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response): # 응답 중 어떤 부분을 크롤링할지 정하는 것
        itemLists = response.css('ul.product > li')
        item = {}
        for itemlist in itemLists:
            item['name'] = itemlist.css('span.item-name > a::text').get().strip()
            item['link'] = "https://algumon.com" + itemlist.css('.item-name > a ::attr(href)').get()
            item['image'] = itemlist.css('div > a > img::attr(src)').get()
            item['price'] = itemlist.css('p.deal-price-info > small::text').getall()
            item['site'] = itemlist.css('span.site::text').get()
            yield item
