import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes" # 크롤링 제목

    def start_requests(self): # 어떤 웹사이트에서 수집할지 정의하는 역할
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response): # 응답 중 어떤 부분을 크롤링할지 정하는 것
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')