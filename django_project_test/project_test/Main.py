# -*- coding: utf-8 -*-
"""
Created on Sun May 28 20:07:41 2023

@author: shefai
"""
import pandas as pd

from function_1_tf_idf_cosine import Funtion1
from function_2_counter_cosine import Funtion2
from function_3_counter_cosine import Funtion3
from function4 import Funtion4
from function5 import Funtion5
from function6 import Funtion6

class Main:
    def __init__(self):
        data = pd.read_csv("cleanData.txt", sep = "\t")
        self.temp = [Funtion1(data), Funtion2(data), Funtion3(data), Funtion4(data), Funtion5(data), Funtion6(data)]
        
        
    def title(self, title):
        temp = dict()
        for obj in enumerate(self.temp):
            temp[obj[0] + 1] = obj[1].recommendations(title)
        return temp
    
obj = Main()
recom = obj.title("Men in Black (a.k.a. MIB) (1997)")
pass