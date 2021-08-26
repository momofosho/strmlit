import streamlit as st
import influencer_page, posts_page, home, profile #to display the other pages
import json
import requests
import pyrebase
from getpass import getpass
import sessionstate
import streamlit as st
from streamlit.hashing import _CodeHasher
try:
    # Before Streamlit 0.65
    from streamlit.ReportThread import get_report_ctx
    from streamlit.server.Server import Server
except ModuleNotFoundError:
    # After Streamlit 0.65
    from streamlit.report_thread import get_report_ctx
    from streamlit.server.server import Server

    
    
def main():
    state = _get_state() #using sessionstate.py, this allows the app to store and save state variables across pages
    if state.user is None: #initialise
        state.user = False

    if not state.user:
        loginSignup(state)
        state.sync() #save state user once login/signup
    # state.user="test-user"
    
    else:
        pages = {
            "Profile": profile.profile,
            "Influencer Page": influencer_page.influencerspage,
            "Posts Page": posts_page.postspage
        }

        if state.query_username: #in "posts page" if click on influencer, will show "home"
            home.home(state)
        else:
        # Display the selected page with the session state
            st.sidebar.title(":floppy_disk: Pages")
            options = tuple(pages.keys())
            state.page = st.sidebar.radio("Select your page", options, options.index(state.page) if state.page else 0)
            pages[state.page](state)

    # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
    state.sync()


def loginSignup(state):
    #initialise firebase for user login/sign up
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
    
    #st.empty() are placeholders for streamlit widgets (we use that to make things 'disappear'/replace)
    forgot_text = st.empty()
    title = st.empty()
    email = st.empty()
    password =  st.empty()
    cola, colb, _ = st.columns(3)
    with cola:
        placeholder = st.empty() #to interchange login&signup button
    with colb:
        forgotpass = st.empty() #checkbox for "forgot password"
    title.title("iota influence")
    text_email = email.text_input("Email") #user input
    text_password = password.text_input("Password", type="password") #user input
    

    #Change Login/Signup button depending on the "Already/Don't have an account? Login/Signup" hyperlink
    query_params = st.experimental_get_query_params() #query params that are in the url link
    tabs = ["Login", "Signup"]
    if "tab" in query_params:
        active_tab = query_params["tab"][0]
    else:
        active_tab = "Login"
    if active_tab not in tabs: #default tab is Login
        active_tab = "Login"  
    non_active_tab = [x for x in tabs if x!=active_tab][0]
    display_text = {"Login": "Already have an account? Login", "Signup":"Don't have an account? Sign up"}
    
    #Here the url in the hyperlink will have the parameter e.g. "?tab=Login" to indicate which page we want
    signup_login_hyperlink = f"""
        <a class="nav-item" href="?tab={non_active_tab}" id="signuploginlink">{display_text[non_active_tab]}</a>
    """
    placeholder_hyperlink = st.empty()
    placeholder_hyperlink.markdown(signup_login_hyperlink, unsafe_allow_html=True)

    #Functions using firebase signup/login
    def signUp():
        #create users
        while not state.user:
            try:
                user = auth.create_user_with_email_and_password(text_email, text_password)
                # user_email = text_email
                # user_password = text_password
                user=str(user)
            except requests.HTTPError as e:
                error_json = e.args[1]
                error = json.loads(error_json)['error']['message']
                if error == "EMAIL_EXISTS":
                    st.error("Email already exists. Login instead")
                else: st.error(error)
                st.stop()
        successful=True
        print("Success .... ")
        email.empty()
        password.empty()
        placeholder.empty()
        placeholder_hyperlink.empty()
        return str(user)

    def login():
        while not state.user:
            try:
                login = auth.sign_in_with_email_and_password(text_email, text_password)
                state.user=str(login)
            except requests.HTTPError as e:
                error_json = e.args[1]
                error = json.loads(error_json)['error']['message']
                st.error(error)
                st.stop()
        # #send email verification
        # auth.send_email_verification(login['idToken'])
        # #reset the password
        # auth.send_password_reset_email(email)
        successful=True
        print("Success ... ")
        email.empty()
        password.empty()
        placeholder.empty()
        placeholder_hyperlink.empty()
        return str(login)

    #Displaying respective buttons depending on the tab   
    if active_tab == "Login":
        if placeholder.button("Login", key="loginbtn"):
            login() #calling the function
        if forgotpass.checkbox("Forgot password?"):
            password.empty()
            title.empty()
            forgot_text.info("Enter email to reset password")
            if placeholder.button("Submit"):
                auth.send_password_reset_email(text_email)
                forgot_text.success("Sent email to reset password!")
            
    elif active_tab == "Signup":
        if placeholder.button("Sign up", key="signupbutton"):
            signUp() #calling the function



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



 
