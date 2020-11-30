# -*- coding: utf-8 -*-
"""28_11_2020_Model_deployement.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16X3HJIWE0-eWPL_GSzBdyrQMzKVufFhe
"""

import spacy
from spacy import displacy

nlp = spacy.load('en_core_web_sm')

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

#from google.colab import files
#uploaded = files.upload()

# Commented out IPython magic to ensure Python compatibility.
#setup
import pandas as pd
import io
import unicodedata
import numpy as np
import re
import string
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer

from spacy.lang.en.stop_words import STOP_WORDS
stopwords = list(STOP_WORDS)

import string
punct = string.punctuation

#data = pd.read_csv(io.BytesIO(uploaded['Zenbra_cleanedReviews.csv']),sep=',\s+', delimiter=',', encoding="utf-8", skipinitialspace=True)
data= pd.read_csv("Zenbra_cleanedReviews.csv", encoding="latin-1")
data.head()

data.shape

data.isnull().sum()

data=data.dropna()

data.isnull().sum()

def text_data_cleaning(sentence):
    doc = nlp(sentence)
    
    tokens = []
    for token in doc:
        if token.lemma_ != "-PRON-":
            temp = token.lemma_.lower().strip()
        else:
            temp = token.lower_
        tokens.append(temp)
    
    cleaned_tokens = []
    for token in tokens:
        if token not in stopwords and token not in punct:
            cleaned_tokens.append(token)
    return cleaned_tokens

tfidf = TfidfVectorizer(tokenizer = text_data_cleaning)
classifier = LinearSVC()

X = data['cleanedReviews']
y = data['is_bad_review']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
X_train.shape, X_test.shape

clf = Pipeline([('tfidf', tfidf), ('clf', classifier)])

clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print(classification_report(y_test, y_pred))

confusion_matrix(y_test, y_pred)

"""Now we will predict the label of some random sentences."""

clf.predict(['Wow, this is amazing product'])

clf.predict(['I recomment it'])

clf.predict(['this very bad'])

import pickle
pickle.dump(clf, open('zenbramodel.pkl', 'wb'))

# load the model from disk
loaded_model = pickle.load(open('zenbramodel.pkl', 'rb'))
result = loaded_model.predict(['this not good'])
print(result)