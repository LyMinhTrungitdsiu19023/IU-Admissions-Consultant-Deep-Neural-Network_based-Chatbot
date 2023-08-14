import numpy as np
import pandas as pd
import random
from underthesea import word_tokenize
import re
import speech_recognition as sr
import os
import pyaudio
from model import *
from pattern import *
def tokenize_input(user_input):
    text = user_input.lower()
    for j in list(input_stopword.keys()):
        text = re.sub(j,input_stopword[j], text)
    return word_tokenize(text)
  
def polarity_score(user_input, label):
    score = 0
    for i in user_input:
        for j in label:
            if i.lower() == j.lower():
                score += 1

    final_score = score/len(label)  

    for j in label:
        if i.lower() == j.lower():
            score += 1

    final_score = score/len(label)  
    return score



def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)

    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for s_word in s_words:
        for i, w in enumerate(words):
            if w == s_word:
                bag[i] = 1

    return np.array(bag)
  
def predict_ans(user_input,user_input_tokened, df):
  ans_lst = []
  response = []
  n = 191
  n_2 = 687

  if re.search(pattern_1, user_input.lower()):
    df1 = df.tail(n_2 - n).loc[~df["Question"].str.contains(pattern_2)].reset_index(drop = True)

  elif re.search(pattern_3, user_input.lower()):
    if re.search(pattern_4, user_input.lower()):
        df1 = df.head(n).loc[df["Question"].str.contains(pattern_5)].reset_index(drop = True)
    else:
        df1 = df.head(n).loc[df["Question"].str.contains(pattern_6)].reset_index(drop = True)
  elif re.search(pattern_7, user_input.lower()):
    df1 = df.tail(n_2 - n).loc[df["Question"].str.contains(pattern_8)].reset_index(drop = True)
  elif re.search(pattern_9, user_input.lower()):
    df1 = df.tail(n_2 - n).loc[df["Question"].str.contains(pattern_10)].reset_index(drop = True)
  elif re.search(pattern_11, user_input.lower()):
    df1 = df.tail(n_2 - n).loc[df["Question"].str.contains(pattern_12)].reset_index(drop = True)
  elif re.search(pattern_13, user_input.lower()):
    if re.search(pattern_14, user_input.lower()):
        df1 = df.tail(n_2 - n).loc[~df["Question"].str.contains(pattern_15)].reset_index(drop = True)
    elif re.search(pattern_16, user_input.lower()):
        df1 = df.tail(n_2 - n).loc[~df["Question"].str.contains(pattern_17)].reset_index(drop = True)
  else:
    if re.search(pattern_18, user_input.lower()):
        df1 = df.head(n).loc[df["Question"].str.contains(pattern_19)].reset_index(drop = True)
    else:
        df1 = df.head(n).loc[~df["Question"].str.contains(pattern_20)].reset_index(drop = True)
        
  for i in range(len(df1)):
    score = polarity_score(user_input_tokened, df1["label"][i])
    if score >= 0.6:
      ans = []
      ans.append(score)
      ans.append(df1["Answer"][i])
      ans_lst.append(ans)

  score_lst = []
  for answer in ans_lst:
    score_lst.append(answer[0])
    max_score = max(score_lst,key=lambda x:float(x))
    if max_score == answer[0]:
      if re.search(pattern_21, user_input):
        if max_score >= 0.7 and re.search(pattern_21, answer[1].lower()):
          response.append(answer[1])

      elif re.search(pattern_22, user_input):
        if max_score >= 0.7 and re.search(pattern_22, answer[1].lower()):
          response.append(answer[1])
      elif re.search(pattern_23, user_input) and re.search(pattern_24, user_input):
        if max_score >= 5:
          response.append(answer[1])        
      elif re.search(pattern_23, user_input) and re.search(pattern_25, user_input):
        if max_score >= 4:
          response.append(answer[1])        
      else:
         if max_score >= 0.7 and not re.search(pattern_26, answer[1].lower()):
          response.append(answer[1])
        
  return set(response)



def chat_bot(user_input):

    if re.search(r"(quit)|(bye)|(tạm biệt)|(cảm ơn)", user_input.lower()):
        out_put =  "Tạm biệt, rất vui được giúp bạn"

    elif re.search(r"(chào)|(hello)|(hey)", user_input.lower()):
        results = model.predict([bag_of_words(user_input, words)])

        results_index = np.argmax(results)

        tag = labels[results_index]

        for tg in data['intents']:

            if tg['tag'] == tag:
                responses = tg['responses']
                res = random.choice(responses)
                out_put = res


    else:
        user_input_tokened = tokenize_input(user_input)
        pre = predict_ans(user_input,user_input_tokened, df)

        if pre != set():
          out_put =  '- '+'\n- '.join(sorted(predict_ans(user_input,user_input_tokened , df)))

        elif pre == set():     
          out_put =  "Xin lỗi, hiện tại tôi chưa có thông tin chi tiết về vấn đề này, bạn có thể truy cập website 'https://hcmiu.edu.vn/category/tuyen-sinh/' để biết thêm chi tiết"



    return out_put
