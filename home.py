from logging import PlaceHolder
from urllib.request import HTTPPasswordMgrWithDefaultRealm
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

import sessionstate
import streamlit as st
from streamlit.hashing import _CodeHasher
import ast
import pyrebase

try:
    # Before Streamlit 0.65
    from streamlit.ReportThread import get_report_ctx
    from streamlit.server.Server import Server
except ModuleNotFoundError:
    # After Streamlit 0.65
    from streamlit.report_thread import get_report_ctx
    from streamlit.server.server import Server


# import os
# os.system('python -m nltk.downloader all')

import importlib
# app_py = importlib.import_module('app')
# user = app_py.emailpass()

import sessionstate
from streamlit.hashing import _CodeHasher

def home(state):
# def main():
    state = _get_state()

    #####test-user
    # state.user="{'kind': 'identitytoolkit#VerifyPasswordResponse', 'localId': 'TH0KU75xQWca2lAWNOdI9vSlSkE3', 'email': 'momofosho999@gmail.com', 'displayName': '', 'idToken': 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjFiYjk2MDVjMzZlOThlMzAxMTdhNjk1MTc1NjkzODY4MzAyMDJiMmQiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vaW90YS13ZWItYXBwIiwiYXVkIjoiaW90YS13ZWItYXBwIiwiYXV0aF90aW1lIjoxNjI3MjE2NDIwLCJ1c2VyX2lkIjoiVEgwS1U3NXhRV2NhMmxBV05PZEk5dlNsU2tFMyIsInN1YiI6IlRIMEtVNzV4UVdjYTJsQVdOT2RJOXZTbFNrRTMiLCJpYXQiOjE2MjcyMTY0MjAsImV4cCI6MTYyNzIyMDAyMCwiZW1haWwiOiJtb21vZm9zaG85OTlAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsibW9tb2Zvc2hvOTk5QGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.MjCLHzI2bzNJUID4cZxo_RHS1Ig0n5qyfXGsBEGm2Vyb-HarryvfuGnfPZV1qxciOdSCduK82HxhzqhodTWzhTLZcUMOgFdWhFvf0DMTPCEUtOapgC1xtZ7B9K9s1RgOUaPozkKjTCo9T3Q8JqDR4PJRFxzCLC4wlIBOb2joBncNMJwnEUZHbU5PbGXjs0leZguwmxdbc0fIaLrPfZIX4_6KmSNwmKTcIyz4Liguq6KhrhC84yhKXOhJJuA-KZhB4jCmjqHg43U_H3RSx3LyVDQKwfI6mEAM_q5vlzFQgmdnZp06B-uPP1BNH1kIJ4fEaD0W3FbY2mSOiGcZfYq6CQ', 'registered': True, 'refreshToken': 'AGEhc0CkG3RvP_lkBO0YZZiBUDzLL6LbIdL2C_yLxqzew1sF4iXa6ty3N6WmgJ8e2S8bSQqb8BwUyNdOHZf5NABkglBDK0Mje8foil_A-s9UnMIU6uJqq7vahKXKNsmHC-Bf5YAmoOx_35dAdvNuRyp4n6EEsquKomdx2m_DB6P_XEzQ2OmNKLuGJhvWavzt6RfT3YWStyqAu9knqud0fdWFnrHfvM3lIQ', 'expiresIn': '3600'}"
    
    # st.write("user:::", state.user)

    # app_state = st.experimental_get_query_params()
    # default_title = app_state["username"] if "username" in app_state else ""
    # title = st.text_input('Influencer Username', value = default_title)
    # app_state["username"] = title
    # a = st.experimental_get_query_params()["username"][0]
    
    #####test query
    # state.query_username = "skinco_clinic"
    a = state.query_username

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
    # st.table(df1)
    # st.write(user_info)

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
    if user_info['bio'].any():
        location = user_info['bio'][0]  #location
    else: location = '-'
    contact_details = '-'
    



    back, title, bookmark = st.beta_columns([1, 3,1])
    with back:
        if st.button("back"):
            state.query_username=False
            return
    if not state.query_username: return
    title.markdown(f"""<h1 style='text-align: left; color: red;'>{username}</h1>""", unsafe_allow_html=True)
    

    # if state.bookmarked is None:
    #     state.bookmarked = False


    firebaseConfig = {
        "apiKey": "AIzaSyBHlJZLmdxtOQtM10CkOP2pNvuO81Elirg",
        "authDomain": "iota-web-app.firebaseapp.com",
        "databaseURL": "https://iota-web-app-default-rtdb.asia-southeast1.firebasedatabase.app",
        "projectId": "iota-web-app",
        "storageBucket": "iota-web-app.appspot.com",
        "messagingSenderId": "390789359948",
        "appId": "1:390789359948:web:c59018f57465985e6307e9",
        "measurementId": "G-RPSDKG694K"
        } 

    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    db = firebase.database()
    bookmark_list = db.get().val()
    # st.write(bookmark_list, type(bookmark_list))
    
    current_user = str(ast.literal_eval(state.user)["email"])
    html_esc_user = current_user.replace(".","&period;")
    html_esc_query = state.query_username.replace(".", "&period;")


    
    # st.write("at first", state.bookmarked)
    if html_esc_user in bookmark_list:
        if html_esc_query in bookmark_list[html_esc_user]:
            db_bookmarked = True
        else: db_bookmarked=False
    else: db_bookmarked=False

    # st.write("yes in db", state.bookmarked)

    state.bookmarked = bookmark.checkbox("Bookmarked", value=db_bookmarked)
    
    # def clickbookmark():
    #     if state.bookmarked:
    #         state.bookmarked = False
    #     else:
    #         state.bookmarked = True
    # bookmark_btn = bookmark.button("Bookmark", on_click=clickbookmark)
    # # bookmark_btn.enabled=False
    # state.bookmarked = bookmark_btn
    

    # st.markdown(location +'\t\t'+ contact_details)
    # primaryColor = st.get_option("theme.primaryColor")
    # s = f"""
    # <style>
    # div.stButton > button:first-child {{ border: 5px solid {primaryColor}; border-radius:20px 20px 20px 20px; }}
    # <style>
    # """
    # st.markdown(s, unsafe_allow_html=True)

    

    

    if state.bookmarked:
        
        # data to save
        data = {"name": html_esc_query}
        db.child(html_esc_user).child(html_esc_query).update(data)
        st.success("added to bookmark")
        # s = f"""
        # <style>
        # div.stButton > button:first-child {{ border: 5px solid #F63366; background-color: #F63366; color: #F0F2F6; border-radius:20px 20px 20px 20px}}
        # <style>
        # """
        # st.markdown(s, unsafe_allow_html=True)
        # bookmark.button("testing")
    else:
