import requests
from datetime import datetime
import csv
import random
from time import sleep


def get_content(response):
    for item in response:
        #print(item)
        if item["type"] != "advertising_1" and item["type"] != "advertising_2":
            if "https" not in item["link"]:
                link = "https://tass.ru" + item["link"]
            else:
                link = item["link"]
            text = item["title"] + " "
            if "subtitle" in item:
                if str(item["subtitle"]) != "None":
                    text += str(item["subtitle"])
            if "section" in item:
                section = str(item["section"])
            else:
                section = "no section"
            yield link, text, section


def proc_content(response, writer):
    date_ = datetime.fromtimestamp(response["lastTime"])
    for link, title, section in get_content(response["newsList"]):
        writer.writerow([link, title, section, date_])
        print(f'{link:<55}, {title:<100}, {section:<25}, {date_}')


#  r = requests.get("https://tass.ru/")
timestamp = 1314705600
data = {"limit": 10,"excludeNewsIds":"","timestamp":timestamp}

with open('output3.csv', 'w+', encoding="utf-8") as f:
    writer = csv.writer(f)
    with open('timestamps.txt', "w+", encoding="utf-8") as links:
        try:
            r = requests.post("https://tass.ru/userApi/mainPageNewsList", json=data)
            print(r.json())
            timestamp = r.json()["lastTime"]
            data = {"limit": 10, "excludeNewsIds": "", "timestamp": timestamp}
            proc_content(r.json(), writer)
            links.write(f'{timestamp}\n')
            sleep(random.randint(1, 3))
        except Exception() as e:
            with open('debug.txt', "a", encoding="utf-8") as d:
                d.write(f'{e}\n{timestamp}\n{r.json()}\n\n')