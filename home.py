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
import importlib
import sessionstate
from streamlit.hashing import _CodeHasher

def home(state):
# def main():
    state = _get_state()
    #####test-user
    # state.user="{'kind': 'identitytoolkit#VerifyPasswordResponse', 'localId': 'TH0KU75xQWca2lAWNOdI9vSlSkE3', 'email': 'momofosho999@gmail.com', 'displayName': '', 'idToken': 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjFiYjk2MDVjMzZlOThlMzAxMTdhNjk1MTc1NjkzODY4MzAyMDJiMmQiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vaW90YS13ZWItYXBwIiwiYXVkIjoiaW90YS13ZWItYXBwIiwiYXV0aF90aW1lIjoxNjI3MjE2NDIwLCJ1c2VyX2lkIjoiVEgwS1U3NXhRV2NhMmxBV05PZEk5dlNsU2tFMyIsInN1YiI6IlRIMEtVNzV4UVdjYTJsQVdOT2RJOXZTbFNrRTMiLCJpYXQiOjE2MjcyMTY0MjAsImV4cCI6MTYyNzIyMDAyMCwiZW1haWwiOiJtb21vZm9zaG85OTlAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsibW9tb2Zvc2hvOTk5QGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.MjCLHzI2bzNJUID4cZxo_RHS1Ig0n5qyfXGsBEGm2Vyb-HarryvfuGnfPZV1qxciOdSCduK82HxhzqhodTWzhTLZcUMOgFdWhFvf0DMTPCEUtOapgC1xtZ7B9K9s1RgOUaPozkKjTCo9T3Q8JqDR4PJRFxzCLC4wlIBOb2joBncNMJwnEUZHbU5PbGXjs0leZguwmxdbc0fIaLrPfZIX4_6KmSNwmKTcIyz4Liguq6KhrhC84yhKXOhJJuA-KZhB4jCmjqHg43U_H3RSx3LyVDQKwfI6mEAM_q5vlzFQgmdnZp06B-uPP1BNH1kIJ4fEaD0W3FbY2mSOiGcZfYq6CQ', 'registered': True, 'refreshToken': 'AGEhc0CkG3RvP_lkBO0YZZiBUDzLL6LbIdL2C_yLxqzew1sF4iXa6ty3N6WmgJ8e2S8bSQqb8BwUyNdOHZf5NABkglBDK0Mje8foil_A-s9UnMIU6uJqq7vahKXKNsmHC-Bf5YAmoOx_35dAdvNuRyp4n6EEsquKomdx2m_DB6P_XEzQ2OmNKLuGJhvWavzt6RfT3YWStyqAu9knqud0fdWFnrHfvM3lIQ', 'expiresIn': '3600'}"
    #####test query
    # state.query_username = "ellisastore"
    a = state.query_username

    #Firebase
    db = firestore.Client.from_service_account_json("firestore-key.json")
    my_dict = {}
    usernames = []
#     documents = db.collection(u'test6')
    documents = db.collection(u'eczema')

    #influencer data
    docs = documents.stream()
    my_dict1 = { doc.id: doc.to_dict() for doc in docs }
    df1 = pd.DataFrame.from_dict(my_dict1)
    df1 = df1.transpose()
    user_info = df1[df1.username.str.contains(a)]


    #posts data
    for doc in documents.stream():        
        # usernames.append(doc.id)
        if doc.id == a:
            print(doc.id)
            collections = documents.document(doc.id).collections()
            for collection in collections:                
                for doc in collection.stream():
                    my_dict[doc.id] = doc.to_dict()


    posts_info = pd.DataFrame.from_dict(my_dict)
    posts_info = posts_info.transpose()

    
    username = a
    if user_info['bio'].any():
        location = user_info['bio'][0]  #location
    else: location = '-'
    contact_details = '-'
    
    
    #Back button, title, bookmark checkbox
    back, title, bookmark = st.columns([1, 3,1])
    with back:
    #back button
        if st.button("back"):
            state.query_username=False
            return
    if not state.query_username: return #go back to app.py
    #title
    st.markdown(f"""<h1 style='text-align: left; color: green;'>{username}</h1>""", unsafe_allow_html=True)

    #bookmark
    #For user to bookmark this influencer (updates firebase Realtime Database)
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
    
    current_user = str(ast.literal_eval(state.user)["email"]) #for now user signs in with email, so that's our way of identifying them
    html_esc_user = current_user.replace(".","&period;") #'.' the dot messes with file naming, so just replacing it
    html_esc_query = state.query_username.replace(".", "&period;") #'.' the dot messes with file naming, so just replacing it
    
    #checking the user's bookmark list from the realtime database
    if html_esc_user in bookmark_list:
        if html_esc_query in bookmark_list[html_esc_user]:
            db_bookmarked = True
        else: db_bookmarked=False
    else: db_bookmarked=False

    #streamlit checkbox widget to bookmark
    state.bookmarked = bookmark.checkbox("Bookmarked", value=db_bookmarked) #default value set to whether it is in database (previously bookmarked)

    if state.bookmarked: #if bookmark checkbox True, add to database
        data = {"name": html_esc_query}
        db.child(html_esc_user).child(html_esc_query).update(data)
        st.success("added to bookmark")
  
    else: #remove from database
        if html_esc_user in bookmark_list:
            user_saved_list = bookmark_list[html_esc_user]
            if html_esc_query in user_saved_list:
                db.child(html_esc_user).child(html_esc_query).remove()
                st.success("Removed from bookmarks")

                
                
                
    #influencer stats            
    posts, followers, following,  = st.columns(3)
    likes, comments, d = st.columns(3)
    with posts:
        st.write("posts")
        st.write(int(user_info['posts'][0]))

    with followers:
        st.write("followers")
        st.write(int(user_info['followers'][0]))

    with following:
        st.write("following")
        st.write(int(user_info['followings'][0]))
        
    #likes and comments related to selected hashtags
    st.title("likes + comments related to:")
    hashtag_list = df1[df1["username"]==state.query_username]['hashtags'].tolist()
    hashtag_list = list(itertools.chain.from_iterable(hashtag_list))
    hashtag_list = list(set([i.lower() for i in hashtag_list]))
    state.hashtag_filter_multiselect = st.multiselect(
        'Select hashtag',
        options=hashtag_list,
        default=state.postpg_hashtag_filter,
    )
    pattern = '|'.join(state.hashtag_filter_multiselect)
    likes2, comments2, d2 = st.columns(3)
    with likes2:
        st.write("likes")
        col_hashtag = posts_info.columns.get_loc("hashtags")
