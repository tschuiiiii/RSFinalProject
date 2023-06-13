# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 09:32:06 2023

@author: shefai
"""
import os
import pickle


def recommendations(title):
    folderpath = r"project_test/similarity/"
    filepaths  = [os.path.join(folderpath, name) for name in os.listdir(folderpath)]
    
    if len(filepaths) == 0:
        print("No Similarity is available in similarity folder, please, first calculate the similarity values")
        return 0
    else:
        tempRecommendation = dict()
        counter = 1
        for file in filepaths:
            with open(file, 'rb') as f:
                dictonary = pickle.load(f)
                tempRecommendation[file.split(".")[0]] = dictonary[title]
                counter+=1
    return tempRecommendation            
    
    
#recomm = recommendations("Barbie: Princess Charm School (2011)")
