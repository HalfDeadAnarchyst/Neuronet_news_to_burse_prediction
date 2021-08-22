# Выполнить эти комманды в консоли питона перед запуском, загрузка модулей nltk
# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')

import csv
import string
import pymorphy2
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import SnowballStemmer
import pandas as pd

# Предварительные настройки
stop_words = stopwords.words("russian")  # nltk загрузка стоп-слов
snowball = SnowballStemmer(language="russian")  # nltk стемматизатор
morph = pymorphy2.MorphAnalyzer(lang='ru')  # Морфический анализатор


#  text = 'В МЭР рассказали о проблемах в реализации совместных проектов с Кубой'


def tokenizer(text):
    result = []
    for element in sent_tokenize(text, language="russian"):  # Токенизация предложения
        tokens = word_tokenize(element, language="russian")  # Токенизация слов
        result_tokens = []
        tokens = [''.join(c for c in s if c not in string.punctuation) for s in tokens]  # удаляем знаки препинания
        tokens = [s for s in tokens if s]  # удаляем пустые элементы
        for token in tokens:
            if token not in stop_words and token != "—" and token != "–":  # удаление стоп-слов и дефисов
                token = morph.parse(token)[0].normal_form  # Нормализация
                token = snowball.stem(token)  # Стемматизация
                result_tokens.append(token)
        result.append(result_tokens)
    #  if len(result) > 1:  # проверка на мультитокеновость
    print(result)
    return result


"""
# Тестовые данные
with open('input.csv', newline='', encoding="UTF-8") as inputfile:
    spamreader = csv.reader(inputfile, delimiter='|')
    for row in spamreader:
        if row:
            linkrow = row[0]
            textrow = row[1]
            daterow = row[2]
            tokenizer(textrow)
            print(linkrow, textrow, daterow)
"""

df = pd.read_csv("input2.csv", error_bad_lines=False, names=["link", "text", "date"])
products_list = df.values.tolist()
for row in products_list:
    if row:
        linkrow = row[0]
        textrow = row[1]
        daterow = row[2]
        tokenized = tokenizer(textrow)
        print(linkrow, textrow, daterow)