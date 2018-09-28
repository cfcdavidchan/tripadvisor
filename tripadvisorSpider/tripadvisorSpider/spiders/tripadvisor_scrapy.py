import scrapy, os,csv
from .helper.review import url_content
from bs4 import BeautifulSoup
from urllib.request import urlopen


class tripadvisorSpider(scrapy.Spider):
    name = 'tripadvisor'
    #start_urls = [
    #    'https://en.tripadvisor.com.hk/Hotel_Review-g297701-d8293999-Reviews-Mandapa_A_Ritz_Carlton_Reserve-Ubud_Bali.html',
    #]

    def __init__(self, *args, **kwargs):
        super(tripadvisorSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_url')]

        self.number_of_review = 0 
        
        #create hotel_data directory
        if not os.path.exists('hotel_data'):
            os.makedirs('hotel_data')
            
        #find the hotel name
        response = urlopen(self.start_urls[0], timeout=20)
        soup = BeautifulSoup(response, "html5lib")
        hotel_name = soup.find('h1',{'id':"HEADING"}).text.replace(" ","_")
        
        #create directory for the hotel
        if not os.path.exists('hotel_data/%s'%hotel_name):
            os.makedirs('hotel_data/%s'%hotel_name)
 
        # create csv for the hotel
        csv_name = '%s_all_data.csv'%hotel_name
        self.csv_path = 'hotel_data/%s/%s'%(hotel_name,csv_name)
        with open(self.csv_path, 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter="\t",quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(['review URL', 'review date', 'review title','review content', 'overall rating', 'stay date', 'traveling type', 'rating', 'reviewer name', 'reviewer contributions', 'reviewer location'])
            
            
    def parse(self, response):
        url_init = 'https://en.tripadvisor.com.hk'
        
        review_list = []
        for url in response.xpath('//div[contains(@class, "quote")]/a/@href').extract():
            review_list.append(url_init + url)
            
        self.number_of_review += len(review_list)
        
        for url in review_list:
            review_date, title, content, overall_rating, stay_date, traveling_type, ranking_dict, reviewer_name, reviewer_contributions, reviewer_location = url_content(url)
            
            with open(self.csv_path, 'a') as csvfile:
                filewriter = csv.writer(csvfile, delimiter="\t",quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow([url, review_date, title, content, overall_rating, stay_date, traveling_type, ranking_dict, reviewer_name, reviewer_contributions, reviewer_location])
        
        next_page = response.xpath('//div[@class = "prw_rup prw_common_responsive_pagination"]/div[@class = "unified ui_pagination "]/a[@class = "nav next taLnk ui_button primary"]/@href').extract_first()
        
        if next_page is not None:
            next_page = url_init + next_page
            yield response.follow(next_page)