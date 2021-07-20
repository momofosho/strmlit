from logging import PlaceHolder
from altair.vegalite.v4.schema.core import DataFormat
from numpy.core.numeric import NaN
from numpy.lib.function_base import place
import streamlit as st
from google.cloud import firestore
import json
import pandas as pd
import itertools
import numpy as np
import time


app_state = st.experimental_get_query_params()
default_title = app_state["username"] if "username" in app_state else ""
title = st.text_input('Influencer Username', value = default_title)
app_state["username"] = title

st.write(st.experimental_get_query_params())



# import importlib

# mod = importlib.import_module('temp')


# a = mod.returnUsername()
# st.write(a) #result that it returns

# time.sleep(15)
# # PATH_TO_MY_FILE = './file.txt'
# # f = open(PATH_TO_MY_FILE,"r")
# # st.write(f.read())
# # f.close()

# def read_file():
#     print("Now reading the file..")
#     try:
#         f = open("./file.txt", "r")
#         for line in f.readlines():
#             st.write(line)
#         f.close()
#     except Exception:
#         st.write("Could not read to file")

# read_file()




# st.title('Home')

# st.write('This is the `home page` of this multi-page app.')

# st.write('In this app, we will be building a simple classification model using the Iris dataset.')
# hashtag_filter = st.sidebar.multiselect(
# 'Select hashtag',
# options=['1','3'])
