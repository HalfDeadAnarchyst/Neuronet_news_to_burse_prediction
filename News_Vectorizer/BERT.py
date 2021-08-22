import numpy as np
import pandas as pd
import requests
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("bankiru.csv")
df = df[["review", "score"]]
df = df[df["score"] != "Без оценки"]
df["review"] = df["review"].str.strip()
df["score"] = df["score"].astype(int)

matrix = np.zeros(shape=(8773, 768))

batch_size = 32
i = 0
while i < df.shape[0]:
    batch_start = i * batch_size
    batch_end = i * batch_size + batch_size
    print(f"{i:5}, {batch_start:5}, {batch_end:5}", end="\r")
    values = df.values[batch_start: batch_end]
    values = values[:, 0]
    texts = list(values)
    response = requests.post("https://data.iori.ranepa.ru/api/bert/encode",
                             json={"texts": texts, "infinite_texts": False},
                             headers={"Authorization": API_KEY})
    matrix[batch_start: batch_end] = response.json()["result"]
    sleep(1)
    i += 1

X_train, X_test, Y_train, Y_test = train_test_split(matrix, df["score"].values, test_size=0.2)
clf = LogisticRegression(random_state=0, multi_class="multinomial", penalty="l2", solver="lbfgs").fit(X_train, Y_train)

clf.score(X_test, Y_test)