#         st.write("bookmarked is false")
        # st.write(bookmark_list)
        if html_esc_user in bookmark_list:
            user_saved_list = bookmark_list[html_esc_user]
            if html_esc_query in user_saved_list:
                db.child(html_esc_user).child(html_esc_query).remove()
                st.success("Removed from bookmarks")
        # s = f"""
        # <style>
        # div.stButton > button:first-child {{ border: 5px solid {primaryColor}; border-radius:20px 20px 20px 20px; }}
        # <style>
        # """
        # st.markdown(s, unsafe_allow_html=True)


    # import toml
    # primaryColor = toml.load(".streamlit/config.toml")['theme']['primaryColor']
    # s = f"""
    # <style>
    # div.stButton > button:first-child {{ border: 5px solid {primaryColor}; border-radius:20px 20px 20px 20px; }}
    # <style>
    # """
    # st.markdown(s, unsafe_allow_html=True)

    posts, followers, following,  = st.beta_columns(3)
    likes, comments, d = st.beta_columns(3)
    with posts:
        st.write("posts")
        st.write(int(user_info['posts'][0]))


    with followers:
        st.write("followers")
        st.write(int(user_info['followers'][0]))

    with following:
        st.write("following")
        st.write(int(user_info['followings'][0]))

    with likes:
        st.write("likes")
        st.write(int(posts_info['likes'].sum(skipna=True)))

    with comments:
        st.write("comments")
        sum =0
        for com in posts_info['comments']:
            sum = sum + len(com)
        st.write(int(sum))
        
    
    
    st.write("Likes + Comments related to")
    hashtag_list = df1[df1["username"]==state.query_username]['hashtags'].tolist()
    hashtag_list = list(itertools.chain.from_iterable(hashtag_list))
    hashtag_filter_multiselect = st.multiselect(
        'Select hashtag',
        options=hashtag_list
    )
    st.write(df1[df1["username"]==state.query_username and tag in "hashtags" for tag in hashtag_filter_multiselect])
    likes2, comments2, d2 = st.beta_columns(3)
