import streamlit as st
from multiapp import MultiApp
#from apps import home, data, model # import your app modules here
import influencer_page, posts_page

app = MultiApp()

st.markdown("""
# iota influence
""")

# Add all your application here
app.add_app("Influencers", influencer_page.app)
app.add_app("Posts", posts_page.app)

# The main app
app.run()
 
