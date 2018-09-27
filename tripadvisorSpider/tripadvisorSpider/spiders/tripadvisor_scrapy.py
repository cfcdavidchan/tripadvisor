import scrapy

class tripadvisorSpider(scrapy.Spider):
    name = 'tripadvisor'
    #start_urls = [
    #    'https://en.tripadvisor.com.hk/Hotel_Review-g297701-d8293999-Reviews-Mandapa_A_Ritz_Carlton_Reserve-Ubud_Bali.html',
    #]

    def __init__(self, *args, **kwargs):
        super(tripadvisorSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_url')]
        
    def parse(self, response):
        url_init = 'https://en.tripadvisor.com.hk'
        review_list = []
        for url in response.xpath('//div[contains(@class, "quote")]/a/@href').extract():
            review_list.append(url_init + url)
        print ('#####')
        print (review_list)
        print ('#####')
        
        
        #next_page = response.xpath('//div[@class = "prw_rup prw_common_responsive_pagination"]/div[@class = "unified ui_pagination "]/a[@class = "nav next taLnk ui_button primary"]/@href').extract_first()
        
        #self.counting_page()
        #if next_page is not None:
        #    next_page = url_init + next_page
        #    yield response.follow(next_page)