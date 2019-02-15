import json, time
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib import error

def airline_url_content(url):
    ntries = 10
    for tries in range(ntries):
        try:
            response = urlopen(url, timeout=20)
            break
        except error.URLError as err:
            print ('ReTry: %s'%url)
            time.sleep(30)
        if tries == ntries -1:
            raise error.URLError('')
    soup = BeautifulSoup(response, "lxml")

    review_id_pointer_start = url.find('-r') + len('-r')
    review_id_pointer_end = url.find('-', review_id_pointer_start)
    review_id = 'review_' + url[review_id_pointer_start:review_id_pointer_end]

    ## extract the general information
    general_information = json.loads(soup.find('script', type="application/ld+json").text)
    # return general_information
    try:
        review_date = general_information['datePublished']
    except:
        try:
            review_date = soup.find('div',{'class':"ui_column is-10-desktop is-12-tablet is-12-mobile"}).find('span',{'class':"ratingDate"})['title']
        except:
            review_date = 'unknown'

    try:
        title = general_information['name']
    except:
        title = 'unknown'

    try:
        content = general_information['reviewBody']
    except:
        content = 'unknown'

    try:
        overall_rating = int(general_information['reviewRating']['ratingValue'])
    except:
        overall_rating = 'unknown'

    #return review_date, title, content, overall_rating

    all_data = soup.find('div',{'id':review_id})
    try:
        stay_date = all_data.find('div',{'class':"prw_rup prw_reviews_stay_date_hsx"}).text
        # remove the blank in the front
        while True:
            if 'Date of travel: ' in stay_date:
                stay_date = stay_date.replace('Date of travel: ','')
            else:
                break
        while True:
            if stay_date[0] == ' ':
                stay_date = stay_date[1:]
            else:
                break

    except:
        stay_date = ''

    #return review_date, title, content, overall_rating, stay_date

    ## ranking part
    ranking_dict = dict()
    try:
        table = all_data.find_all('li',{'class':"recommend-answer"})
        for rating in table:
            rate = str(rating.select('div[class*="ui_bubble_rating bubble_"]'))
            rate_pointer_start = rate.find('<div class="ui_bubble_rating bubble_') + len('<div class="ui_bubble_rating bubble_')
            rate_pointer_end = rate.find('"></div>',rate_pointer_start)
            rate = rate[rate_pointer_start:rate_pointer_end]
            try:
                rate_mark = int(str(rate))/10
            except:
                rate_mark = str(rate)
            label = rating.find('div',{'class':"recommend-description"}).text
            ranking_dict[label] = rate_mark
    except:
        pass


    #return review_date, title, content, overall_rating, stay_date, ranking_dict

    ## review information
    try:
        reviewer_name = all_data.find('div',{'class':"username mo"}).text
    except:
        reviewer_name = 'unknown'

    try:
        reviewer_contributions = all_data.find('span',{'class':"badgetext"}).text
        try:
            reviewer_contributions = int(reviewer_contributions)
        except:
            pass
    except:
        reviewer_contributions = 'unknown'

    try:
        reviewer_location = soup.find('div',{'class':"location"}).text
    except:
        reviewer_location = 'unknown'


    return review_date, title, content, overall_rating, stay_date, ranking_dict, reviewer_name, reviewer_contributions, reviewer_location


if __name__ == "__main__":
    import random
    test_url_1 = "https://www.tripadvisor.com/ShowUserReviews-g1-d8728993-r548879571-Air_Algerie-World.html#REVIEWS"
    test_url_2 = "https://www.tripadvisor.com/ShowUserReviews-g1-d8728993-r543060306-Air_Algerie-World.html#REVIEWS"
    test_url_3 = "https://www.tripadvisor.com/ShowUserReviews-g1-d8728993-r651235255-Air_Algerie-World.html#REVIEWS"

    test_url_list = [test_url_1, test_url_2, test_url_3]

    test_url = random.choice(test_url_list)

    review_date, title, content, overall_rating, stay_date, ranking_dict, reviewer_name, reviewer_contributions, reviewer_location = airline_url_content(test_url)

    print('\n\nFrom testing URL: %s\n\n' % test_url)

    print('review date: ', review_date)
    print('review title: ', title)
    print('review content: ', content)
    print('overall rating: ', overall_rating)
    print('Stay date: ', stay_date)
    print('Rating Table: ', ranking_dict)
    print('Reviewer Name:', reviewer_name)
    print('Reviewer Contributions:', reviewer_contributions)
    print('Reviwer Location:', reviewer_location)