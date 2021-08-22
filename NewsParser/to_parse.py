from tqdm import tqdm
import csv

with open('ria_tags2.csv', 'r', encoding='utf-8') as news_file:
    spamreader = csv.reader(news_file)
    result = []
    for row in spamreader:
        if row:
            result.append([row[0], row[1], row[2], list(row[3:-1])])

tag_dict = dict()

for line in tqdm(result):
    for elem in line[3]:
        if elem in tag_dict:
            tag_dict[elem].append(line)
        else:
            tag_dict[elem] = line

for key in tqdm(tag_dict):
    tag_dict[key] = []

for line in tqdm(result):
    for elem in line[3]:
        if elem in tag_dict:
            tag_dict[elem].append(line)
        else:
            tag_dict[elem] = line

with open('ria_tags3.csv', 'w+', encoding='utf-8') as output_file:
    for key in tqdm(tag_dict):
        output_file.write(f'{key}, {len(tag_dict[key])}\n')
