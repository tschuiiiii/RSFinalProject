# -*- coding: utf-8 -*-
"""
Created on Sun May 28 12:23:11 2023

@author: shefai
"""
import nltk
#nltk.download()
import pandas as pd

#text = "Playing played play James Bond must unmask the mysterious head of the Janus Syndicate and prevent the leader from utilizing the GoldenEye weapons system to inflict devastating revenge on Britain."

data = pd.read_csv("FinalVersion.txt", sep = "\t")

data = data.iloc[:, :]


def cleaning(text):
    from nltk.tokenize import word_tokenize
    tokens = word_tokenize(text)
    # convert to lower case
    tokens = [w.lower() for w in tokens]
    # remove punctuation from each word
    import string
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    # filter out stop words
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]

    from nltk.stem import WordNetLemmatizer
    porter = WordNetLemmatizer()
    words = [porter.lemmatize(word) for word in words]
    words = ' '.join([str(elem) for elem in words])
    return words


for i in range(len(data)):
    
    actors = cleaning(data.iloc[i, 0])
    director = cleaning(data.iloc[i, 1])
    summary =  cleaning(data.iloc[i, 3])
    
    reviews =  cleaning(data.iloc[i, 6])
    keyword =  cleaning(data.iloc[i, 7])
    
    genres = data.iloc[i, 8].replace("|", " ")
    
    genres =  cleaning(genres)
    
    
    data.iloc[i, 0] = actors
    data.iloc[i, 1] = director
    data.iloc[i, 3] = summary
    
    data.iloc[i, 6] = reviews
    data.iloc[i, 7] = keyword
    data.iloc[i, 8] = genres


data.to_csv("cleanData.txt", sep = "\t", index = False)
#%%
import pandas as pd

data = pd.read_csv("cleanData.txt", sep = "\t")

data = data.iloc[:5000,:]

data.to_csv("halfcleanData.txt", sep = "\t", index = False)