#     with likes2:
#         st.write("likes")
#         count=0
#         hash_df = pd.DataFrame()
#         for tag in hashtag_filter_multiselect:
#             hash_df
#             count+=
#         st.write(int(posts_info[posts_info]['likes'].sum(skipna=True)))



#     from bokeh.io import show
#     from bokeh.models import CheckboxButtonGroup, CustomJS

#     LABELS = ["Hashtags", "Keywords", "Posts"]

#     checkbox_button_group = CheckboxButtonGroup(labels=LABELS, active=[0, 1])
#     checkbox_button_group.js_on_click(CustomJS(code="""
#         console.log('checkbox_button_group: active=' + this.active, this.toString())
#     """))

#     st.bokeh_chart(checkbox_button_group)
#     #show(checkbox_button_group)
    
    
    
    
#     from bokeh.io import show
#     from bokeh.models import CustomJS, RadioButtonGroup

#     LABELS = ["Hashtags", "Keywords", "Posts"]
    
#     stwrite = st.empty()

# #     def write_active():
# #         stringwrite = "ASDFASDFASDFSASDF"+str(radio_button_group.active)
# #         stwrite.write(stringwrite)
#     radio_button_group = RadioButtonGroup(labels=LABELS, active=0)
#     radio_button_group.on_change('active', lambda attr, old, new: update())
# #     radio_button_group.on_click(write_active())
# #     radio_button_group.js_on_click(CustomJS(code="""
# #         console.log('radio_button_group: active=' + this.active, this.toString())
# #     """))
# #     st.write(radio_button_group.js_on_click(CustomJS(code="""
# #         console.log('radio_button_group: active=' + this.active, this.toString())
# #     """)))
# #     radio_button_group.on_change('active', lambda attr, old, new: update())
    
#     st.bokeh_chart(radio_button_group)
#     stwrite.write(radio_button_group.active)
    


    stop_words = set(stopwords.words('english'))
    
    for cap in posts_info["caption"]:
        #cap = cap.replace('.','')
        word_tokens = word_tokenize(cap)
        filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
        filtered_sentence = []
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)

    if '#' in filtered_sentence:
        hash = filtered_sentence.index('#')
    else:
        hash = len(filtered_sentence)-1 #if no hashtag then just use end of the sentence
    filtered_sentence = filtered_sentence[0:hash]
    print(filtered_sentence)

    # posts_info = posts_info.join(pd.DataFrame(data = {"processed caption" : np.array(filtered_sentence)}))
    # st.table(posts_info)

#     st.markdown(
#         '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">',
#         unsafe_allow_html=True,
#     )

#     query_params = st.experimental_get_query_params()
#     # st.title(query_params)
#     # query_params = app_state
#     tabs = ["Hashtags", "Keywords", "Posts"]
#     if "tab" in query_params:
#         active_tab = query_params["tab"][0]
#     else:
#         active_tab = "Hashtags"

#     if active_tab not in tabs:
#         active_tab = "Hashtags"

#     import string
#     a_dash = a
#     punctuations = {"_","."}

#     for ele in a_dash:
#         if ele in punctuations:
#             a_dash = a_dash.replace(ele, " ")
#     a_dash = '-'.join(a_dash.split())

