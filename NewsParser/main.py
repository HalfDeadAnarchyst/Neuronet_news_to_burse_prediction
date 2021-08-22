import requests
from lxml import etree
from io import StringIO, BytesIO
from urllib.parse import urljoin
import dateparser
import csv
import random
from time import sleep


def get_content(html):
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(html), parser)
    items = tree.xpath('//div[@id="historicalTableData"]')
    for item in items:
        #i = item.xpath('div[@class="list-item__content"]/a[contains(@class,"list-item__title")]')[0]
        #date_ = item.xpath('div[@class="list-item__info"]/div[contains(@class,"list-item__date")]')[0]
        yield item.text


def get_next_url(html):
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(html), parser)
    link = tree.xpath('//*[@class="list-items-loaded"]')[0].get("data-next-url")
    return urljoin("https://ria.ru/economy/", link)


def proc_content(html, writer):
    for item in get_content(html):
        writer.writerow([item])
        print(item)


r = requests.get("https://agsi.gie.eu/#/historical/NL", timeout=(3.05, 27))
parser = etree.HTMLParser()
tree   = etree.parse(StringIO(r.text), parser)
# next_url = 'https://ria.ru/services/economy/more.html?id=112627457&date=20080630T215434'

with open('output4.csv', 'w+', encoding="utf-8") as f:
    writer = csv.writer(f)
    # proc_content(r.text, writer)
    html = r.text
    print(html)
    proc_content(html, writer)