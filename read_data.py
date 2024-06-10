import pandas as pd
import matplotlib.pyplot as plt

data = pd.DataFrame()
data = pd.read_csv('spam_or_not_spam.csv', sep=',', names = ['message', 'label'])
data = data.dropna(axis=0, how="any")
data['label'] = data['label'].astype(int)

len(data)
data['length'] = data['message'].apply(len)

plt.xlabel('длина сообщения')
plt.ylabel('количество')
data['length'].hist(bins=100, edgecolor='black', figsize=(10,5))

data.hist(column='length',by='label',bins=60,figsize=(12,5),
              edgecolor='black')