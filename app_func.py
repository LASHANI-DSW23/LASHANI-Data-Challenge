import streamlit as st
import pandas as pd
import tensorflow as tf
import numpy as np
import pickle
import time
import plotly.graph_objects as go
from datetime import datetime

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
        return "High-End, High Purchase, Moderate Product Usage"
    elif x == 1:
        return "Low-End, Low Purchase, No Service"
    elif x == 2:
        return "Mid-End, Moderate Purchase, Low Product Usage"
    elif x == 3:
        return "Mid-End, Moderate Purchase, Moderate Product Usage"
    else:
        return "Unknown"

def customerjourney():
    # Assuming telco_df is your DataFrame with customer data
    # You can load your data as follows
    telco_df = pd.read_csv("https://raw.githubusercontent.com/MirantyAnjaniPutri/LASHANI-Data-Challenge/main/data/data.csv")

    # Assuming 72 months
    num_months = 71  # Updated to 71, as it starts from month_1 to month_71

    # Create nodes for Sankey diagram
    nodes = [f"month_{i}" for i in range(1, num_months + 1)] + ['month_72_churn', 'month_72_active']

    # Create links for Sankey diagram
    links = []
    for i in range(num_months - 1):
        month_condition = telco_df['Tenure Months'] >= (72 - i)
        churn_count = telco_df[month_condition & (telco_df['Churn Label'] == 'Yes')].shape[0]
        active_count = telco_df[month_condition & (telco_df['Churn Label'] == 'No')].shape[0]

        links.append({'source': i, 'target': i + 1, 'value': month_condition.sum()})

    # Add links for month 71 to churn and active nodes
    links.append({'source': num_months - 1, 'target': num_months, 'value': churn_count})
    links.append({'source': num_months - 1, 'target': num_months + 1, 'value': active_count})

    # Create Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=10,
            thickness=20,
            line=dict(color='black', width=0.5),
            label=nodes,
            color="rgba(255, 60, 50, 0.5)"  # Set the color for nodes
        ),
        link=dict(
            source=[link['source'] for link in links],
            target=[link['target'] for link in links],
            value=[link['value'] for link in links],
            color="gray"  # Set the color for links
        )
    )])

    # Update layout
    fig.update_layout(
        title_text="Customer Journey - 72 Months",
        title=dict(
            x=0.45,  # Center the title
            font = dict(
                size=20
            )
        ),
        font_size=10,
        hovermode='x',
        hoverlabel=dict(bgcolor="white", font_size=16),
        margin=dict(l=0, r=0, b=0, t=40)
    )

    return fig

def recommendation(x):
    texts = {
        0 : [
                """
                1. Engagement Campaigns:
                   - Develop targeted re-engagement campaigns, especially through the Video product and MyApp.
                   - Offer exclusive content, features, or discounts to encourage increased usage.
                2. Personalization:
                   - Leverage data to personalize recommendations and content within the games, music, and video products.
                   - Tailor promotions based on their historical preferences and usage patterns.
                3. Customer Feedback and Improvement:
                   - Proactively seek feedback from Cluster 0 customers to understand their dissatisfaction.
                   - Address and communicate improvements in response to their concerns.
                """
            ],
        
        1 : [
            """
                1. Service Restoration:
                   - Investigate and address the issues causing 'No Service' across all products promptly.
                   - Clearly communicate the steps taken to improve service reliability and quality.
                2. Re-Introduction Campaigns:
                   - Develop targeted campaigns to re-introduce the value of each product.
            """
            ],
        
        2 : [
                """
                1. Increase Product Engagement:
                   - Launch targeted marketing campaigns to promote key product features.
                   - Provide incentives or rewards for increased product usage.
                2. Personalized Loyalty Programs:
                   - Develop loyalty programs to reward consistent engagement.
                   - Provide personalized recommendations to enhance their experience.
                   - Implement proactive customer support to address any concerns promptly.
                """
            ],

        3 : [
                """
                1. Increase Product Engagement:
                   - Launch targeted marketing campaigns to promote key product features.
                   - Provide incentives or rewards for increased product usage.",
                2. Personalized Loyalty Programs:
                   - Develop loyalty programs to reward consistent engagement.
                   - Provide personalized recommendations to enhance their experience.
                   - Implement proactive customer support to address any concerns promptly.
                """
            ]

    }

    return texts[x]