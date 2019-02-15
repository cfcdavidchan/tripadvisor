from bs4 import BeautifulSoup
import requests, os, shutil, json
import subprocess


airline_data = dict()
page_number = 1

break_true = False
if os.path.exists('airline_data/'):
    shutil.rmtree('airline_data/')
if not os.path.exists('airline_data/'):
    os.makedirs('airline_data')

while True:
    url = 'https://www.tripadvisor.com/MetaPlacementAjax?placementName=airlines_lander_main&wrap=true&skipLocation=true&page=%d' % page_number
    r  = requests.get(url)

    data = r.text
    soup = BeautifulSoup(data, "lxml")
    all_data = soup.find_all('div',{'class':'prw_rup prw_airlines_airline_lander_card'})
    for html in all_data:
        name = html.find('div',{'class':'airlineName'}).text
        url = html.find('a', {'class': 'detailsLink'})['href']

        if name in airline_data.keys():
            break_true = True
            break

        airline_data[name] = 'https://www.tripadvisor.com' + str(url)

    if break_true:
        break
    page_number += 1
print ('number of airline:  ', len(airline_data))
print (airline_data)
print ('Now Crawling... ... ... ... ... ...')

#virtual environment command
virtual = 'source activate tripadvisor'

# crawler path
path_crawler = '/home/david/coding/tripadvisor/tripadvisor_crawler'



problem_url = dict()

for name, url in airline_data.items():
    print('crawling %s' % name)
    # crawler command
    commnad = 'scrapy crawl tripadvisor_airline -a start_url="%s" -a name="%s"' % (url, name)
    try:
        subprocess.Popen('%s && %s' % (virtual, commnad), shell=True, cwd=path_crawler,
                         executable="/bin/bash").wait()
    except:
        problem_url[name] = url

with open('problem_url.json', 'w') as fp:
    json.dump(problem_url, fp)

