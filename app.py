import streamlit as st
from multiapp import MultiApp
#from apps import home, data, model # import your app modules here
import influencer_page, posts_page

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

import home
import profile

def main():
    state = _get_state()
    if state.user is None:
        state.user = False

    if not state.user:
        from bokeh.models.widgets import Panel, Tabs
        from bokeh.io import output_file, show
        from bokeh.plotting import figure
        
        
        import datetime
        import random

        import bokeh
        import bokeh.layouts
        import bokeh.models
        import bokeh.plotting
#         import markdown
        import pandas as pd
        import streamlit as st
        
        def results():
            N = 10
            data = dict(
                dates=[datetime.date(2014, 3, i + 1) for i in range(N)] * 100,
                downloads=[random.randint(0, 100) for i in range(N)] * 100,
            )
            source = bokeh.models.ColumnDataSource(data)

            columns = [
                bokeh.models.widgets.TableColumn(
                    field="dates", title="Date", formatter=bokeh.models.widgets.DateFormatter()
                ),
                bokeh.models.widgets.TableColumn(field="downloads", title="Downloads"),
            ]
            data_table = bokeh.models.widgets.DataTable(
                source=source, columns=columns, height=280, sizing_mode="stretch_width"
            )
            column = bokeh.layouts.Column(
                children=[data_table], sizing_mode="stretch_width"
            )
            return bokeh.models.Panel(child=column, title="Tables")

        def graphs():
            chart = bokeh.plotting.figure(sizing_mode="stretch_width", height=400)
            chart.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], line_width=3, color="navy", alpha=0.5)

            checkbox = bokeh.models.widgets.RadioButtonGroup(labels=["Total", "By product"], active=0)
            if checkbox == "By product":
                    checkbox_group = bokeh.models.widgets.CheckboxButtonGroup(labels=["Option 1", "Option 2", "Option 3"], active=[])

            column = bokeh.layouts.Column(
                chart,
                checkbox,
                sizing_mode="stretch_width"
            )    

            return bokeh.models.Panel(child=column, title="Plotting")        
        
        tabs = bokeh.models.Tabs(
        tabs=[
            results(),
            graphs(),
        ]
        )
        st.bokeh_chart(tabs)


        output_file("slider.html")

        p1 = figure(plot_width=300, plot_height=300)
        p1.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)
        tab1 = Panel(child=p1, title="circle")

        p2 = figure(plot_width=300, plot_height=300)
        p2.line([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], line_width=3, color="navy", alpha=0.5)
        tab2 = Panel(child=p2, title="line")

        tabs = Tabs(tabs=[ tab1, tab2 ])
        show(tabs)
#         st.write(show(tabs))
#         st.bokeh_chart(show(tabs))
#         st.bokeh_chart()
        loginSignup(state)
        state.sync()
    # state.user="test-user"
    
    else:
        pages = {
            # "Dashboard": pagedashboard.page_dashboard,
            # "Settings": pagesettings.page_settings,
            "Profile": profile.profile,
            "Influencer Page": influencer_page.influencerspage,
            "Posts Page": posts_page.postspage
            
        }


        # app_state = st.experimental_get_query_params()
        # displayhome = app_state["username"] if "username" in app_state else False
        
        if state.query_username:
            home.home(state)
        else:
        # Display the selected page with the session state
            st.sidebar.title(":floppy_disk: Page states")
            page = st.sidebar.radio("Select your page", tuple(pages.keys()))
            pages[page](state)


    # app = MultiApp()
    # st.markdown("""
    # # iota influence
    # """)
    # # Add all your application here
    # app.add_app("Influencers", influencer_page.app)
    # app.add_app("Posts", posts_page.app)

    # # The main app
    # app.run()



    # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
    state.sync()


# def page_dashboard(state):
#     st.title(":chart_with_upwards_trend: Dashboard page")
#     display_state_values(state)


# def page_settings(state):
#     st.title(":wrench: Settings")
#     display_state_values(state)

#     st.write("---")
#     options = ["Hello", "World", "Goodbye"]
#     state.input = st.text_input("Set input value.", state.input or "")
#     state.slider = st.slider("Set slider value.", 1, 10, state.slider)
#     state.radio = st.radio("Set radio value.", options, options.index(state.radio) if state.radio else 0)
#     state.checkbox = st.checkbox("Set checkbox value.", state.checkbox)
#     state.selectbox = st.selectbox("Select value.", options, options.index(state.selectbox) if state.selectbox else 0)
#     state.multiselect = st.multiselect("Select value(s).", options, state.multiselect)

