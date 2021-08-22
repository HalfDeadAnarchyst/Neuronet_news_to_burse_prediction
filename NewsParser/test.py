import requests
from lxml import etree
from io import StringIO
import csv
import multiprocessing as mp
import pandas as pd

from datetime import datetime, timedelta
from tqdm import tqdm

day_offset = 0


def get_tags(link, text, date):
    r = requests.get(link, timeout=(3.05, 27))
    html = r.text
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(html), parser)
    tags_list_lxml = tree.xpath('//div[@class="article__tags"]')
    if len(tags_list_lxml) == 0:
        print(f'ERROR: {r.status_code}')
        return date, text, link, ['NO TAGS, RERUN']
    result = []
    for elem in (tags_list_lxml[0]):
        result.append(elem.text)
    # print(result)
    # with open('ria_tags.csv', 'a+', encoding='UTF-8') as res_file:
    #     res_file.write(f'{date}, {text}, {result}\n')
    return date, text, link, result


def news_reader(filename):
    with open(filename, encoding='utf-8') as news_file:
        spamreader = csv.reader(news_file)
        result = []
        for row in spamreader:
            if row:
                date_ = (datetime.strptime(row[-1],
                                           '%Y-%m-%d %H:%M:%S').date() - timedelta(days=day_offset)).strftime(
                    "%d-%m-%Y")
                result.append([row[0], row[1], date_])
    return result


def gen(link_arr, n):
    for i in range(0, len(link_arr), n):
        temp = link_arr[i:i + n]
        yield temp


# [link, text, date]
if __name__ == '__main__':
    res = news_reader('ria.csv')

    # print(mp.cpu_count())
    with open('ria_tags2.csv', 'a+', encoding='UTF-8') as output_file:
        for el in tqdm(gen(res, 10)):
            pool = mp.Pool(2)
            try:
                output = pool.starmap(get_tags, el)
            except:
                print(f"Error on {el}")
            for line in output:
                output_file.write(f'{line}\n')
            pool.close()
