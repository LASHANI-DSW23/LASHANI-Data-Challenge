import streamlit as st
import pandas as pd
import tensorflow as tf
import numpy as np
import pickle
from datetime import datetime
import time

def greet():
    st.toast('Hello!', icon='✅')
    time.sleep(1)
    st.toast('Welcome to the Customer Dashboard', icon='✅')

def stspace(num):
    for j in range(num):
        st.write("")

def map_end_category(category):
    if category == "High End":
        return {"high": 1, "mid": 0, "low": 0}
    elif category == "Mid End":
        return {"high": 0, "mid": 1, "low": 0}
    else:
        return {"high": 0, "mid": 0, "low": 1}
    
def map_payment_method(method):
    if method == 'Credit':
        return {'Credit': 1, 'Debit': 0, 'Digital Wallet': 0, 'Pulsa': 0}
    elif method == 'Debit':
        return {'Credit': 0, 'Debit': 1, 'Digital Wallet': 0, 'Pulsa': 0}
    elif method == 'Digital Wallet':
        return {'Credit': 0, 'Debit': 0, 'Digital Wallet': 1, 'Pulsa': 0}
    elif method == 'Pulsa':
        return {'Credit': 0, 'Debit': 0, 'Digital Wallet': 0, 'Pulsa': 1}

def segmentationlabel(x):
    if x == 0:
        return "High-End, Moderate"
    elif x == 1:
        return "Low-End, No Service"
    elif x == 2:
        return "Mid-End, Low"
    elif x == 3:
        return "Mid-End, Moderate"
    else:
        return "Unknown"

