import subprocess, csv

with open('hotel_url.csv') as csvfile:
    rows = csv.reader(csvfile)
    url_list = [row[0] for row in rows]

virtual = 'source activate jing_jing'
path_crawler = '/home/david/coding/tripadvisor/tripadvisorSpider'



for url in url_list:
	print ('crawling %s' %url)
	#subprocess.call('%s && pwd'%virtual, shell=True, cwd=path_crawler, executable="/bin/bash")
	subprocess.Popen('%s && scrapy crawl tripadvisor -a start_url="%s"'%(virtual,url), shell=True, cwd=path_crawler, executable="/bin/bash")
