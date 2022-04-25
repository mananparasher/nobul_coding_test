# -*- coding: utf-8 -*-
"""Nobul LR.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TOeAaRWw2tv3_QlaiDlAPWWySAnMezug
"""

import re
import pickle
import nltk
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import LogisticRegression


def load_data(path)->pd.DataFrame:
  # load the data
  file = open(path, 'rb')
  data = pickle.load(file)
  return data


def clean_data(df)->pd.DataFrame:
  nltk.download('stopwords')
  stemmer = PorterStemmer()
  words = stopwords.words("english")
  df['cleaned'] = df['body_basic'].apply(lambda x: " ".join([stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words]).lower())
  return df

def vectorization(df):
  vectorizer = TfidfVectorizer(min_df= 3, stop_words="english", sublinear_tf=True, norm='l2', ngram_range=(1, 2))
  return vectorizer

def split_data(df)->pd.DataFrame:
  X = df['cleaned']
  y = df['label']
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
  return X_train, X_test, y_train, y_test


def create_pipeline(X_train, y_train,vectorizer):
  pipeline = Pipeline([('vect', vectorizer),
                     ('chi',  SelectKBest(chi2, k=1200)),
                     ('clf', LogisticRegression(random_state=0))])
  
  model = pipeline.fit(X_train, y_train)
  return model


def save_model(model)->str:
  with open('LogisticRegression.pkl', 'wb') as f:
    pickle.dump(model, f)

  return 'LogisticRegression.pkl'


def make_predictions(model_path,X_test, y_test):
  loaded_model = pickle.load(open(model_path, 'rb'))
  report=classification_report(y_test, loaded_model.predict(X_test))
  return report


if __name__ == "__main__":

    df=load_data('data.pkl')
              
    df=clean_data(df)

    vectorizer=vectorization(df)

    X_train, X_test, y_train, y_test=split_data(df)

    model=create_pipeline(X_train, y_train,vectorizer)

    model_path=save_model(model)
    
    print(make_predictions(model_path,X_test, y_test))