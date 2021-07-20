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


import importlib

mod = importlib.import_module('temp')


a = mod.returnUsername()
st.write(a) #result that it returns




# st.title('Home')

# st.write('This is the `home page` of this multi-page app.')

# st.write('In this app, we will be building a simple classification model using the Iris dataset.')
# hashtag_filter = st.sidebar.multiselect(
# 'Select hashtag',
# options=['1','3'])
