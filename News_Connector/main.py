from vectorizer import get_sentence_color, tokenizer
import csv
from datetime import datetime, timedelta
from tqdm import tqdm

day_offset = 0


def news_reader_ndate(filename):
    with open(filename, encoding='utf-8') as news_file:
        result = []
        spamreader = csv.reader(news_file)
        for row in spamreader:
            if row:
                result.append([row[0], row[1]])
    return result


def news_reader(filename):
    with open(filename, encoding='utf-8') as news_file:
        result = []
        spamreader = csv.reader(news_file)
        for row in spamreader:
            if row:
                date_ = (datetime.strptime(row[-1], '%Y-%m-%d %H:%M:%S').date() - timedelta(days=day_offset)).strftime("%d-%m-%Y")
                # print(date, row[1])
                result.append([date_, row[1]])
    return result


def get_color(filename):
    with open(filename, encoding='utf-8') as news_file:
        result = []
        spamreader = csv.reader(news_file)
        rows = []
        for row in spamreader:
            rows.append(row)
        for i in range(2, len(rows)):
            date_ = datetime.strptime(rows[i][2], '%d/%m/%y').date().strftime("%d-%m-%Y")
            if (float(rows[i][7]) - float(rows[i-1][7])) > 0:
                # print(rows[i][0], rows[i][2], 1)
                result.append([rows[i][0], date_, 1])
            else:
                # print(rows[i][0], rows[i][2], 0)
                result.append([rows[i][0], date_, 0])
    return result


def concantenator(db, table):
    result = []
    for db_name, db_date, db_color in tqdm(db):
        for table_date, table_text in table:
            if db_date == table_date:
                result.append([table_date, db_name, db_color, table_text, get_sentence_color(tokenizer(table_text))])
                # print([table_date, db_name, db_color, table_text])
    return result


blue_fish_db = get_color('blue_fish.csv')
mos_birzsh_db = get_color('mos_birzsh.csv')
rts_db = get_color('rts.csv')
potreb_sector_db = get_color('potreb_sector.csv')
all_db = blue_fish_db + mos_birzsh_db + rts_db + potreb_sector_db

# tass_table = news_reader('tass.csv')
# ria_table = news_reader("ria.csv")
# all_tables = tass_table + ria_table
all_tables = news_reader_ndate('results/ria_tagged_covid.csv')

all_res = concantenator(all_db, all_tables)
# for row in all_res:
#     print(row)


with open ("ria_tagged_covid_color.csv", "w", encoding='utf-8') as result_file:
    spamwriter = csv.writer(result_file)
    spamwriter.writerows(all_res)

