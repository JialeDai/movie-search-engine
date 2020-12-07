import pymongo
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer 
from bson import ObjectId

def plot_search(query):
    client = pymongo.MongoClient("mongodb://Song:a931021@cluster0-shard-00-00-ywxjv.azure.mongodb.net:27017,cluster0-shard-00-01-ywxjv.azure.mongodb.net:27017,cluster0-shard-00-02-ywxjv.azure.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
    movie_db= client.movie_web

    # get previous stored data in order to speed the program
    data = movie_db.catalog_movie_plots.find()
    corpus = data[1]['corpus']
    all_ids = data[2]['all_ids']

    # get the num of tokens and types of origin documents
    tokens = nltk.word_tokenize(query)
    
    # removing stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words] 
    
    # stem the tokens
    ps = PorterStemmer()
    stemmed_tokens = [ps.stem(token) for token in filtered_tokens]
    output_query = ' '.join(stemmed_tokens)

    # add user query into the corpus
    corpus.append(query)

    # calculating the 
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus)
    word = vectorizer.get_feature_names()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(X)

    #computing cos similarity
    arr_tfidf = tfidf.toarray()
    np.set_printoptions(precision = 3)
    l_cossim = {}
    i = 0
    arr_query = arr_tfidf[len(corpus)-1].reshape(1, -1)

    while i < len(corpus)-1:
        arr_plot = arr_tfidf[i].reshape(1, -1)
        cossim = cosine_similarity(arr_query, arr_plot)
        l_cossim[all_ids[i]] = float(cossim)
        i += 1
    sorted_l_cosim = sorted(l_cossim.items(), key=lambda item:item[1], reverse=True)
    high_ids = sorted_l_cosim[:10]
    high_oids = [ObjectId(item[0]) for item in high_ids]

    return high_oids