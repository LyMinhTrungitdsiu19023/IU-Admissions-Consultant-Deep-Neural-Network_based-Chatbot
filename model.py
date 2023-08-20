import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import pandas as pd
import tensorflow as tf
import tflearn
import json
import pickle
import random
from underthesea import word_tokenize
import re
import speech_recognition as sr
import os
import pyaudio
# # from googletrans import Translator
nltk.download("punkt")


#Import dataset
df1 = pd.read_csv("IUTVTS.csv",names=["Question", "Answer"], encoding = "utf-8", header=None, sep=';')
df2 = pd.read_csv("Copy of Cau hoi TVTS .csv",names=["Question", "Answer"], encoding = "utf-8", header=None, sep=';')
df2 = df2.drop([0, 2]).reset_index(drop=True)

with open('greeting.json') as intents:
    data = json.load(intents)

with open('dataset_stopword-Copy1.json') as f1:
    dataset_stopword = json.loads(f1.read())
    
with open('input_stopword-Copy1.json') as f2:
    input_stopword = json.loads(f2.read())
    
    
    
    
for i in range(459):
  df2["Question"][i] = re.sub(r"[0-9]","", df2["Question"][i])

for i in range(len(df2)):
  df2["Answer"][i] = re.sub("Chương " + "[A-Za-z0-9 -: ́ ̀‘’ ̣ ̉,;–….	ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ]*","",df2["Answer"][i])




df = pd.concat([df1,df2]).reset_index(drop=True)

def data_labeling(df):
    tag_lst = []
    for i in range(len(df)):
        tag = str(df["Question"][i]).lower()
        for j in list(dataset_stopword.keys()):
            tag = re.sub(j,dataset_stopword[j], tag)
            
        tag_lst.append(word_tokenize(tag))
    df.insert(2, 'label', tag_lst)

    return df

  
  
df = data_labeling(df)

stemmer = LancasterStemmer()

# getting informations from intents.json--
words = []
labels = []
x_docs = []
y_docs = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        x_docs.append(wrds)
        y_docs.append(intent['tag'])

        if intent['tag'] not in labels:
            labels.append(intent['tag'])
# Stemming the words and removing duplicate elements.
words = [stemmer.stem(w.lower()) for w in words if w not in "?"]
words = sorted(list(set(words)))
labels = sorted(labels)


training = []
output = []
out_empty = [0 for _ in range(len(labels))]

# One hot encoding, Converting the words to numerals
for x, doc in enumerate(x_docs):
    bag = []
    wrds = [stemmer.stem(w) for w in doc]
    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)


    output_row = out_empty[:]
    output_row[labels.index(y_docs[x])] = 1

    training.append(bag)
    output.append(output_row)


training = np.array(training)
output = np.array(output)

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 128)
net = tflearn.fully_connected(net, 256)
net = tflearn.fully_connected(net, 512)
net = tflearn.fully_connected(net, len(output[0]), activation='softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net)
try:
    model.load("model.tflearn")
except:

    model.fit(training, output, n_epoch=400, batch_size=8, show_metric=True)
    model.save('model.tflearn')
