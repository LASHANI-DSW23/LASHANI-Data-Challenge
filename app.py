import streamlit as st
import pandas as pd
import tensorflow as tf
import numpy as np
import pickle
from datetime import datetime
from app_func import *
from PIL import Image

# Set Layout Config
st.set_page_config(page_title="DSW - Lashani", page_icon=":chart_with_upwards_trend:",layout="wide")

# Add Font
streamlit_style = """
			<style>
			@import url('https://fonts.cdnfonts.com/css/neue-haas-grotesk-display-pro');    

			html, body, [class*="css"]  {
			font-family: 'neue haas grotesk display pro';
			}
			</style>
			"""

# Apply Font
st.markdown(streamlit_style, unsafe_allow_html=True)

# Greet
if "greet" not in st.session_state:
    greet()
    st.session_state.greet = True

# Make a Centered Text
col1, col2,  = st.columns((36, 6))

# Add Header Text
with col1:
    stspace(2)
    st.write("## Customer Dashboard")

# Add Image
with col2:
    st.image(Image.open("./img/TelkomselLogo.png"))

# Generate Tabs
listTabs = [
"Dashboard",
"Churn & CLTV Forecasting"
]

# Show tabs
dashtab, mltab = st.tabs([s.center(55,"\u2001") for s in listTabs])

with dashtab:
    pass

with mltab:
    # Write Header
    st.write("### Input Customer Data")

    # Caching
    if "churnmodel" not in st.session_state:
        with open('./model/churnmodel.pkl', 'rb') as model_file:
            churnmodel = pickle.load(model_file)

        with open('./model/cltvmodel.pkl', 'rb') as model_file:
            cltvmodel = pickle.load(model_file)

        st.session_state.model = {
            "churn" : churnmodel,
            "cltv" : cltvmodel
        }

    # Optimization
    else:
        churnmodel = st.session_state.model["churn"]
        cltvmodel = st.session_state.model["cltv"]

    # Create Columns for Input Sections
    col0, col1, col2, col3, col4 = st.columns(5)  # First row of columns
    col5, col6, col7, col8, col9, col10 = st.columns(6)  # Second row of columns

    # User Inputs for the First Row of Columns
    with col0:
        st.markdown("<p style='text-align: left;'>Tenure Months</h1>", unsafe_allow_html=True)
        months = st.number_input("", step=1)  # User inputs tenure months

    with col1:
        st.markdown("<p style='text-align: left;'>Location</h1>", unsafe_allow_html=True)
        location = st.selectbox(
            '',
            ('Jakarta', 'Bandung'))  # User selects location (Jakarta or Bandung)

    with col2:
        st.markdown("<p style='text-align: left;'>Device</h1>", unsafe_allow_html=True)
        device = st.selectbox(
            '',
            ('Low End', 'Mid End', 'High End'))  # User selects device category

    with col3:
        st.markdown("<p style='text-align: left;'>Payment</h1>", unsafe_allow_html=True)
        payment = st.selectbox(
            '',
            ('Credit', 'Debit', 'Digital Wallet', 'Pulsa'))  # User selects payment method

    with col4:
        st.write("<p style='text-align: left;'>Monthly Purchase</h1>", unsafe_allow_html=True)
        monthly = st.number_input(" ", step=1)  # User inputs monthly purchase amount

    # User Inputs for the Second Row of Columns
    with col5:
        games = st.checkbox("Games Product")  # User checks the Games option

    with col6:
        music = st.checkbox("Music Product")  # User checks the Music option

    with col7:
        education = st.checkbox("Education Product")  # User checks the Education option

    with col8:
        callcenter = st.checkbox("Call Center")  # User checks the Call Center option

    with col9:
        video = st.checkbox("Video Product")  # User checks the Video option

    with col10:
        myapp = st.checkbox("MyApp")  # User checks the MyApp option
        stspace(2)  # Add vertical space

        # Button to Trigger Prediction
        col00, col01 = st.columns(2)
        with col01:
            isPredict = st.button("Predict!")  # User clicks the "Predict!" button to make predictions

    # Generate Mapping
    mapdevice = map_end_category(device)
    mappayment = map_payment_method(payment)

    # Create a new DataFrame with user inputs
    df = pd.DataFrame({
        'Tenure Months': [months],
        'Location': [location],
        'Games Product': [int(games)],
        'Music Product': [int(music)],
        'Education Product': [int(education)],
        'Call Center': [int(callcenter)],
        'Video Product': [int(video)],
        'Use MyApp': [int(myapp)],
        'Monthly Purchase (Thou. IDR)': [monthly],
        'is_High End': [mapdevice["high"]],
        'is_Low End': [mapdevice["low"]],
        'is_Mid End': [mapdevice["mid"]],
        'use_Credit': [mappayment["Credit"]],
        'use_Debit': [mappayment["Debit"]],
        'use_Digital Wallet': [mappayment["Digital Wallet"]],
        'use_Pulsa': [mappayment["Pulsa"]]
    })

    # Map the 'Location' column to numerical values
    df['Location'] = df['Location'].map({'Jakarta': 1, 'Bandung': 0})

    # Predict Input when the "Predict!" button is clicked
    if isPredict:

        # Predict the result with previously trained model
        churnresult = churnmodel.predict(df.values[0].reshape(1, -1))[0]
        cltvresult = cltvmodel.predict(df.values[0].reshape(1, -1))[0]
        
        # Display the prediction results
        st.success(f"Predicted Churn: {'Positive' if churnresult == 1 else 'Negative'}, Predicted Customer Lifetime Value: {round(cltvresult, 1)} (Thousand IDR)")
