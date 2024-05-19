import scrapy
from scrapy.crawler import CrawlerProcess


class RozetkaSpider(scrapy.Spider):
    name = "rozetka"
    allowed_domains = ["hard.rozetka.com.ua"]
    start_urls = ["https://hard.rozetka.com.ua/ua/monitors/c80089/"]

    BASE_URL = 'https://hard.rozetka.com.ua/'

    def parse(self, response):
        product_urls = response.xpath('/html//a[@class="product-link goods-tile__heading"]/@href').getall()
        for product_url in product_urls:
            yield response.follow(
                product_url,
                callback=self.parse_product_page
            )
        next_link = response.xpath("//a[@title='До наступної сторінки']/@href").get()
        if next_link:
            yield scrapy.Request(url=self.BASE_URL + next_link)

    def parse_product_page(self, response):
        comments_url = response.xpath('/html//a[@class="product__rating-reviews ng-star-inserted"]/@href').get()
        if comments_url:
            yield response.follow(comments_url, callback=self.parse_comment_page)

        yield {
            'title': response.xpath('/html//p[@class="product__title-left h1 product__title-collapsed ng-star-inserted"]/text()').get(),
            'old_price': response.xpath('/html//p[@class="product-price__small ng-star-inserted"]/text()').get(default='0').replace(u'\xa0', u''),
            'current_price': response.xpath('/html//p[@class="product-price__big"]/text()').get(default='0').replace(u'\xa0', u''),
        }

    def parse_comment_page(self, response):
        # TODO: add parsing for reviews
        for review in response.xpath('/html//li[@class="product-comments__list-item ng-star-inserted"]'):
            print(review.xpath('div[@class="comment__body"]/text()').get())

if __name__ == '__main__':
    process = CrawlerProcess()
    # spider = RozetkaSpider()
    process.crawl(RozetkaSpider)
    process.start()