#     li_items = "".join(
#         f"""
#         <li class="nav-item">
#             <a class="nav-link{' active' if t==active_tab else ''}" href="?username={a}&tab={t}#{a_dash}">{t}</a>
#         </li>
#         """
#         for t in tabs
#     )
#     tabs_html = f"""
#         <ul class="nav nav-tabs">
#         {li_items}
#         </ul>
#     """

#     st.markdown(tabs_html, unsafe_allow_html=True)
#     st.markdown("<br>", unsafe_allow_html=True)
    if "active_tab" not in st.session_state: #default tab
        st.session_state.active_tab = "Hashtags"
    
    import numpy as np
    if "board" not in st.session_state: #initialise
        st.session_state.board = np.array([["Hashtags","Keywords","Posts"]]) #tabs #np.full((1, 3), ".", dtype=str)   #np.array([["."],["."],["."]])#

    # Define callbacks to handle button clicks.
    def handle_click(i, j):
        st.session_state.active_tab = st.session_state.board[i, j]
    # Show one button for each field.
    for i, row in enumerate(st.session_state.board):
        cols = st.beta_columns([0.14, 0.14, 0.14, 0.58])
        for j, field in enumerate(row):
            cols[j].button(
                field,
                key=f"{i}-{j}",
                on_click=handle_click,
                args=(i, j),
            )
    

    if st.session_state.active_tab == "Hashtags":
        flat_list = [item for sublist in posts_info['hashtags'] for item in sublist]
        flat_str = ' '.join(flat_list)
        wordcloud = WordCloud(background_color = 'lightblue', width = 1000, height = 1000, max_words = 50).generate(flat_str)

        plt.rcParams['figure.figsize'] = (10, 10)
        plt.title('Hashtags', fontsize = 20)
        plt.axis('off')
        plt.imshow(wordcloud)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()


    elif st.session_state.active_tab == "Keywords":
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

    elif st.session_state.active_tab == "Posts":
        import plotly.express as px

        df = pd.DataFrame(['skincare','health','others'])
        df = df.rename(columns={0:'category'})
        df['values'] = pd.DataFrame([20,4,11])
        #st.write(df)
        fig = px.pie(df, values='values', names='category')
        st.plotly_chart(fig)
    else:
        st.error("Something has gone terribly wrong.")

    state.sync()



def _get_session():
    session_id = get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")
    
    return session_info.session


def _get_state(hash_funcs=None):
    session = _get_session()

    if not hasattr(session, "_custom_session_state"):
        session._custom_session_state = sessionstate._SessionState(session, hash_funcs)

    return session._custom_session_state
if __name__ == "__main__":
    main()



# app_state = st.experimental_get_query_params()
# default_title = app_state["username"] if "username" in app_state else ""
# title = st.text_input('Influencer Username', value = default_title)
# app_state["username"] = title

# a = st.experimental_get_query_params()["username"][0]

# # Authenticate to Firestore with the JSON account key.
# db = firestore.Client.from_service_account_json("firestore-key.json")

# #doc_id = db.collection("test5")
# my_dict = {}
# usernames = []
# documents = db.collection(u'test6')

# #influencer data
# docs = documents.stream()
# my_dict1 = { doc.id: doc.to_dict() for doc in docs }
# df1 = pd.DataFrame.from_dict(my_dict1)
# df1 = df1.transpose()
# user_info = df1[df1.username.str.contains(a)]
# # st.table(df1)
# # st.write(user_info)

# #posts data
# for doc in documents.stream():
    
#     # usernames.append(doc.id)
#     if doc.id == a:
#         print(doc.id)
#         collections = documents.document(doc.id).collections()
#         for collection in collections:
            
#             for doc in collection.stream():
#                 my_dict[doc.id] = doc.to_dict()

# # print(my_dict)
# posts_info = pd.DataFrame.from_dict(my_dict)
# posts_info = posts_info.transpose()
# #st.table(posts_info)

# username = a
# location = user_info['bio'][0]  #location
# contact_details = '-'
# st.title(username)
# st.markdown(location +'\t\t'+ contact_details)

# posts, followers, following, likes, comments = st.beta_columns(5)