#     # Dynamic state assignments
#     for i in range(3):
#         key = f"State value {i}"
#         state[key] = st.slider(f"Set value {i}", 1, 10, state[key])


# def display_state_values(state):
#     st.write("Input state:", state.input)
#     st.write("Slider state:", state.slider)
#     st.write("Radio state:", state.radio)
#     st.write("Checkbox state:", state.checkbox)
#     st.write("Selectbox state:", state.selectbox)
#     st.write("Multiselect state:", state.multiselect)
    
#     for i in range(3):
#         st.write(f"Value {i}:", state[f"State value {i}"])

#     if st.button("Clear state"):
#         state.clear()


def loginSignup(state):
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

    # email = make_recording_widget(st.empty)
    # password = make_recording_widget(st.empty)
    # placeholder = make_recording_widget(st.empty)
    # placeholder_checkbox = make_recording_widget(st.empty)

    email = st.empty()
    password =  st.empty()
    placeholder = st.empty() #to interchange login&signup button

    text_email = email.text_input("Email")
    text_password = password.text_input("Password", type="password")
   

  
    query_params = st.experimental_get_query_params()
    tabs = ["Login", "Signup"]
    if "tab" in query_params:
        active_tab = query_params["tab"][0]
    else:
        active_tab = "Login"

    if active_tab not in tabs:
        active_tab = "Login"

    non_active_tab = [x for x in tabs if x!=active_tab][0]
    display_text = {"Login": "Already have an account? Login", "Signup":"Don't have an account? Sign up"}
    
    signup_login_hyperlink = f"""
        <a class="nav-item" href="?tab={non_active_tab}" id="signuploginlink">{display_text[non_active_tab]}</a>
    """
    placeholder_hyperlink = st.empty()
    placeholder_hyperlink.markdown(signup_login_hyperlink, unsafe_allow_html=True)

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
                # st.write(login)
                # st.write(auth.get_account_info(login["idToken"]))
                # user_email = text_email
                # user_password = text_password
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


        db = firebase.database()
        # data to save
        data = {"name": "Mortimer 'Morty' Smith"}
        db.child("users").child("Morty").set(data)
        return str(login)

    if active_tab == "Login":
        if placeholder.button("Login", key="loginbtn"):
            login()
            
    elif active_tab == "Signup":
        if placeholder.button("Sign up", key="signupbutton"):
            signUp()



    # else:
    #     okay_run()




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



# widget_values = {}

# def make_recording_widget(f):
#     """Return a function that wraps a streamlit widget and records the
#     widget's values to a global dictionary.
#     """
#     def wrapper(label, *args, **kwargs):
#         widget_value = f(label, *args, **kwargs)
#         widget_values[label] = widget_value
#         return widget_value

#     return wrapper


# button = make_recording_widget(st.button)
# slider = make_recording_widget(st.slider)
# checkbox = make_recording_widget(st.checkbox)
# # ... create any other wrapped widgets you want
# another = make_recording_widget(st.empty)
# button("Recorded Button")
# slider("Recorded Slider")
# checkbox("Recorded Checkbox")

# # All current widget values will be recorded in the widget_values dict.
# # We print them here; they could also be serialized to JSON or whatever.
# st.write("Recorded values: ", widget_values)







# if 'user' not in st.session_state:
#     st.session_state['user'] = False

# successful = False
# def okay_run():
#     app = MultiApp()
#     st.markdown("""
#     # iota influence
#     """)
#     # Add all your application here
#     app.add_app("Influencers", influencer_page.app)
#     app.add_app("Posts", posts_page.app)

#     # The main app
#     app.run()

# # global user_email 
# # user_email = "initialise"
# # global user_password
# # user_password = "initialisepass"

# # def emailpass():
# #     credentials = [user_email, user_password]
# #     return credentials

