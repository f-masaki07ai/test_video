# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 18:18:39 2023

@author: fujii masaki
"""
from gensim.models import KeyedVectors

model = KeyedVectors.load_word2vec_format('model.vec', binary=False)
model.save("model.kv")
word = "りんご"
ans = model.most_similar(negative=[word])
print(ans)