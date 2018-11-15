import subprocess, csv
import time
import os

#type of review is going to be crawled
hotel_data = False

if hotel_data == False:
    rental_data = True
else:
    rental_data = False
###

# read the csv
csv_filename = 'rental_url.csv' ## change it if it is needed
csv_path = os.path.join(os.getcwd(), csv_filename)

with open(csv_path) as csvfile:
    rows = csv.reader(csvfile)
    url_list = [row[0] for row in rows]
###

#virtual environment command
virtual = 'source activate jing_jing'
###

# crawler path
path_crawler = '/home/david/coding/tripadvisor/tripadvisor_crawler'
###

#crawler command
if hotel_data == True:
    command = 'scrapy crawl tripadvisor_hotel -a start_url='
if rental_data == True:
    commnad = 'scrapy crawl tripadvisor_rental -a start_url='

#crawl review url by url
problem_url = []
for url in url_list:
	print ('crawling %s' %url)
	#subprocess.call('%s && pwd'%virtual, shell=True, cwd=path_crawler, executable="/bin/bash")
	try:
		subprocess.Popen('%s && %s"%s"'%(virtual, commnad, url), shell=True, cwd=path_crawler, executable="/bin/bash").wait()
	except:
		problem_url.append(url)
###

#write all the problem csv into problem_url.csv
problem_url_csv_path = csv_path = os.path.join(os.getcwd(), 'problem_url.csv')
with open(problem_url_csv_path, 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter="\t", quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for value in problem_url:
        filewriter.writerow([value])
###
