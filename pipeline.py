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
wordnet = WordNetLemmatizer()
COLUMNS = ["title","summary","links","categories","references"] # todo: add sections

def download_article():
    try:
        return wikipedia.page(title=wikipedia.random(1))
    except: #dziwnie ta paczka działa, czasem artykułu nie ma z tytułem który został wylosowany
        return download_article()

def preprocess_article(article):

    title = article.title
    summary = wordnet.lemmatize(porter.stem(article.summary))
    categories = "|".join(article.categories)
    links = "|".join(article.links)
    try:
        references = "|".join(article.references)
    except KeyError:
        references = ""

    try:
        df = pd.read_csv(open("wikipedia.csv",encoding="utf-8"),encoding_errors='ignore').set_index("title")
        df.loc[title] = (summary,links,categories,references)
    except pd.errors.EmptyDataError as e:
        preprocessed_dict = {"title":title,"summary":summary,"links":links,"categories":categories,"references":references}
        df = pd.DataFrame.from_records([preprocessed_dict],index="title")

    df.to_csv(open("wikipedia.csv",mode="w",encoding="utf-8"))

def pipeline(iterations):
    for i in range(iterations):
        article = download_article()
        print(article.title)
        preprocess_article(article)

pipeline(50)
