import nltk
import re
import string
import os
import os.path
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import math
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity

def removeStopwords(unprocessingList):
    stop_words=set(stopwords.words('english'))
    afterProcessingList=[w for w in unprocessingList if not w in stop_words]
    afterProcessingList=[]
    for w in unprocessingList:
        if w not in stop_words:
            afterProcessingList.append(w)
    return afterProcessingList

def stemming(unStemmedList):
    ps=PorterStemmer()
    afterStemmedList=[]
    for w in unStemmedList:
        afterStemmedList.append(ps.stem(w))
    return afterStemmedList

def getFileList():
    fileList = []
    newSet = {}
    newFileList = []
    rootdir = '.\IR\\assignment1\data\\'
    pathlist =  os.listdir(rootdir)
    for i in range(0,len(pathlist)):
        path = os.path.join(rootdir,pathlist[i])
        if os.path.isfile(path):
            f = open(path,'r',encoding='utf8')
            lines=f.readlines()
            lines_str = ','.join(lines)
            lower_lines_str = lines_str.lower()
            remove = str.maketrans('','',string.punctuation)
            without_punctuation_str = lower_lines_str.translate(remove)
            sens = nltk.sent_tokenize(without_punctuation_str)
            words = []
            for sent in sens:
                words.append(nltk.word_tokenize(sent))
            tokens =  words[0]
            types = set(tokens)
            fileWordList=list(set(stemming(removeStopwords(types))))
            processing_str=','.join(fileWordList)
            fileList.append(processing_str)
    return fileList

def findCosineSilimarity():
    corpus=getFileList() 
    vectorizer = CountVectorizer()   
    X = vectorizer.fit_transform(corpus)  
    word = vectorizer.get_feature_names()  
    transformer=TfidfTransformer()
    tfidf=transformer.fit_transform(X)
    weight=tfidf.toarray()
    for a in cosine_similarity(weight):
        print(a)
    print(cosine_similarity(weight))

def processing(filePath):
    f=open(filePath,'r',encoding='utf8')
    lines=f.readlines()
    lines_str = ','.join(lines)
    lower_lines_str = lines_str.lower()
    remove = str.maketrans('','',string.punctuation)
    without_punctuation_str = lower_lines_str.translate(remove)
    sens = nltk.sent_tokenize(without_punctuation_str)
    words = []
    for sent in sens:
        words.append(nltk.word_tokenize(sent))
    tokens =  words[0]
    fileName = filePath.split('\\')[-1]
    print("The numner of the tokens in "+fileName+' is '+str(len(tokens)))
    types = set(tokens)
    print('The numbner of the types in '+fileName+' is '+str(len(types)))
    print('The nuber of the tokens in '+fileName+' after removing all the stopwords is '+str(len(removeStopwords(tokens))))
    print('The nuber of the types in '+fileName+' after removing all the stopwords is '+str(len(removeStopwords(types))))
    print('The number of the terms（size of vocabulary) left in '+ fileName+ ' after stemming is '+ str(len(set(stemming(removeStopwords(types))))))
    print('\n')

def generateCollection():
    if not os.path.exists(".\IR\\assignment1\corpus\collection.txt"):
        for filename in os.listdir(".\IR\\assignment1\data"):
            with open(".\IR\\assignment1\data\\" + filename,encoding='utf8') as f:
                for line in f.readlines():
                    with open(".\IR\\assignment1\corpus\collection.txt","a",encoding='utf8') as collection:
                        collection.write(line) 

generateCollection()
processing('.\IR\\assignment1\data\\a1.txt')
processing('.\IR\\assignment1\data\\a2.txt')
processing('.\IR\\assignment1\data\\a3.txt')
processing('.\IR\\assignment1\data\\a4.txt')
processing('.\IR\\assignment1\data\\a5.txt')
processing('.\IR\\assignment1\data\\a6.txt')
processing('.\IR\\assignment1\data\\a7.txt')
processing('.\IR\\assignment1\data\\a8.txt')
processing('.\IR\\assignment1\data\\a9.txt')
processing('.\IR\\assignment1\data\\a10.txt')
processing('.\IR\\assignment1\corpus\\collection.txt')
findCosineSilimarity()