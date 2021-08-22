import requests
from lxml import etree
from io import StringIO, BytesIO
from urllib.parse import urljoin
import dateparser
import csv
import random
from time import sleep
from bs4 import BeautifulSoup

from datetime import datetime, timedelta
import string
from tqdm import tqdm
day_offset = 0


def get_tags(link, text, date):
    r = requests.get(link, timeout=(3.05, 27))
    html = r.text
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)
    tags_list_lxml = tree.xpath('//div[@class="article__tags"]')
    result = []
    for elem in (tags_list_lxml[0]):
        result.append(elem.text)
    # print(result)
    with open('ria_tags.csv', 'a+', encoding='UTF-8') as res_file:
        res_file.write(f'{date}, {text}, {result}\n')
    return result


def news_reader(filename):
    with open(filename, encoding='utf-8') as news_file:
        result = []
        spamreader = csv.reader(news_file)
        for row in tqdm(spamreader):
            if row:
                date_ = (datetime.strptime(row[-1],
                         '%Y-%m-%d %H:%M:%S').date() - timedelta(days=day_offset)).strftime("%d-%m-%Y")
                # print(date, row[1])
                result.append([date_, row[1], get_tags(row[0], row[1], date_)])
                # print(date_, row[1], get_tags(row[0]))
    return result


news_list = news_reader('ria.csv')

