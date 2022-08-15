import scrapy


class NewsExtractor(scrapy.Spider):
    name = 'news_extractor.com'
    allowed_domains = [
        'www.cbc.ca',
        'www.ctvnews.ca'
    ]
    

    def start_requests(self):
        yield scrapy.Request('https://www.cbc.ca/news', self.parse)
        yield scrapy.Request('https://www.ctvnews.ca', self.parse_ctv)

    
    def parse(self, response):
        for link in response.css("a.card::attr(href)").getall():

            if 'https://www.cbc.ca' in link:
                yield scrapy.Request(url=link, callback=self.parse_author)

            yield scrapy.Request(url='https://www.cbc.ca' + link, callback=self.parse_author) 


    def parse_author(self, response):
        yield {'media': 'cbc', 'title': response.css('h1.detailHeadline::text').get(), 'author': response.css('span.authorText a::text').get()}


    def parse_ctv(self, response):
        for link in response.css("a.c-list__item__link::attr(href)").getall():

            if 'www.ctvnews.ca' in link:
                yield scrapy.Request(url=link, callback=self.parse_ctv_author)

            yield scrapy.Request(url = 'https://www.ctvnews.ca' + link, callback=self.parse_ctv_author)

    
    def parse_ctv_author(self, response):
        title = response.css('h1.c-title__text::text').get()
        author = response.xpath("//a[@class='bio-link-follow']/text()").get()
        if not author:
            author = response.xpath("//div[@class='byline']/text()").get()

        if title:
            yield {'media': 'ctv', 'title': title, 'author': author}