# with posts:
#   st.write("posts")
#   st.write(str(user_info['posts'][0]))


# with followers:
#   st.write("followers")
#   st.write(str(user_info['followers'][0]))

# with following:
#   st.write("following")
#   st.write(str(user_info['followings'][0]))

# with likes:
#   st.write("likes")
#   st.write(str(posts_info['likes'].sum(skipna=True)))

# with comments:
#   st.write("comments")
#   sum =0
#   for com in posts_info['comments']:
#     sum = sum + len(com)
#   st.write(str(sum))


# stop_words = set(stopwords.words('english'))
 
# for cap in posts_info["caption"]:
#   #cap = cap.replace('.','')
#   word_tokens = word_tokenize(cap)
#   filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
#   filtered_sentence = []
#   for w in word_tokens:
#       if w not in stop_words:
#           filtered_sentence.append(w)

# if '#' in filtered_sentence:
#     hash = filtered_sentence.index('#')
# else:
#     hash = len(filtered_sentence)-1 #if no hashtag then just use end of the sentence
# filtered_sentence = filtered_sentence[0:hash]
# print(filtered_sentence)

# # posts_info = posts_info.join(pd.DataFrame(data = {"processed caption" : np.array(filtered_sentence)}))
# # st.table(posts_info)

# st.markdown(
#     '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">',
#     unsafe_allow_html=True,
# )

# # query_params = st.experimental_get_query_params()
# # st.title(query_params)
# query_params = app_state
# tabs = ["Hashtags", "Keywords", "Posts"]
# if "tab" in query_params:
#     active_tab = query_params["tab"][0]
# else:
#     active_tab = "Hashtags"

# if active_tab not in tabs:
#     active_tab = "Hashtags"

# import string
# a_dash = a
# punctuations = {"_","."}

# for ele in a_dash:
#     if ele in punctuations:
#         a_dash = a_dash.replace(ele, " ")
# a_dash = '-'.join(a_dash.split())

# li_items = "".join(
#     f"""
#     <li class="nav-item">
#         <a class="nav-link{' active' if t==active_tab else ''}" href="?username={a}&tab={t}#{a_dash}">{t}</a>
#     </li>
#     """
#     for t in tabs
# )
# tabs_html = f"""
#     <ul class="nav nav-tabs">
#     {li_items}
#     </ul>
# """

# st.markdown(tabs_html, unsafe_allow_html=True)
# st.markdown("<br>", unsafe_allow_html=True)

# if active_tab == "Hashtags":
#     flat_list = [item for sublist in posts_info['hashtags'] for item in sublist]
#     flat_str = ' '.join(flat_list)
#     wordcloud = WordCloud(background_color = 'lightblue', width = 1000, height = 1000, max_words = 50).generate(flat_str)

#     plt.rcParams['figure.figsize'] = (10, 10)
#     plt.title('Hashtags', fontsize = 20)
#     plt.axis('off')
#     plt.imshow(wordcloud)
#     st.set_option('deprecation.showPyplotGlobalUse', False)
#     st.pyplot()


# elif active_tab == "Keywords":
#     filtered_str = ' '.join(filtered_sentence)
#     filtered_str = re.sub(r'[^\w\s]', '', filtered_str)
#     print(filtered_str)

#     wordcloud = WordCloud(background_color = 'lightblue', width = 1000, height = 1000, max_words = 50).generate(filtered_str)

#     plt.rcParams['figure.figsize'] = (10, 10)
#     plt.title('Caption Keywords', fontsize = 20)
#     plt.axis('off')
#     plt.imshow(wordcloud)
#     st.set_option('deprecation.showPyplotGlobalUse', False)
#     st.pyplot()

# elif active_tab == "Posts":
#     import plotly.express as px

#     df = pd.DataFrame(['skincare','health','others'])
#     df = df.rename(columns={0:'category'})
#     df['values'] = pd.DataFrame([20,4,11])
#     #st.write(df)
#     fig = px.pie(df, values='values', names='category')
#     st.plotly_chart(fig)
# else:
#     st.error("Something has gone terribly wrong.")