# if not st.session_state.user:
#     firebaseConfig = {
#     "apiKey": "AIzaSyBHlJZLmdxtOQtM10CkOP2pNvuO81Elirg",
#     "authDomain": "iota-web-app.firebaseapp.com",
#     "databaseURL": "https://iota-web-app-default-rtdb.asia-southeast1.firebasedatabase.app",
#     "projectId": "iota-web-app",
#     "storageBucket": "iota-web-app.appspot.com",
#     "messagingSenderId": "390789359948",
#     "appId": "1:390789359948:web:c59018f57465985e6307e9",
#     "measurementId": "G-RPSDKG694K"
#     }
    
#     firebase = pyrebase.initialize_app(firebaseConfig)
#     auth = firebase.auth()


#     # email = make_recording_widget(st.empty)
#     # password = make_recording_widget(st.empty)
#     # placeholder = make_recording_widget(st.empty)
#     # placeholder_checkbox = make_recording_widget(st.empty)

#     email = st.empty()
#     password =  st.empty()
#     placeholder = st.empty() #to interchange login&signup button
#     placeholder_checkbox = st.empty()

#     text_email = email.text_input("Email")
#     text_password = password.text_input("Password", type="password")

#     query_params = st.experimental_get_query_params()
#     tabs = ["Login", "Signup"]
#     if "tab" in query_params:
#         active_tab = query_params["tab"][0]
#     else:
#         active_tab = "Login"

#     if active_tab not in tabs:
#         active_tab = "Login"

#     non_active_tab = [x for x in tabs if x!=active_tab][0]
#     display_text = {"Login": "Already have an account? Login", "Signup":"Don't have an account? Sign up"}
    
#     signup_login_hyperlink = f"""
#         <a class="nav-item" href="?tab={non_active_tab}" id="signuploginlink">{display_text[non_active_tab]}</a>
#     """
#     placeholder_hyperlink = st.empty()
#     placeholder_hyperlink.markdown(signup_login_hyperlink, unsafe_allow_html=True)

#     def signUp():
#         #create users
#         try:
#             user = auth.create_user_with_email_and_password(text_email, text_password)
#             # user_email = text_email
#             # user_password = text_password
#             st.session_state.user=user
#         except requests.HTTPError as e:
#             error_json = e.args[1]
#             error = json.loads(error_json)['error']['message']
#             if error == "EMAIL_EXISTS":
#                 st.error("Email already exists. Login instead")
#         successful=True
#         print("Success .... ")
#         email.empty()
#         password.empty()
#         placeholder.empty()
#         placeholder_checkbox.empty()
#         placeholder_hyperlink.empty()
#         okay_run()

#     def login():
#         try:
#             login = auth.sign_in_with_email_and_password(text_email, text_password)
#             # st.write(login)
#             # st.write(auth.get_account_info(login["idToken"]))
#             # user_email = text_email
#             # user_password = text_password
#             st.session_state.user=login
#         except requests.HTTPError as e:
#             error_json = e.args[1]
#             error = json.loads(error_json)['error']['message']
#             st.error(error)
#         # #send email verification
#         # auth.send_email_verification(login['idToken'])
#         # #reset the password
#         # auth.send_password_reset_email(email)
#         successful=True
#         print("Success ... ")
#         email.empty()
#         password.empty()
#         placeholder.empty()
#         placeholder_checkbox.empty()
#         placeholder_hyperlink.empty()


#         db = firebase.database()
#         # data to save
#         data = {"name": "Mortimer 'Morty' Smith"}
#         db.child("users").child("Morty").set(data)
#         okay_run()

#     if active_tab == "Login":
#         if placeholder.button("Login", key="loginbtn"):
#             login()
            
#     elif active_tab == "Signup":
#         if placeholder.button("Sign up", key="signupbutton"):
#             signUp()

# else:
#     okay_run()

# def returnstate():
#     return st.session_state.get("user")







# st.session_state.sync()







# def changeCheckboxToLogin():
#     login_checkbox = placeholder_checkbox.checkbox("Already have an account? Login", key="logincheck")
#     placeholder.button("Sign up", key="signupbutton")

# def changeCheckboxToSignUp():
#     signup_checkbox = placeholder_checkbox.checkbox("Sign up", key="signCheckBox")
#     placeholder.button("Login", key="loginbtn")


# placeholder.button("Login", key="signup2")
# if login_checkbox:
#     changeCheckboxToSignUp()
#     st.write(login_checkbox)
# else:
#     changeCheckboxToLogin()
#     st.write(signup_checkbox)




# if successful:
#     okay_run()

 
