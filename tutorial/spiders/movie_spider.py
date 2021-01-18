import scrapy


class MovieSpider(scrapy.Spider):
    name = "movie" # 크롤링 제목

    def start_requests(self): # 어떤 웹사이트에서 수집할지 정의하는 역할
        urls = [
            'https://movie.naver.com/movie/running/current.nhn',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response): # 응답 중 어떤 부분을 크롤링할지 정하는 것
        movie_lists = response.css('ul.lst_detail_t1 > li')
        item = {}
        for movie_list in movie_lists:
            item['title'] = movie_list.css('.tit > a::text').get()
            item['age_limit'] = movie_list.css('.tit > span::text').get()
            item['rating'] = movie_list.css('.star_t1 > a > span.num::text').get()
            item['rating_count'] = movie_list.css('.star_t1 > a > span.num2 > em::text').get()
            item['reservation'] = movie_list.css('.info_exp > dd > .star_t1 > span.num::text').get()
            yield item

