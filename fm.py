# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 18:18:39 2023

@author: fujii masaki
"""
import gensim
model = gensim.models.Word2Vec.load('./ja.bin')
for item, value in model.wv.most_similar('人生'):
    print(item,value)