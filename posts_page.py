from altair.vegalite.v4.schema.core import DataFormat
from numpy.core.numeric import NaN
from numpy.lib.function_base import place
import pyrebase
import streamlit as st
from google.cloud import firestore
import json
import pandas as pd
import itertools
import numpy as np
from bokeh.models.widgets import TableColumn
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models import DataTable, HTMLTemplateFormatter
from streamlit_bokeh_events import streamlit_bokeh_events
import ast
import json
from github import Github
import importlib
import sessionstate
from streamlit.hashing import _CodeHasher

def postspage(state):
    st.title('posts')
    #getting data from firebase
    db = firestore.Client.from_service_account_json("firestore-key.json")
    my_dict = {}
    usernames = []
#     documents = db.collection(u'test6')
    documents = db.collection(u'eczema')    
    for doc in documents.stream():
        usernames.append(doc.id)
        collections = documents.document(doc.id).collections()
        for collection in collections:
            for doc in collection.stream():
                my_dict[doc.id] = doc.to_dict()

    df = pd.DataFrame.from_dict(my_dict)
    df = df.transpose() #into a dataframe

    #cleaning the dataframe, making everything strings to avoid unhashable type errors
#     placeholder = st.empty()
    for col in df: 
        df[col] = df[col].fillna('NA')
        column = df.columns.get_loc(col)
        print(type(df.iat[0,column]))
    df['engagement_comments'] = df['engagement_comments'].astype(str)
    df['engagement_likes'] = df['engagement_likes'].astype(str)
    df['username'] = df['username'].astype(str)
    df["sentiment"] = df["sentiment_emoji"].astype(str)
    df["time"] = df["time"].astype(str)
    for col in range(df.shape[1]):
            if type(df.iat[0,col])==list:
                df[df.columns[col]] = df[df.columns[col]].apply(lambda x: tuple(x))
    df.astype(str)
    for row in range((df.shape)[0]):
        for col in range((df.shape)[1]):
            if df.iat[row,col] == []:
                df.iat[row,col] = 'NA'

    #this will be the df that we keep merging/filtering
    filtered_df = df

    #Hashtag filter
    #getting the hashtags
    hash = df['hashtags'].tolist()
    hash = list(itertools.chain.from_iterable(hash))
    hash = list(set([i.lower() for i in hash]))
    col = df.columns.get_loc("hashtags")
    hashtag_df = pd.DataFrame()
    
    #hashtag multiselect widget
    state.postpg_hashtag_filter = st.sidebar.multiselect(
        label='Select hashtag',
        options=hash,
        default=state.postpg_hashtag_filter
    )
    
    #apply filter
    filtered_df['hashtags'] = filtered_df['hashtags'].apply(tuple)
    if state.postpg_hashtag_filter:
        for hash in state.postpg_hashtag_filter:
            for row in range((df.shape)[0]): 
                if hash in df.iat[row,col]:
                    hashtag_df = hashtag_df.append(df.iloc[row,:])
        if hashtag_df.empty == False:
            filtered_df = pd.merge(hashtag_df,filtered_df, how = 'inner')
        else:
            for col in hashtag_df: 
                hashtag_df[col] = hashtag_df[col].fillna('NA')


    #engagement rate for comments slider
    comments_df = pd.DataFrame()
    state.comments = st.sidebar.slider(
        'Select engagement rate for comments',
    0,100, (0,100), step=5
    )
    min_fol = state.comments[0]
    max_fol = state.comments[1]
    col = df.columns.get_loc("engagement_comments")

    if state.comments:
        for row in range((df.shape)[0]): 
            rate = df.iat[row,col]
            if rate == 'NA':
                rate = 0
            if min_fol <= float(rate) <= max_fol:
                #apply filter
                comments_df = comments_df.append(df.iloc[row,:])

        if comments_df.empty == True:
            filtered_df = pd.DataFrame()
            for col in comments_df: 
                comments_df[col] = comments_df[col].fillna('NA')
        if (filtered_df.empty == False and comments_df.empty == False):
            filtered_df["engagement_comments"] = filtered_df["engagement_comments"].astype(str)
            comments_df["engagement_comments"] = comments_df["engagement_comments"].astype(str)
            
            print(comments_df.dtypes)
            print(comments_df.columns)
            filtered_df = pd.merge(comments_df,filtered_df, how = 'inner')

    #engagement rate for likes slider
    likes_df = pd.DataFrame()
    state.likes = st.sidebar.slider(
        'Select engagement rate for likes',
    0,100, (0,100), step=5
    )
    min_fol = state.likes[0]
    max_fol = state.likes[1]
    col = df.columns.get_loc("engagement_likes")

    if state.likes:
        for row in range((df.shape)[0]): 
            rate = df.iat[row,col]
            # print(min_fol)
            # print(max_fol)
            if rate == 'NA':
                rate = 0
            if min_fol <= float(rate) <= max_fol:
                #apply filter
                likes_df = likes_df.append(df.iloc[row,:])

        if likes_df.empty == True:
            filtered_df = pd.DataFrame()
            for col in likes_df: 
                likes_df[col] = likes_df[col].fillna('NA')
        if (filtered_df.empty == False and likes_df.empty == False):
            filtered_df["engagement_likes"] = filtered_df["engagement_likes"].astype(str)
            likes_df["engagement_likes"] = likes_df["engagement_likes"].astype(str)
            filtered_df = pd.merge(likes_df,filtered_df, how = 'inner')
  

    
 ###############################################################################################  
    #Displaying filtered_df
    import home
    with st.beta_container():
        filtered_df
        cols = st.columns(4)
        cols[0].write("engagement_likes")
        cols[1].write("engagement_comments")
        cols[2].write("sentiment")
        cols[3].write("username")
        for i in range(len(filtered_df)):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(round(float(filtered_df["engagement_likes"][i]),2))
            with col2:
                st.write(round(float(filtered_df["engagement_comments"][i]),2))
            with col3:
                if filtered_df["sentiment_emoji"][i]=="NA":
                    st.markdown("`NA`")
                else:
                    st.write(filtered_df["sentiment_emoji"][i])
            with col4:
                if st.button(filtered_df["username"][i], key=filtered_df["shortcode"][i]):
                    state.query_username = filtered_df["username"][i]


