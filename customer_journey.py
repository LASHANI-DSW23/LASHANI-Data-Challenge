import plotly.graph_objects as go
import pandas as pd
import streamlit as st

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

# Streamlit
with st.container():
    st.plotly_chart(fig, use_container_width=True)
