# -*- coding: utf-8 -*-
"""
Created on Fri May 26 18:15:56 2023

@author: shefai
"""
# import libraries
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
# Import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
import os
import pickle



# load datasets function
class Funtion1:
    
    def __init__(self, data):
        self.data = data
    
    
            
    def Simfunction(self):
        
        
        tfidf = TfidfVectorizer(stop_words='english')
        matrix = tfidf.fit_transform(self.data['summary'])
        
        file_name = "funtion1.pickle"
        path = 'similarity/'+file_name
       
        if os.path.exists(path):
            with open(path, 'rb') as handle:
                temp2Dic = pickle.load(handle)
                return temp2Dic
              
        else:
            
            cosine_sim = cosine_similarity(matrix, matrix)
            tempDict = dict()
            for i in range(len(cosine_sim)):
                arry = cosine_sim[i]
                topValues = list(np.argpartition(arry, -6)[-6:])
                tempDict[i] = topValues
           
                if i in topValues:
                    topValues.remove(i)
            
            titletoIndexDic = dict(zip(self.data.title, self.data.index))
            
            index_to_titleDic = dict(zip(self.data.index, self.data.title))
            
            titleText = self.data['title']
            
            temp2Dic = dict()
            
            for i, title in titleText.items():
                
                index = titletoIndexDic[title]
                
                moviesIndex = tempDict[index]
                temp3 = list()
                for k in moviesIndex:
                    temp3.append(index_to_titleDic[k])
                temp2Dic[title] = temp3
            
            with open(path, 'wb') as handle:
                pickle.dump(temp2Dic, handle, protocol=pickle.HIGHEST_PROTOCOL)
            
               
        return temp2Dic
            
     
    def recommendations(self, title):
        titlePointtoSimiMoviesDic = self.Simfunction()
        return titlePointtoSimiMoviesDic[title]
        






