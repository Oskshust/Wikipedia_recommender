import wikipedia

from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import pandas as pd
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from nltk.corpus import stopwords
porter = PorterStemmer()
wordnet = WordNetLemmatizer()
COLUMNS = ["title","summary","content","links","categories","references"] # todo: add sections

def download_article():
    try:
        return wikipedia.page(title=wikipedia.random(1))
    except: # sometimes the package can't find the article but the title is a random title from the list of articles
        return download_article()


def preprocess_article(article):

    title = article.title
    summary = wordnet.lemmatize(porter.stem(article.summary))
    content =wordnet.lemmatize(porter.stem(article.content))
    content = " ".join([word for word in content.split() if word not in set(stopwords.words('english'))])

    categories = "|".join(article.categories)
    links = "|".join(article.links)
    try:
        references = "|".join(article.references)
    except KeyError:
        references = ""
    return title,summary,content,links,categories,references
def save_article(title,summary,content,links,categories,references):
    try:
        df = pd.read_csv(open("wikipedia2.csv",encoding="utf-8"),encoding_errors='ignore').set_index("title")
        df.loc[title] = (summary,content,links,categories,references)
    except pd.errors.EmptyDataError as e:
        preprocessed_dict = {"title":title,"summary":summary,"content":content,"links":links,"categories":categories,"references":references}
        df = pd.DataFrame.from_records([preprocessed_dict],index="title")
    # We append the articles one by one in case there is an error, 
    df.to_csv(open("wikipedia2.csv",mode="w",encoding="utf-8"))


for i in range(10000):
    article = download_article()
    print(article.title)
    title,summary,content,links,categories,references = preprocess_article(article)
    save_article(title,summary,content,links,categories,references)