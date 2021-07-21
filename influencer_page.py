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

# def returnRes():
#     res = 4
#     return res

# def pyt():
#     return 1

def app():

    st.title('influencers:')
    # Authenticate to Firestore with the JSON account key.
    db = firestore.Client.from_service_account_json("firestore-key.json")

    # doc_id = db.collection("users")

    # documents = db.collection(u'users')
    # print(documents)
    # for doc in documents.stream():
    #     print(doc.id)
    #     #docs = doc.stream()
    #     my_dict = { doc.id: doc.to_dict()}
    #     print(my_dict)
    #     collections = documents.document(doc.id).collections()
    #     for collection in collections:
            
    #         for doc in collection.stream():
    #             print(f'{doc.id} => {doc.to_dict()}')
                

    doc_id = db.collection("test6")

    docs = doc_id.stream()
    my_dict = { doc.id: doc.to_dict() for doc in docs }
    #print(my_dict)
    df = pd.DataFrame.from_dict(my_dict)
    df = df.transpose()
    placeholder = st.empty()
    #placeholder.dataframe(df)
    for col in df: 
        df[col] = df[col].fillna('NA')
        column = df.columns.get_loc(col)
        print(type(df.iat[0,column]))
    df['followers'] = df['followers'].astype(str)
   # df['location'] = df['location'].astype(str)
    df['posts'] = df['posts'].astype(str)
    df['username'] = df['username'].astype(str)
    df['hashtags'] = df['hashtags'].apply(lambda x: tuple(x))


    filtered_df = df

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
            placeholder.table(filtered_df)
        else:
            for col in hashtag_df: 
                hashtag_df[col] = hashtag_df[col].fillna('NA')


    #Location
    # locations = df['location'].tolist()
    # locations = [x for x in locations if type(x) != float]
    # #print(locations) 
    # locations_filter = st.sidebar.multiselect(
    #     'Select country',
    #     options=locations
    # )

    # #apply filter
    # location_df = pd.DataFrame()
    # col = df.columns.get_loc("location")
    # if locations_filter:
    #     for row in range((df.shape)[0]): 
    #         if (df.iat[row,col]) in (locations_filter):
    #             location_df = location_df.append(df.iloc[row,:])
    #     if (location_df.empty == False):
    #         #print(filtered_df)
    #         filtered_df = pd.merge(location_df,filtered_df, how = 'inner')
    #         #print(filtered_df)
    #         placeholder.table(filtered_df)
    #     else:
    #         for col in location_df: 
    #             location_df[col] = location_df[col].fillna('NA')
        


    #Followers
    followers_df = pd.DataFrame()
    followers = st.sidebar.slider(
        'Select follower range',
        1000, 10000, (1000, 10000), step=100
    )
    min_fol = followers[0]
    max_fol = followers[1]
    col = df.columns.get_loc("followers")
    #print(col)

    if followers:
        for row in range((df.shape)[0]): 
            followers_count = df.iat[row,col]
            # print(min_fol)
            # print(max_fol)
            if followers_count == 'NA':
                followers_count = np.NaN
            if min_fol <= int(followers_count) <= max_fol:
                #apply filter
                followers_df = followers_df.append(df.iloc[row,:])

        if followers_df.empty == True:
            filtered_df = pd.DataFrame()
            for col in followers_df: 
                followers_df[col] = followers_df[col].fillna('NA')
        if (filtered_df.empty == False and followers_df.empty == False):
            print(followers_df)
            print(filtered_df)
            filtered_df["followers"] = filtered_df["followers"].astype(int)
            followers_df["followers"] = followers_df["followers"].astype(int)

            filtered_df = pd.merge(followers_df,filtered_df, how = 'inner')
            print(filtered_df)

        
            
        placeholder.table(filtered_df)


        
    placeholder.table(filtered_df)
    cds = ColumnDataSource(filtered_df)
    columns = [
    TableColumn(field="bio",title="bio")#, formatter = HTMLTemplateFormatter(template="""{wordWrap: ‘break-word’}<%= value %>""")),#, width=200),
    TableColumn(field="category",title="category"),#, width=200),
    TableColumn(field="followers",title="followers"),#, width=200),
    TableColumn(field="followings",title="followings"),#, width=200),
    TableColumn(field="hashtags",title="hashtags"),#, width=200),
    TableColumn(field="posts",title="posts"),#, width=200),
    TableColumn(field="username",title="username"),#, width=200),          
    ]
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
    p = DataTable(source=cds, columns=columns, css_classes=["all"], aspect_ratio="auto")#, width=500, height=5000)
    result = streamlit_bokeh_events(bokeh_plot=p, events="INDEX_SELECT", key="foo", refresh_on_update=True, debounce_time=0)#, override_height=1000)
