#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from datetime import datetime
import sys

if __name__ == "__main__":
    # Get input arguments
    headline = sys.argv[1]
    category = sys.argv[2]
    authors = sys.argv[3]
    id = sys.argv[4]
    date = sys.argv[5]
    data = pd.read_csv('models/News_Category_Dataset_v3.csv', index_col=False)

    # # input = {"link": "https://www.huffpost.com/entry/the-federalist", "headline": "Over 4 Million Americans Roll Up Sleeves For Omicron-Targeted COVID Boosters", "category": "U.S. NEWS", "authors": "Carla K. Johnson, AP", "id":"9809", "date": "2022-09-23"}

    stop_words = set(stopwords.words('english'))
    string = ""
    for word in headline.split():
        word = ("".join(e for e in word if e.isalnum()))
        word = word.lower()
        if not word in stop_words:
            string += word + " " 
    headline = string.strip()


    lemmatizer = WordNetLemmatizer()
    string = ""
    for w in word_tokenize(headline):
        string += lemmatizer.lemmatize(w,pos = "v") + " "
    headline = string.strip()

    date = datetime.strptime(date, '%Y-%m-%d')
    date = date.strftime("%a") + "_" + date.strftime("%b")

    data.loc[len(data.index)] = ["del", headline, category, authors, id, date] 
    data.to_csv('models/News_Category_Dataset_v3.csv', index = False)
    print("DataBase Updated")





