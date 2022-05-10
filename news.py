# -*- coding: utf-8 -*-
"""ML_Assignment_02.ipynb

Automatically generated by Colaboratory.
"""

from google.colab import drive
drive.mount('/content/drive')

import numpy as np
import pandas as pd
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop = stopwords.words('english')
#from wordcloud import WordCloud

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, Bidirectional
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Load the ds
trueds = pd.read_csv(r'/content/drive/MyDrive/ML_Project/ML_Assignment_02/True.csv')
fakeds = pd.read_csv(r'/content/drive/MyDrive/ML_Project/ML_Assignment_02/Fake.csv')

# Add label 0 = true, 1= fake
trueds['label'] = 1
fakeds['label'] = 0

# Merge title and text
trueds['text'] = trueds['title'] + " " + trueds['text']
fakeds['text'] = fakeds['title'] + " " + fakeds['text']

#OPTIONAL set everything to lowercase MIN: 46 of video

# Select only columns of interest 
trueds = trueds[['text', 'label']]
fakeds = fakeds[['text', 'label']]

# Append datasets together
ds = trueds.append(fakeds, ignore_index=True)

#print(ds.head(), ds.tail())

"""# Data pre-processing"""

# Removing the stopwords from the 'text' column
ds['text'] = ds['text'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))

# Removing string punctuation
ds = ds.replace(r'[^\w\s]|_', '', regex=True)

# Removing words with less than 2 characters
ds = ds.replace(r'\b\w{1,2}\b', '', regex=True)

# create a list from the words
X = [d.split() for d in ds['text'].tolist()]

y = ds['label'].values
#len(X[0])

# Tokenize texts
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X)

# Assign index to word
X = tokenizer.texts_to_sequences(X)
# tokenizer.word_index # test
print(X[0])

# Set the maxlen of sequences to 1000 
maxlen = 100
X = pad_sequences(X, maxlen=maxlen)
# Every sequence has now maximum 1000 words
len(X[0])

# To account for unknown words we add 1 to the vocabulary (similar to Laplace Smoothing technique)
vocab_size = len(tokenizer.word_index) + 1

model = Sequential()
model.add(Embedding(vocab_size, output_dim=100, input_length=maxlen))
model.add(Bidirectional(LSTM(units=128)))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
print(model.summary())

# Split the dataset into train and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

# Fit the model to the training data
model.fit(X_train, y_train, validation_split=0.3, epochs=4, shuffle=True)

# Perform predictions on the test data
y_pred = (model.predict(X_test) >= 0.5).astype(int)

# Accuracy computation and evaluation
print(accuracy_score(y_test, y_pred))
print(classification_report(y_test,y_pred))
