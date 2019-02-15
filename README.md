# Natural Language Processing for tripadvisor.com

## Description
This is a Natural Language Processing(NLP) project of analysing review data from [Tripadvisor.com](https://www.tripadvisor.com/). In this project, we could like to know whether the reviewing behaviors or rating preference will be different amoung different types of travelers.

There are two main parts of the entire project.
  1. [Web-crawler](https://github.com/cfcdavidchan/tripadvisor#web-crawler)

  [Python-scrapy](https://scrapy.org/) library will be used to develop a web-crawler in order to download and extract the review data from Tripadvisor.com

  2. [Natural Language Processing](https://github.com/cfcdavidchan/tripadvisor#Natural-Language-Processing)

  Applying natural language processing to extract the insight from downloaded data.

## Installation
[Python 3.5.6](https://www.python.org/downloads/release/python-356/)

Library pre-install

* `pip install -r requirement.txt`

## Web-crawler

Getting into the root directory of scrapy.

* `cd tripadvisorSpider_crawler/`

Two types of data can be crawled by this script, which are Hotel review and rental Vacation review. Different command wil be used because the web page structures are different.

For hotel review:
* `scrapy crawl scrapy crawl tripadvisor_hotel -a start_url="TARGET URL"`

For rental vacation:
* `scrapy crawl scrapy crawl tripadvisor_rental -a start_url="TARGET URL"`


After running the code `hotel_data` or `rental_data` directoy will be created under the root directory of scrapy. Then, the review data will be stored into a csv file.


###### Bonus
`run_spider.py` inside `tripadvisor_crawler` can be used in order to crawl review by reading a list of url from csv.

things need to be awared when using `run_spider.py`
  1. Conda virtual environment, called jing_jing, is set as default in this script. Please change the command `source activate jing_jing` to the related virtual environment if it is needed

  2. Please change the type of data is going to be crawled initally. If hotel review need to be crawled please change `hotel_data = True` in the script, vice versa.

  3. Plese change `csv_filename` to the target csv and the csv should be placed at tripadvisor_crawler directory as default.


*Note:*   The Target url should be the hotel or rental vacation page from tripadvisor, such as [Exmaple 1](https://www.tripadvisor.com/Hotel_Review-g60982-d87011-Reviews-Prince_Waikiki-Honolulu_Oahu_Hawaii.html), [Example 2](https://www.tripadvisor.com/Hotel_Review-g60982-d1818106-Reviews-The_Modern_Honolulu-Honolulu_Oahu_Hawaii.html), [Example 3](https://www.tripadvisor.com/VacationRentalReview-g60982-d1739906-The_Bird_Cage_Waikiki_Hideaway_free_wi_fi-Honolulu_Oahu_Hawaii.html) or [Example 4](https://www.tripadvisor.com/VacationRentalReview-g60647-d4801464-Sunset_Beach_on_the_beach_near_the_Banzai_Pipeline-Haleiwa_Oahu_Hawaii.html)

## Natural Language Processing

Download the nltk language database

  * `python -m nltk.downloader all`



1.  Word frequence counter:

  In this part, the script will read all the csv first. Then, the word in review will be splited word by word. Finally, word counting will be started before stop words and symbol will be deleted. 

  1.1 Create a directory inside analysis directory. Let's say it is named as `hotel_data`

  1.2 Place all the csv inside the directory (`hotel_data`)

  1.3 Run `juputer notebook` and open `word_analysis.ipynb` inside analysis csv_directory

  1.4 Change variable `data` inside the notebook as the directory name that just created(`hotel_data`)

  1.5 Change the code in the last cell, `"ascending_wordcount_pd.to_csv(csv_name,index=False)"`, where csv_name should be the name of csv file that saves the word counting result.

  1.6 Run all the cells in the notebook
