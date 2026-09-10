#!/usr/bin/env python
# coding: utf-8
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer

# Below libraries are for similarity matrices using sklearn
from sklearn.metrics.pairwise import cosine_similarity  
from sklearn.metrics import pairwise_distances

import fasttext
from huggingface_hub import hf_hub_download
import random
import pickle

if __name__ == "__main__":
        data = pd.read_csv('models/News_Category_Dataset_v3.csv', index_col=False)
        headline_vectorizer = CountVectorizer()
        headline_features = headline_vectorizer.fit_transform(data['headline'])
        model_path = hf_hub_download(repo_id="facebook/fasttext-en-vectors", filename="model.bin")
        model = fasttext.load_model(model_path)
        vocabulary = model.words


        headline_encoded = []
        headline_id_dict = {}

        for i in range(len(data)):
            fasttext_word = np.zeros(300, dtype="float32")
            for word in data.loc[i, 'headline'].split():
                if word in vocabulary:
                    fasttext_word = np.add(fasttext_word, model[word])
            fasttext_word = np.divide(fasttext_word, len(data.loc[i, 'headline'].split()))
            headline_id_dict[str(data.loc[i, 'id'])] = fasttext_word
            headline_encoded.append(fasttext_word)
        headline_encoded = np.array(headline_encoded)

        with open('models/headline_id_dict.pkl', 'wb') as f:
            pickle.dump(headline_id_dict, f)

        with open('models/vocab.pkl', 'wb') as f:
            pickle.dump(vocabulary, f)

        with open('models/headline_encoding.dat', 'wb') as f:
            pickle.dump(headline_encoded, f)

        print("Encoding done!")