#         col_username = posts_info.columns.get_loc("username")
        col_likes = posts_info.columns.get_loc("likes")
#         col_comments = posts_info.columns.get_loc("comments")
        tot_likes=0
        for row in range((posts_info.shape)[0]):
#             for col in range((posts_info.shape)[1]):
                for tag in state.hashtag_filter_multiselect:
                    if tag in posts_info.iat[row,col_hashtag]:
#                 if any(tag in posts_info.iat[row,col_hashtag] for tag in state.hashtag_filter_multiselect):
                        try:
                            tot_likes+=posts_info.iat[row,col_likes] #.sum()
                        except:
                            tot_likes+=0
                        break
        st.write(int(tot_likes))
    with comments2:
        st.write("comments")
        col_hashtag = posts_info.columns.get_loc("hashtags")
        #         col_username = posts_info.columns.get_loc("username")
#         col_likes = posts_info.columns.get_loc("likes")
        col_comments = posts_info.columns.get_loc("comments")
        tot_comments=0
        for row in range((posts_info.shape)[0]):
#             for col in range((posts_info.shape)[1]):
                for tag in state.hashtag_filter_multiselect:
                    if tag in posts_info.iat[row,col_hashtag]:
                        try:
                            tot_comments+=len(posts_info.iat[row,col_comments])
                        except:
                            tot_comments+=0
                        break
        st.write(int(tot_comments))


        
        
    #Caption keywords
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

    #Dashboard, navigation tabs
    st.title("dashboard")
    if "active_tab" not in st.session_state: #default tab
        st.session_state.active_tab = "Hashtags"
    
    import numpy as np
    if "tabs" not in st.session_state: #initialise
        st.session_state.tabs = np.array([["Hashtags","Keywords","Posts"]]) 

    # Define callbacks to handle button clicks.
    def handle_click(i, j):
        st.session_state.active_tab = st.session_state.tabs[i, j] #on button click, set "active_tab" to be respective tab
    # Show one button for each field.
    for i, row in enumerate(st.session_state.tabs):
        cols = st.columns([0.14, 0.14, 0.14, 0.58])
        for j, field in enumerate(row):
            cols[j].button(
                field,
                key=f"{i}-{j}",
                on_click=handle_click,
                args=(i, j),
            )
    
    #Hashtags wordcloud
    if st.session_state.active_tab == "Hashtags":
        try:
            flat_list = [item for sublist in posts_info['hashtags'] for item in sublist]
            flat_str = ' '.join(flat_list)
            wordcloud = WordCloud(background_color = 'lightblue', width = 1000, height = 1000, max_words = 50).generate(flat_str)

            plt.rcParams['figure.figsize'] = (10, 10)
            plt.title('Hashtags', fontsize = 20)
            plt.axis('off')
            plt.imshow(wordcloud)
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()
        except:
            st.markdown("`There are no hashtags in the captions.`")

    #Caption keywords wordcloud
    elif st.session_state.active_tab == "Keywords":
        try:
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
        except:
            st.markdown("`There are no captions for this post.`")

    #Posts segmentation (here it is hardcoded, cos in backend we haven't run it for everyone yet)
    elif st.session_state.active_tab == "Posts":
        import plotly.express as px
        df = pd.DataFrame(['skincare','health','covid','others'])
        df = df.rename(columns={0:'category'})
        df['values'] = pd.DataFrame([20,4,6,11])
        #st.write(df)
        fig = px.pie(df, values='values', names='category')
        st.plotly_chart(fig)
    else:
        st.error("Something has gone terribly wrong.")
        
    #these are also hardcoded as we don't have access to Instagram Graph API "user insights" yet
    st.title("user insights")
    gender, location = st.columns(2)
    with gender:
        st.title("gender")    
        import plotly.express as px
        df = pd.DataFrame(['Women','Men'])
        df = df.rename(columns={0:'category'})
        df['values'] = pd.DataFrame([59.7,40.3])
        #st.write(df)
        fig = px.pie(df, values='values', names='category')
        st.plotly_chart(fig,use_container_width=True)
    with location:
        st.title("top locations")
        chart_data = pd.DataFrame(
#         np.random.randn(20, 6, 3),
        [[20,10,6,3,1]],
        columns=["Singapore", "Istanbul", "Hong Kong", "London","Malta"])
        st.bar_chart(chart_data,width=20)

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

# if __name__ == "__main__":
#     main()



