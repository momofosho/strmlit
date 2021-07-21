from logging import PlaceHolder
from altair.vegalite.v4.schema.core import DataFormat
from numpy.core.numeric import NaN
from numpy.lib.function_base import place
import streamlit as st
from google.cloud import firestore
import json
import pandas as pd
import itertools
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
# import os
# os.system('python -m nltk.downloader all')


app_state = st.experimental_get_query_params()
default_title = app_state["username"] if "username" in app_state else "['newfacebeauty.hk']"
title = st.text_input('Influencer Username', value = default_title)
app_state["username"] = title

# st.write(st.experimental_get_query_params())

a = st.experimental_get_query_params().get('username',['nope'])[0]
st.write(st.experimental_get_query_params())
st.write(type(st.experimental_get_query_params()))
st.write(st.experimental_get_query_params().keys())
# a = 'monie_skin_care'
st.write(a) #result that it returns

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("firestore-key.json")

#doc_id = db.collection("test5")
my_dict = {}
usernames = []
documents = db.collection(u'test6')

#influencer data
docs = documents.stream()
my_dict1 = { doc.id: doc.to_dict() for doc in docs }
df1 = pd.DataFrame.from_dict(my_dict1)
df1 = df1.transpose()
user_info = df1[df1.username.str.contains(a)]
st.table(df1)
st.write(user_info)

#posts data
for doc in documents.stream():
    
    # usernames.append(doc.id)
    if doc.id == a:
        print(doc.id)
        collections = documents.document(doc.id).collections()
        for collection in collections:
            
            for doc in collection.stream():
                my_dict[doc.id] = doc.to_dict()

# print(my_dict)
posts_info = pd.DataFrame.from_dict(my_dict)
posts_info = posts_info.transpose()
#st.table(posts_info)

username = a
location = user_info['bio'][0]  #location
contact_details = '-'
st.title(username)
st.markdown(location +'\t\t'+ contact_details)

posts, followers, following, likes, comments = st.beta_columns(5)

with posts:
  st.write("posts")
  st.write(str(user_info['posts'][0]))


with followers:
  st.write("followers")
  st.write(str(user_info['followers'][0]))

with following:
  st.write("following")
  st.write(str(user_info['followings'][0]))

with likes:
  st.write("likes")
  st.write(str(posts_info['likes'].sum(skipna=True)))

with comments:
  st.write("comments")
  sum =0
  for com in posts_info['comments']:
    sum = sum + len(com)
  st.write(str(sum))

# nltk.download('punkt')
# nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
 
for cap in posts_info["caption"]:
  #cap = cap.replace('.','')
  word_tokens = word_tokenize(cap)
  filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
  filtered_sentence = []
  for w in word_tokens:
      if w not in stop_words:
          filtered_sentence.append(w)

hash = filtered_sentence.index('#')
filtered_sentence = filtered_sentence[0:hash]
print(filtered_sentence)

# posts_info = posts_info.join(pd.DataFrame(data = {"processed caption" : np.array(filtered_sentence)}))
# st.table(posts_info)

st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">',
    unsafe_allow_html=True,
)

query_params = st.experimental_get_query_params()
tabs = ["Hashtags", "Keywords", "Posts"]
if "tab" in query_params:
    active_tab = query_params["tab"][0]
else:
    active_tab = "Hashtags"

if active_tab not in tabs:
    active_tab = "Hashtags"

import string
a_dash = a
punctuations = {"_","."}

for ele in a_dash:
    if ele in punctuations:
        a_dash = a_dash.replace(ele, " ")
a_dash = '-'.join(a_dash.split())

li_items = "".join(
    f"""
    <li class="nav-item">
        <a class="nav-link{' active' if t==active_tab else ''}" href="/?username={a}&tab={t}">{t}</a>
    </li>
    """
    for t in tabs
)
tabs_html = f"""
    <ul class="nav nav-tabs">
    {li_items}
    </ul>
"""

st.markdown(tabs_html, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

if active_tab == "Hashtags":
    flat_list = [item for sublist in posts_info['hashtags'] for item in sublist]
    flat_str = ' '.join(flat_list)
    wordcloud = WordCloud(background_color = 'lightblue', width = 1000, height = 1000, max_words = 50).generate(flat_str)

    plt.rcParams['figure.figsize'] = (10, 10)
    plt.title('Hashtags', fontsize = 20)
    plt.axis('off')
    plt.imshow(wordcloud)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()


elif active_tab == "Keywords":
    filtered_str = ' '.join(filtered_sentence)
    filtered_str = re.sub(r'[^\w\s]', '', filtered_str)
    print(filtered_str)

    wordcloud = WordCloud(background_color = 'lightblue', width = 1000, height = 1000, max_words = 50).generate(filtered_str)

    plt.rcParams['figure.figsize'] = (10, 10)
    plt.title('Caption Keywords', fontsize = 20)
    plt.axis('off')
    plt.imshow(wordcloud)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

elif active_tab == "Posts":
    st.write("If you'd like to contact me, then please don't.")
else:
    st.error("Something has gone terribly wrong.")
