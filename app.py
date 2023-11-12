import streamlit as st
import pandas as pd
import tensorflow as tf
import numpy as np
import pickle
import joblib
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
"Customer Insights and Predictions"
]

# Show tabs
dashtab, mltab = st.tabs([s.center(55,"\u2001") for s in listTabs])
####

with dashtab:
    st.markdown('<iframe title="Dashboard_Lashani" width="100%" height="600" src="https://app.powerbi.com/view?r=eyJrIjoiZTNjNTgxNmYtYmZkZS00M2Q1LTk2YjUtNDRiZDRhN2U4MzU0IiwidCI6IjllYzZkNzdmLTQ0ZmQtNDc3MC05YTkzLTdkYjI2OTYzZWNlOSIsImMiOjEwfQ%3D%3D" frameborder="0" allowFullScreen="true"></iframe>', unsafe_allow_html = True)

with mltab:
    # Write Header
    st.write("### Customer Forecasting")
    st.write("Enter the values for the features asked to predict the customer's cluster segmentation, churn label, and lifetime value.")

    # Caching
    if "model" not in st.session_state:
        with open('./model/churnmodel.pkl', 'rb') as model_file:
            churnmodel = pickle.load(model_file)

        with open('./model/cltvmodel.pkl', 'rb') as model_file:
            cltvmodel = pickle.load(model_file)

        with open('./model/kmeans.pkl', 'rb') as model_file:
            kmeansmodel = pickle.load(model_file)

        scaler = joblib.load('./model/scaler_model.pkl')

        st.session_state.model = {
            "churn" : churnmodel,
            "cltv" : cltvmodel,
            "kmeans" : kmeansmodel,
            "scaler" : scaler
        }

    # Optimization
    else:
        churnmodel = st.session_state.model["churn"]
        cltvmodel = st.session_state.model["cltv"]
        kmeans = st.session_state.model["kmeans"]
        scaler = st.session_state.model["scaler"]

    # Create Columns for Input Sections
    col0, col1, col2, col3, col4 = st.columns(5)  # First row of columns
    col5, col6, col7, col8, col9, col10, col11 = st.columns(7)  # Second row of columns

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
        st.write("<p style='text-align: left;'>Monthly Purchase (Thousand IDR)</h1>", unsafe_allow_html=True)
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

    with col11:
        noservice = st.checkbox("No Service")
        stspace(2)  # Add vertical space

        # Button to Trigger Prediction
        col00, col01 = st.columns(2)
        with col01:
            isPredict = st.button("Predict!")  # User clicks the "Predict!" button to make predictions

    # Generate Mapping
    mapdevice = map_end_category(device)
    mappayment = map_payment_method(payment)

    if noservice:
        games = 2
        music = 2
        education = 2
        video = 2
        myapp = 2
    
    # Predict Input when the "Predict!" button is clicked
    if isPredict:

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

        # Create a new DataFrame for Segmentation Model
        dfcluster = df[["Games Product", "Music Product", "Education Product", "Call Center", "Video Product", "Use MyApp", "Monthly Purchase (Thou. IDR)", "is_High End", "is_Low End", "is_Mid End"]]

        # Map the 'Location' column to numerical values
        df['Location'] = df['Location'].map({'Jakarta': 1, 'Bandung': 0})

        # Predict the result with previously trained model
        churnresult = churnmodel.predict(df.values[0].reshape(1, -1))[0]
        cltvresult = cltvmodel.predict(df.values[0].reshape(1, -1))[0]

        scaled_data = scaler.transform(dfcluster.values[0].reshape(1, -1))
        segmentationresult = kmeans.predict(scaled_data)[0]

        # Display the prediction results
        st.success(f"Cluster Type: Cluster {segmentationresult} ({segmentationlabel(int(segmentationresult))}), Predicted Churn: {'Positive' if churnresult == 1 else 'Negative'}, Predicted Customer Lifetime Value: {round(cltvresult, 1)} (Thousand IDR)")
        st.write(f"Recommendation for Cluster {segmentationresult} ({segmentationlabel(int(segmentationresult))}):")

        # List of recommendations for Cluster 0
        recommendations_cluster = recommendation(segmentationresult)

        # Display recommendations
        for recommendation in recommendations_cluster:
            st.write(recommendation)

    # Write Header
    st.write("### Customer Insights")

    with st.expander("Customer Segmentation Clusters"):
        segmentdf = pd.read_csv("./data/clusters.csv").set_index("Cluster")
        st.dataframe(segmentdf)
        st.write("""
        Above is the result of our customer segmentation using clusters. The segmentation result reveals four distinct customer clusters (labelled 0 to 3), each characterized by specific behavior patterns; each of them is:""")

        clusters_description = [
            "Cluster 0 **(High End, High Purchase, Moderate Product Usage)**",
            "Cluster 1 **(Low End, Low Purchase, No Service)**",
            "Cluster 2 **(Mid End, Moderate Purchase, Low Product Usage)**",
            "Cluster 3 **(Mid End, Moderate Purchase, Moderate Product Usage)**"
        ]

        for num, description in enumerate(clusters_description):
            st.write(f"{num + 1}. {description}")

        stspace(1)
        st.write("""
        Notes:\n
        - Low Monthly Purchase Level : **Less than 50.000**\n
        - Moderate Monthly Purchase Level : **More than 50.000 and less than 100.000**\n
        - High Monthly Purchase Level : **More than 100.000**
        """)

    with st.expander("Customer Journey"):
        if "custjourneyfig" not in st.session_state:
            custjourneyfig = customerjourney()
            st.session_state.custjourneyfig = custjourneyfig
        
        else:
            custjourneyfig = st.session_state.custjourneyfig

        st.plotly_chart(custjourneyfig, use_container_width=True)
        st.write("From the **Sankey diagram** above, we can see the growth of our Customer from each month. Each node or bar, represents the months that have passed, as for the height of that bar represents the amount of customers we've recruited for the months that have passed. In the end we can see that the bar is divided into two: **Month_72_Churn and Month_72_Active** to differentiate the amount of active customers and churn customers in the current quarter.")
        st.write("Our recommendation for the next Data Gathering, is that we record the customer's ID to track their journey with the company for each month. As for **the stages**: we propose **Awareness, Research, Consideration, Purchase, and Support**. So for each month, we will be able to see on what stage is the customer on.")
