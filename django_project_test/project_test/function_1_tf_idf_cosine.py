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

    def tf_idf(self):

        tfidf = TfidfVectorizer(stop_words='english')
        matrix = tfidf.fit_transform(self.data['summary'])

        file_name = "funtion1.pickle"
        path = 'project_test/similarity/' + file_name

        if os.path.exists(path):
            with open(path, 'rb') as handle:
                self.sim_dic = pickle.load(handle)

        else:
            print("all")
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

        # todo: KeyError see 'alaskaLand (2013)' - id = 110284
        # todo: KeyError see 'Asphalt Playground (La cité rose) (2012)' - id = 110108
        # todo: KeyError see 'A Prayer for Rain (2013)' - id = 143565
        # todo: KeyError see 'Extraordinary Mission (2017)' - id = 173897
        # todo: KeyError see 'The Rolling Stones - Havana Moon (2016)' - id = 169790
        # todo: KeyError see 'Carriage to Vienna (1966)' - id = 126947
        # todo: KeyError see 'The Spider Labyrinth (1988)' - id = 175845
        # todo: KeyError see 'Koumiko Mystery, The (Mystère Koumiko, Le) (1967' - id = 114631
        titleDic = dict(zip(self.data.title, self.data.index))

        index_to_titleDic = dict(zip(self.data.index, self.data.title))

        titleIndex = titleDic[title]
        indexOfRecommendedMovies = sim_dic[titleIndex]

        if titleIndex in indexOfRecommendedMovies:
            indexOfRecommendedMovies.remove(titleIndex)
        else:
            indexOfRecommendedMovies = indexOfRecommendedMovies[:5]

        list_of_recommendations = list()

        for index in indexOfRecommendedMovies:
            list_of_recommendations.append(index_to_titleDic[index])
        return list_of_recommendations


#data = pd.read_csv("project_test/cleanData.txt", sep="\t")
# data passed to save times
#obj = Funtion1(data)
#recomm = obj.recommendations("Toy Story (1995)")

# remove the english stoping words like an, is, the, etc.
