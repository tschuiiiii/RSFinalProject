# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 15:59:43 2023

@author: shefai
"""

import os
import pickle
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import gensim.downloader as api
glove_model = api.load("glove-wiki-gigaword-100")
#%%
# load datasets function
class FuntionGloveReview:
    def __init__(self, data):
        self.data = data
        
        
    def cosine_similarity_matrix(self, matrix):
        dot_product = np.dot(matrix, matrix.T)
        norm = np.linalg.norm(matrix, axis=1)
        similarity_matrix = dot_product / np.outer(norm, norm)
        return similarity_matrix

    def preprocess_text(self, value):
        tokens = word_tokenize(value)
        return tokens


    def functionRetunToken(self, text):
        documentList = list()
        
        for i, value in text.items():
            documentList.append(self.preprocess_text(value))
        # metrix with zero,,, number of rows = number of documents, number of columns = total number of words in all documents
        matrxMajor = list()
        
        for index in range(len(documentList)):
            matrxtemp = list()
            for docum in documentList[index]:
                
                
                
                if docum in glove_model:
                    temp = glove_model[docum]
                else:
                    temp = np.zeros(100)
                
                matrxtemp.append(temp)
            
            matrxMajor.append(np.mean(matrxtemp, axis=0))
            
                    
        return np.array(matrxMajor)
    
    def Simfunction(self):
        file_name = "funtionGloveReviews.pickle"
        path = 'similarity/'+file_name
        
        if os.path.exists(path):
            with open(path, 'rb') as handle:
                temp2Dic = pickle.load(handle)
                return temp2Dic
               
        else:
            text = self.data["reviews"]
            matrix = self.functionRetunToken(text)
            SimMatrix =  self.cosine_similarity_matrix(matrix)
            
            
            
            temp2Dic = dict()
            tempDict = dict()
            
            for i in range(len(SimMatrix)):
                array = SimMatrix[i,:]
                
                temppp = list(np.argpartition(np.array(array), -6)[-6:])
                
                if i in temppp:
                    temppp.remove(i)
                    
                tempDict[i] = temppp
            
            
            
            # convert into dictionary of title movies
            titleText = self.data['title']
            titletoIndexDic = dict(zip(self.data.title, self.data.index))
            index_to_titleDic = dict(zip(self.data.index, self.data.title))
            
            temp2Dic = dict()
            for l, title in titleText.items():
                
                index = titletoIndexDic[title]
                moviesIndex = tempDict[index]   
                temp3 = list()
                for p in moviesIndex:
                    if p in index_to_titleDic:
                        temp3.append(index_to_titleDic[p])
                temp2Dic[title] = temp3
            
            with open(path, 'wb') as handle:
                pickle.dump(temp2Dic, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
            return temp2Dic
    
    def recommendations(self, title):
        titlePointtoSimiMoviesDic = self.Simfunction()
        return titlePointtoSimiMoviesDic[title]
      
#%%
# data = pd.read_csv("cleanDataV1.txt", sep = "\t")
# data.dropna(inplace=True)
# obj1 = Funtion9(data)

# ab = obj1.recommendations("Lakshya (2004)")


