# Natural Language Processing for tripadvisor.com

## Description
This is a Natural Language Processing(NLP) project of analysing review data from [Tripadvisor.com](https://www.tripadvisor.com/). In this project, we could like to know whether the reviewing behaviors or rating preference will be different amoung different types of travelers.

There are two main parts of the entire project.
  1. [Web-crawler](https://github.com/cfcdavidchan/tripadvisor#web-crawler)

  [Python-scrapy](https://scrapy.org/) library will be used to develop a web-crawler in order to download and extract the review data from Tripadvisor.com

  2. Natural Language Processing

  Applying natural language processing to extract the insight from downloaded data.

## Installation
[Python 3.5.6](https://www.python.org/downloads/release/python-356/)

Library pre-install

* `pip install -r requirements.txt`

## Web-crawler

Getting into the root directory of scrapy.

* `cd tripadvisorSpider/`
* `scrapy crawl tripadvisor -a start_url="TARGET URL"`

After running the code hotel_data directoy will be created under the root directory of scrapy. Then, the review data will be stored into a csv file.

*Note:*   The Target url should be the hotel page from tripadvisor, such as [Exmaple 1](https://www.tripadvisor.com/Hotel_Review-g60982-d87011-Reviews-Prince_Waikiki-Honolulu_Oahu_Hawaii.html), [Example 2](https://www.tripadvisor.com/Hotel_Review-g60982-d1818106-Reviews-The_Modern_Honolulu-Honolulu_Oahu_Hawaii.html) or [Example 3](https://www.tripadvisor.com/Hotel_Review-g297701-d8293999-Reviews-Mandapa_a_Ritz_Carlton_Reserve-Ubud_Bali.html)
