#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances
import random
import pickle
import sys



class Recommender:
    def __init__(self):
        self.data = pd.read_csv('models/News_Category_Dataset_v3.csv', index_col=False)
        self.vocabulary = None
        with open('models/vocab.pkl', 'rb') as f:
            self.vocabulary = pickle.load(f)
        self.headline_id_dict = None
        with open('models/headline_id_dict.pkl', 'rb') as f:
            self.headline_id_dict = pickle.load(f)
        self.headline_encoded = None
        with open('models/headline_encoding.dat', 'rb') as f:
            self.headline_encoded = pickle.load(f)
        
    def recommend(self, read_ids, cat_list):
        if(len(read_ids) == 0):
            rec = self.data['id'].tolist()
            random.shuffle(rec)
            return rec[:10]

        titles_encoded = []
        for i in read_ids:
            titles_encoded.append(self.headline_id_dict[str(i)])

        titles_encoded = np.array(titles_encoded)

        new_df = []
        for i in titles_encoded:
            fasttext_dist  = pairwise_distances(self.headline_encoded, i.reshape(1,-1))
            indices = np.argsort(fasttext_dist.flatten())[0:200].tolist()
            if(len(new_df) == 0):
                new_df = pd.DataFrame({
                            'headline_text': self.data['headline'][indices].values,
                            'id': self.data['id'][indices].values,
                            'Category': self.data['category'][indices].values})
            else:
                new_df = pd.concat([new_df, (pd.DataFrame({
                            'headline_text': self.data['headline'][indices].values,
                            'id': self.data['id'][indices].values,
                            'Category': self.data['category'][indices].values}))], axis=0)
        new_df = new_df.iloc[1:, ]
        if(len(cat_list) == 0):
            rec = new_df['id'].tolist()
            random.shuffle(rec)
            return rec[:10]
        new_df = new_df[new_df['Category'].isin(cat_list)]
        
        # print(titles)
        # print(new_df.to_string())
        return new_df['id'].tolist()[:10]





# model = Recommender()
# print(model.recommend(["7595", "12554"], ['WORLD', 'POLITICS', 'SPORTS']))
if __name__ == "__main__":
    # Get input arguments
    read_ids = sys.argv[1].strip().split(',')
    cat_list = sys.argv[2].strip().split(',')
    # print(read_ids)
    # print(cat_list)
    
    model = Recommender()
    rec = model.recommend(read_ids, cat_list)
    print(rec)