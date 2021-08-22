import csv
import os

with open('ria_tags2.csv', 'r', encoding='utf-8') as news_file:
    spamreader = csv.reader(news_file, delimiter=',')
    result = []
    for row in spamreader:
        if row:
            while str(row[2])[0:5] != ' http':
                row[1] = row[1] + ',' + row[2]
                row.pop(2)
            result.append([row[0], row[1], row[2], list(row[3:-1])])

files = [x for x in os.listdir('tags_files') if x not in 'results']
for filename in files:
    tags_list = []
    with open('tags_files/' + filename, 'r', encoding='utf-8') as tags_file:
        for line in tags_file.readlines():
            line = line[:len(line) - 1]
            tags_list.append(line)
    # print(tags_list)

    tagged_result = []
    for line in result:
        for elem in line[3]:
            # print(elem)
            if elem in tags_list:
                tagged_result.append(line)
                break

    temp_name = 'tags_files/results/ria_tagged_' + str(filename)[:len(str(filename)) - 4] + '.csv'
    with open(temp_name, 'w+', encoding='utf-8') as output_file:
        writer = csv.writer(output_file)
        for line in tagged_result:
            writer.writerow([line[0], line[1]])

    print([temp_name, len(tagged_result)])