###############################################################################################
    link = 'https://share.streamlit.io/momofosho/strmlit/main/home.py'
#     ####### after user clicks: - for eg:
#     # global result
#     #result = 'user1'
#     # define events
#     cds = ColumnDataSource(filtered_df)
#     columns = [
#     TableColumn(field="engagement_likes",title="engagement_likes", width=200),
#     TableColumn(field="engagement_comments",title="engagement_comments", width=200),
#     TableColumn(field="username", title="username", formatter=HTMLTemplateFormatter(template=f'<a target="_blank" href="{link}?username=<%= value %>" ><%= value %></a>'), width=500)
#     ]
#     cds.selected.js_on_change(
#         "indices",
#         CustomJS(
#                 args=dict(source=cds),
#                 code="""
#                 document.dispatchEvent(
#                 new CustomEvent("INDEX_SELECT", {detail: {data: source.selected.indices}})
#                 )
#                 """
#         )
#     )
#     p = DataTable(source=cds, columns=columns, css_classes=["all"], width=500, height=5000)
#     result = streamlit_bokeh_events(bokeh_plot=p, events="INDEX_SELECT", key="foo", refresh_on_update=True, debounce_time=0)#, override_height=1000)
#     string = 'initialise' #initializing var
#     if result:
#         try:
#             st.write(result)
# #             st.write(type(result))
#             string = filtered_df.iloc[result["INDEX_SELECT"]["data"][0]]["username"]
# #             string = filtered_df.iloc[ast.literal_eval(result)["INDEX_SELECT"]["data"][0]]["username"]
#             st.write(string)
#             #placeholder.table(df)
#         except IndexError:
#             pass















