import requests, json, random
from bs4 import BeautifulSoup
from urllib.request import urlopen


def url_content(url):
    response = urlopen(url, timeout=20)
    soup = BeautifulSoup(response, "html5lib")

    
    ## extract the general information
    general_information = json.loads(soup.find('script', type="application/ld+json").text)
    #return general_information
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
    
    ##return review_date, title, content, overall_rating
    
    ## extract the traveling type and date
    stay_info = soup.find('div',{'class':"recommend-titleInline"}).text
    stay_hardcode = 'Stayed: '
    comma_hardcode = ', '    
    stay_date = stay_info[len(stay_hardcode):stay_info.find(',')]
    traveling_type = ''
    traveling_type_table = ['family','couple','solo','business','frined']
    for type_ in traveling_type_table:
        if type_ in stay_info:
            traveling_type = type_
            break
    if traveling_type == '': ## save the whole crwl info if the traveling type cannot be detacted
        try:
            print ('type cannot be detected')
            traveling_type = stay_info[len('travelled as a '):]
        except:
            traveling_type = stay_info
    ##return stay_date, traveling_type
            
    ## ranking part
    star_info = soup.findAll('div',{'class':"ui_column is-10-desktop is-12-tablet is-12-mobile"})
    star_info = star_info[0].findAll('li',{'class':"recommend-answer"})
    
    description = 'ui_bubble_rating bubble_'
    ranking_dict = dict()
    
    if len(star_info) > 0: #only do this when the reviewer provides the rating of each area
        for rate in star_info:
            rate_area = rate.find('div',{'class':"recommend-description"}).text

            pointer = str(rate).find(description) + len('ui_bubble_rating bubble_')
            try:
                rate_mark = int(str(rate)[pointer:pointer+2])/10
            except:
                rate_mark = str(rate)

            ranking_dict[rate_area] = rate_mark
    
    ##return ranking_dict
    
    ## review information
    try:
        reviewer_name = soup.find('div',{'class':"prw_rup prw_reviews_member_info_resp_sur"}).find('div',{'class':"info_text"}).get_text()
    except:
        reviewer_name = 'unknown'
    try:
        reviewer_contributions = int(soup.find('div',{'class':"prw_rup prw_reviews_member_info_resp_sur"}).find('span',{'class':'badgetext'}).get_text())
    except:
        reviewer_contributions = 'unknown'

    try:
        reviewer_location = soup.find('div',{'class':"prw_rup prw_reviews_member_info_resp_sur"}).find('div',{'class':"userLoc"}).get_text()
    except:
        reviewer_location = 'unknown'
    
    #return reviewer_name, reviewer_contributions, reviewer_location
    
    
    
    
    return review_date, title, content, overall_rating, stay_date, traveling_type, ranking_dict, reviewer_name, reviewer_contributions, reviewer_location
    


if __name__ == "__main__":
    test_url_1 = 'https://en.tripadvisor.com.hk/ShowUserReviews-g297701-d603335-r616402936-Viceroy_Bali-Ubud_Bali.html'
    test_url_2 = 'https://en.tripadvisor.com.hk/ShowUserReviews-g297701-d8293999-r618076141-Mandapa_A_Ritz_Carlton_Reserve-Ubud_Bali.html'
    test_url_3 = 'https://en.tripadvisor.com.hk/ShowUserReviews-g297701-d603335-r507151028-Viceroy_Bali-Ubud_Bali.html'

    test_url_list = [test_url_1, test_url_2, test_url_3]

    test_url = random.choice(test_url_list)

    review_date, title, content, overall_rating, stay_date, traveling_type, ranking_dict, reviewer_name, reviewer_contributions, reviewer_location = url_content(test_url) 
    
    print ('\n\nFrom testing URL: %s\n\n'%test_url)
    
    print ('review date: ',review_date)
    print ('review title: ',title)
    print ('review content: ', content)
    print ('overall rating: ', overall_rating)
    print ('Stay date: ',stay_date)
    print ('traveling type: ', traveling_type)
    print ('Rating Table: ', ranking_dict)
    print ('Reviewer Name:', reviewer_name)
    print ('Reviewer Contributions:', reviewer_contributions)
    print ('Reviwer Location:', reviewer_location)
    
    print ('\n')