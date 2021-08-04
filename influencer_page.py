from altair.vegalite.v4.schema.core import DataFormat
from numpy.core.numeric import NaN
from numpy.lib.function_base import place
from pandas.core.frame import DataFrame
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


import streamlit as st
import sessionstate
from streamlit.hashing import _CodeHasher
def influencerspage(state):

#     st.write(state.user)
    st.title('influencers:')
    # Authenticate to Firestore with the JSON account key.
    db = firestore.Client.from_service_account_json("firestore-key.json")  

    #Getting the data in firebase, putting into dataframe
#     doc_id = db.collection("test6")
    doc_id = db.collection("eczema")
    docs = doc_id.stream()
    my_dict = { doc.id: doc.to_dict() for doc in docs }
    df = pd.DataFrame.from_dict(my_dict)
    df = df.transpose()
    placeholder = st.empty()
    
    #Cleaning, if not will have some errors when merging if its not hashable/column type not consistent
    for col in df: 
        df[col] = df[col].fillna('NA')
        column = df.columns.get_loc(col)
        print(type(df.iat[0,column]))
    df['followers'] = df['followers'].astype(str)
   # df['location'] = df['location'].astype(str)
    df['posts'] = df['posts'].astype(str)
    df['username'] = df['username'].astype(str)
    df['hashtags'] = df['hashtags'].apply(lambda x: tuple(x))

    #Just making it neater, taking the columns we want
    df = df[["username","bio","followers","followings","posts","category","hashtags"]] #,"sentiment"

    #this will be the final table shown after filtering
    filtered_df = df

    ###Hashtag Filter###
    #Getting all the hashtags in the table
    hash = df['hashtags'].tolist()
    hash = list(itertools.chain.from_iterable(hash))
    col = df.columns.get_loc("hashtags")
    hashtag_df = pd.DataFrame() #initialise
    #select hashtag widget
    state.hashtag_filter = st.sidebar.multiselect(
        'Select hashtag',
        options=hash
    )
    #apply filter
    filtered_df['hashtags'] = filtered_df['hashtags'].apply(tuple)
    if state.hashtag_filter:
        for hash in state.hashtag_filter:
            for row in range((df.shape)[0]): 
                if hash in df.iat[row,col]:
                    hashtag_df = hashtag_df.append(df.iloc[row,:])
        if hashtag_df.empty == False:
            filtered_df['hashtags'] = filtered_df['hashtags'].apply(lambda x: tuple(x))
            filtered_df = pd.merge(hashtag_df,filtered_df, how = 'inner')
            filtered_df['hashtags'] = filtered_df['hashtags'].apply(lambda x: str(x))
            placeholder.table(filtered_df)
            filtered_df['hashtags'] = filtered_df['hashtags'].apply(lambda x: ast.literal_eval(x))
        else:
            for col in hashtag_df: 
                hashtag_df[col] = hashtag_df[col].fillna('NA')


    ###Followers Filter###
    followers_df = pd.DataFrame()           #initialise
    state.followers = st.sidebar.slider(    #followers slider widget
        'Select follower range',
        1000, 10000, (1000, 10000), step=100
    )
    min_fol = state.followers[0]
    max_fol = state.followers[1]
    col = df.columns.get_loc("followers")

    #apply filter
    if state.followers:
        for row in range((df.shape)[0]): 
            followers_count = df.iat[row,col]
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
            print("followers_df", followers_df)
            print("filtered_df",filtered_df)
            filtered_df["followers"] = filtered_df["followers"].astype(int)
            followers_df["followers"] = followers_df["followers"].astype(int)
            filtered_df['hashtags'] = filtered_df['hashtags'].apply(lambda x: tuple(x))     
            filtered_df = pd.merge(followers_df,filtered_df, how = 'inner')
            print("filtered_df",filtered_df)

        
        #streamlit table can't parse the tuple/list, so just converting to string and displaying the table before reverting back
        filtered_df['hashtags'] = filtered_df['hashtags'].apply(lambda x: str(x))    #convert to string
        placeholder.table(filtered_df)            #display table
        filtered_df['hashtags'] = filtered_df['hashtags'].apply(lambda x: ast.literal_eval(x)) #convert back to tuple

    #streamlit table can't parse the tuple/list, so just converting to string and displaying the table before reverting back
    filtered_df['hashtags'] = filtered_df['hashtags'].apply(lambda x: str(x))    
    placeholder.table(filtered_df)
    filtered_df['hashtags'] = filtered_df['hashtags'].apply(lambda x: ast.literal_eval(x))    
#     cds = ColumnDataSource(filtered_df)
#     columns = [
#     TableColumn(field="bio",title="bio"),# formatter = HTMLTemplateFormatter(template="""{wordWrap: ‘break-word’}<%= value %>""")),#, width=200),
#     TableColumn(field="category",title="category"),#, width=200),
#     TableColumn(field="followers",title="followers"),#, width=200),
#     TableColumn(field="followings",title="followings"),#, width=200),
#     TableColumn(field="hashtags",title="hashtags"),#, width=200),
#     TableColumn(field="posts",title="posts"),#, width=200),
#     TableColumn(field="username",title="username"),#, width=200),          
#     ]
# #     cds.selected.js_on_change(
# #         "indices",
# #         CustomJS(
# #                 args=dict(source=cds),
# #                 code="""
# #                 document.dispatchEvent(
# #                 new CustomEvent("INDEX_SELECT", {detail: {data: source.selected.indices}})
# #                 )
# #                 """
# #         )
# #     )
#     p = DataTable(source=cds, columns=columns, css_classes=["all"], aspect_ratio="auto", width=1500)#, width=500, height=5000)
#     result = streamlit_bokeh_events(bokeh_plot=p, events="INDEX_SELECT", key="foo", refresh_on_update=True, debounce_time=0)#, override_height=1000)

