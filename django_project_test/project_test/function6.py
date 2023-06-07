# -*- coding: utf-8 -*-
"""
Created on Fri May 26 18:15:56 2023

@author: shefai
"""
# import libraries
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
# Import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
import os
import pickle

# load datasets function
class Funtion6:
    def __init__(self, data):
        self.data = data
           
    def tf_idf(self):
        cont_vect = CountVectorizer(stop_words='english', binary = True)
        matrix = cont_vect.fit_transform(self.data['reviews'])
        
        file_name = "funtion6.pickle"
        path = 'similarity/'+file_name
        
        if os.path.exists(path):
            with open(path, 'rb') as handle:
                self.sim_dic = pickle.load(handle)
               
        else:
            cosine_sim = cosine_similarity(matrix, matrix)
            tempDict = dict()
            for i in range(len(cosine_sim)):
                arry = cosine_sim[i]
                topValues = list(np.argpartition(arry, -6)[-6:])
                tempDict[i] = topValues
            
            self.sim_dic = tempDict
            with open(path, 'wb') as handle:
                pickle.dump(tempDict, handle, protocol=pickle.HIGHEST_PROTOCOL)
                
        return self.sim_dic
    def recommendations(self, title):
        sim_dic = self.tf_idf()
        
        titleDic = dict(zip(self.data.title, self.data.index))
        
        index_to_titleDic = dict(zip(self.data.index, self.data.title))
        
        
        titleIndex = titleDic[title]
        indexOfRecommendedMovies = sim_dic[titleIndex]
        
        if titleIndex in indexOfRecommendedMovies:
            indexOfRecommendedMovies.remove(titleIndex)
        else:
            indexOfRecommendedMovies = indexOfRecommendedMovies[:5]
            
        list_of_recommendations =   list()
        
        for index in indexOfRecommendedMovies:
            list_of_recommendations.append(index_to_titleDic[index])
        return list_of_recommendations
        
        




