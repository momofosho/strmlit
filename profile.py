import streamlit as st
import sessionstate
from streamlit.hashing import _CodeHasher
import pyrebase
import ast

def profile(state):
    st.title("Profile")
    current_user = str(ast.literal_eval(state.user)["email"])
    st.write("Name: ", current_user)
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

    if st.button("Change password"):
        auth.send_password_reset_email(current_user)
        st.success("Sent email to reset password")
    
    st.title("Bookmarks")
    db = firebase.database()
    bookmark_list = db.get().val()
    # st.write(bookmark_list, type(bookmark_list))
    
    current_user = str(ast.literal_eval(state.user)["email"])
    html_esc_user = current_user.replace(".","&period;")
    
    if html_esc_user in bookmark_list:
        bookmarks = bookmark_list[html_esc_user]
    else:
        bookmarks = {}
    
    import html
    for i in bookmarks:
        # html_esc_query = state.query_username.replace(".", "&period;")
        if st.checkbox(html.unescape(i), value=True):
            pass
        else:
            db.child(html_esc_user).child(i).remove()
            st.error("Removed from bookmarks")


