# -*- coding: utf-8 -*-
"""
Created on Fri May 26 18:15:56 2023

@author: shefai
"""

import pandas as pd
import numpy as np

data = pd.read_csv("dataframe_v11.txt", sep="\t")
data.info()
#%%
del data["synopsis"]
del data["adult"]
data.dropna(inplace = True)

#%%
## add.......
# title and rating to datasets
movie = pd.read_csv("movies.csv")
rating = pd.read_csv("ratings.csv")

movieId_genre = dict(zip(movie.movieId, movie.genres))
movieId_title = dict(zip(movie.movieId, movie.title))

movieId_rating = dict(zip(rating.movieId, rating.rating))

#%%

deletedList = list()
for id in list(data['Id']):
    if id in movieId_genre and id in movieId_title and id in movieId_rating:
        pass
        #temp1.append(movieId_genre[id])
        #temp2.append(movieId_title[id])
        #temp3.append(movieId_rating[id])
    else: 
        deletedList.append(id)

for delete in deletedList:
    data = data[data["Id"] != delete]
#%%
temp1 = list()
temp2 = list()
temp3 = list()
for id in list(data['Id']):
        temp1.append(movieId_genre[id])
        temp2.append(movieId_title[id])
        temp3.append(movieId_rating[id])
    
#%%

data["genres"] = temp1
data["title"] = temp2
data["rating"] = temp3
#%%
data.to_csv("FinalVersion.txt", sep = "\t", index = False)







