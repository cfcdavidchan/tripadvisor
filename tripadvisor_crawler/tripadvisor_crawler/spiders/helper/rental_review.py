from bs4 import BeautifulSoup
import time, re, random
from urllib.request import urlopen
from urllib import error




def rental_url_content(reviewer_url, review_code):
	review_code = 'review_' + review_code

	ntries = 10
	for tries in range(ntries):
		try:
			response = urlopen(reviewer_url, timeout=20)
			break
		except error.URLError as err:
			print('ReTry: %s' % reviewer_url)
			time.sleep(30)
		if tries == ntries - 1:
			raise error.URLError('')

	soup = BeautifulSoup(response, "html5lib")
	soup = soup.find('div', {'id': str(review_code)})

	# soup = BeautifulSoup(html, "html5lib")
	# review data
	try:
		title = str(soup.find('div', {'class': "quote vrClickTestQuote"}).text)
	except:
		title = 'unknown'

	try:
		content = soup.find('div', {'class': "entry vrReviewText"}).find('span').text.replace('\n', '')
	except:
		content = 'unknown'

	try:
		overall_rating_string = ' '.join(
			soup.find('div', {'class': "rating reviewItemInline"}).select('span[class*="ui_bubble_rating bubble_"]')[
				0].get('class'))
		overall_rating = int(overall_rating_string[overall_rating_string.find('ui_bubble_rating bubble_') + len(
			'ui_bubble_rating bubble_'):]) / 10
	except:
		overall_rating = 'unknown'

	try:
		date = soup.find('div', {'class': "rating reviewItemInline"}).find('span', {'class': "ratingDate"}).get_text()

		if date.find("Reviewed") >= 0:
			if date.find('for a stay in ') < 0:
				review_date = date[date.find("Reviewed ") + len('Reviewed '):]
			else:
				review_date = date[date.find("Reviewed ") + len('Reviewed '):date.find("\nfor a stay")]
		else:
			review_date = 'unknown'

		if date.find('for a stay in '):
			stay_date = date[date.find("or a stay in ") + len('or a stay in '):].replace("\n", "")

		else:
			stay_date = 'unknown'
	except:
		review_date = 'unknown'
		stay_date = 'unknown'

	ranking_dict = dict()

	try:
		ranking_table = soup.find('table', {'class': "vrReviewRatings"}).findAll('td')
		for detail in ranking_table:
			label = detail.find('span', {'class': 'vrReviewRatingLabel'}).get_text()
			rank = ' '.join(detail.select('span[class*="ui_bubble"]')[0].get('class'))
			rank = int((rank[rank.find('ui_bubble_rating bubble_') + len('ui_bubble_rating bubble_'):])) / 10

			ranking_dict[label] = rank
	except:
		pass

	try:
		traveling_type = 'unknown'
		all_div = soup.select('div')
		for div in all_div:
			if div.find('span', {'class': 'vrReviewItem itemLabel'}) and (
			div.find('span', {'class': 'vrReviewItem itemLabel'}).text) == "Traveling group:":
				if div.div:
					traveling_type = str(div.div.select('span[class="vrReviewItem"]')[0].text)
					break

	except:
		traveling_type = 'unknown'

	# reviewer data
	try:
		reviewer_name = soup.find('div', {'class': "username mo"}).text.replace('\n', '')
	except:
		reviewer_name = 'unknown'

	try:
		reviewer_location = soup.find('div', {'class': "location"}).text.replace('\n', '')
		if reviewer_location == '':
			reviewer_location = 'unknown'
	except:
		reviewer_location = 'unknown'

	try:
		reviewer_contributions = int(re.sub("[^0-9]", "", soup.find('div', {'class': "reviewerBadge badge"}).span.text))
	except:
		reviewer_contributions = 'unknown'

	return title, content, overall_rating, review_date, stay_date, ranking_dict, traveling_type, reviewer_name, reviewer_contributions, reviewer_location


if __name__ == "__main__":
	test_url_1 = 'https://www.tripadvisor.com/ShowUserReviews-g60654-d1902662-r588183824-Ko_Olina_Beach_Villa_OT1404_Penthouse_Full_Ocean-Kapolei_Oahu_Hawaii.html'
	review_code_1 = '588183824'

	test_url_2 = 'https://www.tripadvisor.com/ShowUserReviews-g60654-d1902662-r492340572-Ko_Olina_Beach_Villa_OT1404_Penthouse_Full_Ocean-Kapolei_Oahu_Hawaii.html'
	review_code_2 = '492340572'

	test_url_3 = 'https://www.tripadvisor.com/ShowUserReviews-g60654-d1902662-r403901696-Ko_Olina_Beach_Villa_OT1404_Penthouse_Full_Ocean-Kapolei_Oahu_Hawaii.html'
	review_code_3 = '403901696'

	test_pair = [[test_url_1, review_code_1], [test_url_2, review_code_2], [test_url_3, review_code_3]]

	pair = random.choice(test_pair)

	title, content, overall_rating, review_date, stay_date, ranking_dict, traveling_type, reviewer_name, reviewer_contributions, reviewer_location = rental_url_content(
		pair[0], pair[1])

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