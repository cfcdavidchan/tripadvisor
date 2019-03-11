import scrapy, os,csv, re
from .helper.airline_review import airline_url_content
import numpy as np
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
                 'Legroom','Seat Comfort','Customer Service', 'Value for Money','Cleanliness','Check-in and Boarding',
                 'Food and Beverage','In-flight entertainment (WiFi, TV, movies)',
                 'reviewer name', 'reviewer contributions', 'reviewer location'])

        for url in self.reviews_url:
            review_date, title, content, overall_rating, stay_date, ranking_dict, reviewer_name, reviewer_contributions, reviewer_location = airline_url_content(
                url)
            rating_summary = []

            if 'Legroom' in ranking_dict:
                rating_summary.append(ranking_dict['Legroom'])
            else:
                rating_summary.append(np.nan)

            if 'Seat Comfort' in ranking_dict:
                rating_summary.append(ranking_dict['Seat Comfort'])
            else:
                rating_summary.append(np.nan)

            if 'Customer Service' in ranking_dict:
                rating_summary.append(ranking_dict['Customer Service'])
            else:
                rating_summary.append(np.nan)

            if 'Value for Money' in ranking_dict:
                rating_summary.append(ranking_dict['Value for Money'])
            else:
                rating_summary.append(np.nan)

            if 'Cleanliness' in ranking_dict:
                rating_summary.append(ranking_dict['Cleanliness'])
            else:
                rating_summary.append(np.nan)

            if 'Check-in and Boarding' in ranking_dict:
                rating_summary.append(ranking_dict['Check-in and Boarding'])
            else:
                rating_summary.append(np.nan)

            if 'Food and Beverage' in ranking_dict:
                rating_summary.append(ranking_dict['Food and Beverage'])
            else:
                rating_summary.append(np.nan)

            if 'In-flight entertainment (WiFi, TV, movies)' in ranking_dict:
                rating_summary.append(ranking_dict['In-flight entertainment (WiFi, TV, movies)'])
            else:
                rating_summary.append(np.nan)



            with open(csv_path, 'a') as csvfile:
                filewriter = csv.writer(csvfile, delimiter="\t", quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow(
                    [url, review_date, title, content, overall_rating, stay_date, rating_summary[0],
                     rating_summary[1], rating_summary[2], rating_summary[3], rating_summary[4],
                     rating_summary[5], rating_summary[6], rating_summary[7],
                     reviewer_name, reviewer_contributions, reviewer_location])