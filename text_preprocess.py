import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
import string

nltk.download('stopwords')


def loadData():
    messages = pd.read_csv('spam_or_not', sep='\t', names=['label', 'message'])
    messages['length'] = messages['message'].apply(len)

    return messages


def text_process(data):
    nopunc = [c for c in data if c not in string.punctuation]
    nopunc = ''.join(nopunc)

    stemmed = ''
    nopunc = nopunc.split()
    for i in nopunc:
        stemmer = SnowballStemmer('russian')
        stemmed += (stemmer.stem(i)) + ' '

    clean_msgs = [word for word in stemmed.split() if
                  word.lower() not in stopwords.words('russian')]

    return clean_msgs


def main():
    messages = loadData()
    # print(messages)
    messages['processed_msg'] = messages['message'].apply(text_process)

    print(
        '\n################################################## Processed Messages ##################################################\n')
    with pd.option_context('expand_frame_repr', False):
        print(messages)
    # print(messages)

    messages.to_csv('csv files/processed_msgs.csv', encoding='utf-8',
                    index=False)