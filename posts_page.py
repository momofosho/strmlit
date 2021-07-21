from altair.vegalite.v4.schema.core import DataFormat
from numpy.core.numeric import NaN
from numpy.lib.function_base import place
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

def app():
    
    st.title('posts')
    st.write('\U0001F1F8\U0001F1EC')

     # Authenticate to Firestore with the JSON account key.
    db = firestore.Client.from_service_account_json("firestore-key.json")

   #doc_id = db.collection("test5")
    my_dict = {}
    usernames = []
    documents = db.collection(u'test6')
    #print(documents)
    for doc in documents.stream():
      #  print(doc.id)
        usernames.append(doc.id)
        collections = documents.document(doc.id).collections()
        for collection in collections:
            
            for doc in collection.stream():
                my_dict[doc.id] = doc.to_dict()


   # print(my_dict)
    df = pd.DataFrame.from_dict(my_dict)
    df = df.transpose()
   # df.insert(0, 'username', usernames)

    placeholder = st.empty()
    #placeholder.dataframe(df)
    for col in df: 
        df[col] = df[col].fillna('NA')
        column = df.columns.get_loc(col)
        print(type(df.iat[0,column]))
    df['engagement_comments'] = df['engagement_comments'].astype(str)
    df['engagement_likes'] = df['engagement_likes'].astype(str)
    df['username'] = df['username'].astype(str)
   # df['hashtags'] = df['hashtags'].apply(lambda x: tuple(x))
    for col in range(df.shape[1]):
            if type(df.iat[0,col])==list:
                df[df.columns[col]] = df[df.columns[col]].apply(lambda x: tuple(x))
    df.astype(str)

    for row in range((df.shape)[0]):
        for col in range((df.shape)[1]):
            if df.iat[row,col] == []:
                df.iat[row,col] = 'NA'
    print(df)
    filtered_df = df

    #hashtag filter
    hash = df['hashtags'].tolist()
    hash = list(itertools.chain.from_iterable(hash))
    col = df.columns.get_loc("hashtags")

    hashtag_df = pd.DataFrame()

    #Hashtag
    hashtag_filter = st.sidebar.multiselect(
        'Select hashtag',
        options=hash
    )
    #apply filter
    filtered_df['hashtags'] = filtered_df['hashtags'].apply(tuple)
    if hashtag_filter:
        for hash in hashtag_filter:
            for row in range((df.shape)[0]): 
                if hash in df.iat[row,col]:
                    hashtag_df = hashtag_df.append(df.iloc[row,:])
        if hashtag_df.empty == False:
            filtered_df = pd.merge(hashtag_df,filtered_df, how = 'inner')
            #placeholder.table(filtered_df)
        else:
            for col in hashtag_df: 
                hashtag_df[col] = hashtag_df[col].fillna('NA')



    #engagement rate - comments
    comments_df = pd.DataFrame()
    comments = st.sidebar.slider(
        'Select engagement rate for comments',
    0,100, (0,100), step=5
    )
    min_fol = comments[0]
    max_fol = comments[1]
    col = df.columns.get_loc("engagement_comments")
    #print(col)

    if comments:
        for row in range((df.shape)[0]): 
            rate = df.iat[row,col]
            # print(min_fol)
            # print(max_fol)
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
#             print(comments_df.head(5))
#             print(type(comments_df))
#             print(filtered_df)
            filtered_df["engagement_comments"] = filtered_df["engagement_comments"].astype(str)
#             print(filtered_df)
            comments_df["engagement_comments"] = comments_df["engagement_comments"].astype(str)

            filtered_df = pd.merge(comments_df,filtered_df, how = 'inner')
#             print(filtered_df)

        
            
        #placeholder.table(filtered_df)



    #engagement rate - likes
    likes_df = pd.DataFrame()
    likes = st.sidebar.slider(
        'Select engagement rate for likes',
    0,100, (0,100), step=5
    )
    min_fol = likes[0]
    max_fol = likes[1]
    col = df.columns.get_loc("engagement_likes")
    #print(col)

    if likes:
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
           # print(likes_df)
           # print(filtered_df)
            filtered_df["engagement_likes"] = filtered_df["engagement_likes"].astype(str)
            likes_df["engagement_likes"] = likes_df["engagement_likes"].astype(str)

            filtered_df = pd.merge(likes_df,filtered_df, how = 'inner')
          #  print(filtered_df)

        
            
    #     placeholder.table(filtered_df)
    
    # placeholder.table(filtered_df)
    

    #converting a col into hyperlink
    #link = 'https://share.streamlit.io/kirubhaharini/streamlit-trial/main/home.py'
    #link = 'https://www.google.com.sg'
    link = 'https://share.streamlit.io/momofosho/strmlit/main/home.py'


    #######n after user clicks: - for eg:
    # global result
    #result = 'user1'
    # define events
    cds = ColumnDataSource(filtered_df)
    columns = [
    TableColumn(field="engagement_likes",title="engagement_likes", width=200),
    TableColumn(field="engagement_comments",title="engagement_comments", width=200),
    TableColumn(field="username", title="username", formatter=HTMLTemplateFormatter(template=f'<a target="_blank" href="{link}?username=<%= value %>" onclick="alert("Hello");"><%= value %></a>'), width=500)
    ]
    cds.selected.js_on_change(
        "indices",
        CustomJS(
                args=dict(source=cds),
                code="""
                document.dispatchEvent(
                new CustomEvent("INDEX_SELECT", {detail: {data: source.selected.indices}})
                )
                """
        )
    )
    p = DataTable(source=cds, columns=columns, css_classes=["all"], width=500, height=5000)
    result = streamlit_bokeh_events(bokeh_plot=p, events="INDEX_SELECT", key="foo", refresh_on_update=True, debounce_time=0)#, override_height=1000)
    string = 'initialise' #initializing var
    if result:
        try:
            st.write(result)
#             st.write(type(result))
            string = filtered_df.iloc[result["INDEX_SELECT"]["data"][0]]["username"]
#             string = filtered_df.iloc[ast.literal_eval(result)["INDEX_SELECT"]["data"][0]]["username"]
            st.write(string)
            #placeholder.table(df)
        except IndexError:
            pass
   



