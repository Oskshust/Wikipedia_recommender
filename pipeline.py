import wikipedia
import asyncio

import nltk

from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
import pandas as pd
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize

porter = PorterStemmer()

COLUMNS = ["title","summary","links","categories","references"] # todo: add sections

def download_article():
    try:
        return wikipedia.page(title=wikipedia.random(1))
    except:
        return download_article()


def preprocess_article(article):

    try:
        references = "|".join(article.references)
    except KeyError:
        references = ""
    preprocessed_dict = {"title":article.title,"summary":porter.stem(article.summary),"links":"|".join(article.links),"categories":"|".join(article.categories),"references":references}

    try:
        df = pd.read_csv(open("wikipedia.csv",encoding="utf-8"),encoding_errors='ignore').set_index("title")

        df.loc[article.title] = (porter.stem(article.summary),"|".join(article.links),"|".join(article.categories),references)
    except pd.errors.EmptyDataError as e:
        df = pd.DataFrame.from_records([preprocessed_dict],index="title")
    print(df)
    df.to_csv(open("wikipedia.csv",mode="w",encoding="utf-8"))

def pipeline(iterations):
    for i in range(iterations):
        article = download_article()
        print(article.title)
        preprocess_article(article)
# title | contents | links | categories |

pipeline(5)
