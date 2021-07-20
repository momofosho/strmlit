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

mod = importlib.import_module('posts_page')

a = mod.app()
s = a
print(s)
def returnUsername():
    return s
