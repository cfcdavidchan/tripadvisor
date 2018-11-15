import scrapy, os, csv, json
from bs4 import BeautifulSoup
from urllib.request import urlopen
from .helper.rental_review import rental_url_content
import re
from scrapy import Request

class retnalsSpider(scrapy.Spider):
	name = 'tripadvisor_rental'

	def __init__(self, *args, **kwargs):
		super(retnalsSpider, self).__init__(*args, **kwargs)
		self.start_urls = [kwargs.get('start_url')]

		# create hotel_data directory
		if not os.path.exists('rental_data'):
			os.makedirs('rental_data')

		# # find the rentals name
		response = urlopen(self.start_urls[0], timeout=20)
		soup = BeautifulSoup(response, "html5lib")
		rental_name = str(json.loads(soup.find('script', {'type': "application/ld+json"}).text)['name']).replace(" ",
		                                                                                                         "_")

		rental_name = re.sub(r"[^A-Za-z]+", '', rental_name)
		#self.start_urls = ['https://www.tripadvisor.com' + str(soup.find('div',{'class':'quote'}).find('a',href=True)['href'])]

		# create directory for the hotel
		if not os.path.exists('rental_data/%s' % rental_name):
			os.makedirs('rental_data/%s' % rental_name)

		#create csv for the hotel
		csv_name = '%s_all_data.csv' % rental_name
		self.csv_path = 'rental_data/%s/%s' % (rental_name, csv_name)

		with open(self.csv_path, 'w') as csvfile:
			filewriter = csv.writer(csvfile, delimiter="\t", quotechar='|', quoting=csv.QUOTE_MINIMAL)
			filewriter.writerow(
				['review URL', 'review date', 'review title', 'review content', 'overall rating', 'stay date',
				 'traveling type', 'rating', 'reviewer name', 'reviewer contributions', 'reviewer location'])


	def parse(self, response):
		## find hotel name
		# if self.rental_name == '':
		# 	print ('/n url /n/n')
		# 	print (response.url)
		# 	response = urlopen(response.url, timeout=20)
		# 	soup = BeautifulSoup(response, "html5lib")
		# 	self.rental_name = str(json.loads(soup.find('script', {'type': "application/ld+json"}).text)['name']).replace(" ","_")
		# 	self.rental_name = re.sub(r"[^A-Za-z]+", '',self.rental_name)
		#
		# 	# # create directory for the hotel
		# 	if not os.path.exists('rental_data/%s' % self.rental_name):
		# 		os.makedirs('rental_data/%s' % self.rental_name)
		# 	#create csv for the hotel
		# 	csv_name = '%s_all_data.csv' % self.rental_name
		# 	self.csv_path = 'rental_data/%s/%s' % (self.rental_name, csv_name)
		#
		# 	with open(self.csv_path, 'w') as csvfile:
		# 		filewriter = csv.writer(csvfile, delimiter="\t", quotechar='|', quoting=csv.QUOTE_MINIMAL)
		# 		filewriter.writerow(
		# 			['review URL', 'review date', 'review title', 'review content', 'overall rating', 'stay date',
		# 			 'traveling type', 'rating', 'reviewer name', 'reviewer contributions', 'reviewer location'])
		#
		#
		#
		reviews = response.xpath('//div[contains(@class, "reviewSelector")]').extract()

		soup = [BeautifulSoup(html, "html5lib") for html in reviews]

		print ('\n\n\n\n\n\n')
		for review in soup:
			url =  'https://www.tripadvisor.com' + str(review.find('div',{'class':'quote'}).find('a',href=True)['href'])
			review_code = review.select('div[class*="reviewSelector"]')[0].get('data-reviewid')
			print ('url:%s'%url)
			print ('review_code:%s'%review_code)
			title, content, overall_rating, review_date, stay_date, ranking_dict, traveling_type, reviewer_name, reviewer_contributions, reviewer_location = rental_url_content(
				url, review_code)
			print('review date: ', review_date)
			print('review title: ', title)
			print('review content: ', content)
			print('overall rating: ', overall_rating)
			print('Stay date: ', stay_date)
			print('traveling type: ', traveling_type)
			print('Rating Table: ', ranking_dict)
			print('Reviewer Name:', reviewer_name)
			print('Reviewer Contributions:', reviewer_contributions)
			print('Reviwer Location:', reviewer_location)
			print ('\n')

			with open(self.csv_path, 'a') as csvfile:
				filewriter = csv.writer(csvfile, delimiter="\t", quotechar='|', quoting=csv.QUOTE_MINIMAL)
				filewriter.writerow(
					[url, review_date, title, content, overall_rating, stay_date, traveling_type, ranking_dict,
					 reviewer_name, reviewer_contributions, reviewer_location])

		print('\n\n\n\n\n\n')
		next_page = response.xpath('//div[@class = "prw_rup prw_common_north_star_pagination responsive"]/div[@class = "unified ui_pagination north_star "]/a[@class = "nav next taLnk ui_button primary"]/@href').extract_first()
		#
		#
		#
		url_init = 'https://www.tripadvisor.com'
		#
		if next_page is not None:
			next_page = url_init + next_page
			print('\n\n\n\n\n\n')
			print('next page:%s' % next_page)
			print('\n\n\n\n\n\n')
			yield response.follow(next_page)

