import scrapy, os,csv, re
from .helper.airline_review import airline_url_content
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib import error



class airlineSpider(scrapy.Spider):
    name = 'tripadvisor_airline'

    def __init__(self, *args, **kwargs):
        super(airlineSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_url')]
        self.airline_name = kwargs.get('name')
        self.reviews_url = []

    def parse(self, response):
        all_url = response.xpath('//div[contains(@class, "quote")]/a/@href').extract()
        for url in all_url:
            fullurl = 'https://www.tripadvisor.com' + url
            self.reviews_url.append(fullurl)


        ## checking for next page
        next_page = response.xpath('//div[@class = "unified pagination "]/a[@class = "nav next rndBtn ui_button primary taLnk"]/@href').extract_first()
        if next_page is not None:
            next_page = 'https://www.tripadvisor.com' + next_page
            yield response.follow(next_page)

    def closed(self, spider):
        print ('\n\n\n\n\n\n')
        print (self.reviews_url)
        print (self.airline_name,' has ', len(self.reviews_url), 'reviews in total')
        print('\n\n\n\n\n\n')
        airline_name = re.sub(r"[^A-Za-z]+", '', self.airline_name)

        # create directory for the hotel
        if not os.path.exists('airline_data/%s' % airline_name):
            os.makedirs('airline_data/%s' % airline_name)

        # create csv for the hotel
        csv_name = '%s_all_data.csv' % airline_name
        csv_path = 'airline_data/%s/%s' % (airline_name, csv_name)

        with open(csv_path, 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter="\t", quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(
                ['review URL', 'review date', 'review title', 'review content', 'overall rating', 'stay date',
                 'rating', 'reviewer name', 'reviewer contributions', 'reviewer location'])

        for url in self.reviews_url:
            review_date, title, content, overall_rating, stay_date, ranking_dict, reviewer_name, reviewer_contributions, reviewer_location = airline_url_content(
                url)
            with open(csv_path, 'a') as csvfile:
                filewriter = csv.writer(csvfile, delimiter="\t", quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow(
                    [url, review_date, title, content, overall_rating, stay_date, ranking_dict,
                     reviewer_name, reviewer_contributions, reviewer_location])