# -*- coding: utf-8 -*-
"""
Created on Sun May 28 20:07:41 2023

@author: shefai
"""
import pandas as pd
import openai


# machine learing techniques
from .function_1_tf_idf_cosine import Funtion1
from .function4 import Funtion4
from .function5 import Funtion5

# deep learning techniques
from .gloveEmbedding_Summary import FuntionGloveSumm
from .gloveEmbedding_reviews import FuntionGloveReview
from .gloveEmbedding_others import FuntionGloveOthers


class Main:
    def __init__(self):
        data = pd.read_csv("cleanDataV1.txt", sep = "\t")
        self.temp = [Funtion1(data), Funtion4(data), Funtion5(data), FuntionGloveSumm(data), FuntionGloveReview(data), FuntionGloveOthers(data)]
    def title(self, title):
        temp = dict()
        for obj in enumerate(self.temp):
            temp[obj[0] + 1] = obj[1].recommendations(title)
        return temp
    
#%%
obj = Main()
recom = obj.title("Keep the Lights On (2012)")

