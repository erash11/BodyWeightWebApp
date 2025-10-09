import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(page_title="Body Weight Trends", layout="wide")

# Load the dataset
@st.cache_data
def load_data():
    # Use relative path for deployment (place CSV in same directory as app)
    file_path = "BodyWeightMaster.csv"
    data = pd.read_csv(file_path)
    
    # Convert the DATE column to datetime format
    data['DATE'] = pd.to_datetime(data['DATE'])
    
    # Extract date from the DATE column
    data['Date'] = data['DATE'].dt.date
    
    # Add YearMonth column
    data['YearMonth'] = data['DATE'].dt.to_period('M')
    
    return data

# Load data
data = load_data()

# Title
st.title("Body Weight Trends Over Time")

# Mode selection
mode = st.radio("Select Mode:", options=["Individual", "Position"], horizontal=True)

# Dynamic dropdown based on mode
if mode == "Individual":
    names = sorted(data['NAME'].astype(str).unique())
    selected_value = st.selectbox(
        "Select Individual:",
        options=["All Individuals"] + names,
        index=0
    )
else:
    positions = sorted(data['POS'].astype(str).unique())
    selected_value = st.selectbox(
        "Select Position:",
        options=["All Positions"] + positions,
        index=0
    )

# Filter data based on selection
if mode == "Individual":
    if selected_value == "All Individuals":
        ind_data = data.copy()
    else:
        ind_data = data[data['NAME'] == selected_value]
else:
    if selected_value == "All Positions":
        ind_data = data.copy()
    else:
        ind_data = data[data['POS'] == selected_value]

# Calculate average weight for each day
avg_weight_by_day = ind_data.groupby(['Date'])['WEIGHT'].mean().reset_index()

# Calculate average weight for each month
avg_weight_by_month = ind_data.groupby(['YearMonth'])['WEIGHT'].mean().reset_index()

# Convert YearMonth back to datetime for plotting
avg_weight_by_month['YearMonth'] = avg_weight_by_month['YearMonth'].dt.to_timestamp()

# Create the figure
fig = go.Figure()

# Plot the average weight for each day with breaks at the end of each month
for i, month in enumerate(avg_weight_by_month['YearMonth']):
    if i < len(avg_weight_by_month['YearMonth']) - 1:
        mask = (pd.to_datetime(avg_weight_by_day['Date']) >= month) & (pd.to_datetime(avg_weight_by_day['Date']) < avg_weight_by_month['YearMonth'].iloc[i + 1])
    else:
        mask = pd.to_datetime(avg_weight_by_day['Date']) >= month
    
    monthly_data = avg_weight_by_day.loc[mask]
    fig.add_trace(go.Scatter(
        x=monthly_data['Date'], 
        y=monthly_data['WEIGHT'],
        mode='lines+markers', 
        name='Daily Avg Weight', 
        line=dict(color='rgba(0,128,128,0.15)'), 
        showlegend=False
    ))

# Plot the average weight for each month as separate segments with data labels
for date, weight in zip(avg_weight_by_month['YearMonth'], avg_weight_by_month['WEIGHT']):
    fig.add_trace(go.Scatter(
        x=[date, date + pd.DateOffset(days=30)], 
        y=[weight, weight],
        mode='lines+text', 
        line=dict(color='navy', width=2), 
        name='Monthly Avg Weight',
        text=[None, f'{weight:.1f}'],
        textposition='top center',
        textfont=dict(color='darkred', family='Arial', size=12)
    ))

# Update the layout
title = f'Body Weight per Month for {selected_value}'

fig.update_layout(
    title=title,
    xaxis_title='Date',
    yaxis_title='Weight (lbs)',
    xaxis=dict(
        tickmode='array',
        tickvals=avg_weight_by_month['YearMonth'],
        ticktext=avg_weight_by_month['YearMonth'].dt.strftime('%b %y'),
        tickangle=-45
    ),
    legend_title_text='',
    legend=dict(
        x=0.01,
        y=0.99,
        traceorder='normal',
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(0,0,0,0)'
    ),
    showlegend=False,
    height=600
)

# Display the plot
st.plotly_chart(fig, use_container_width=True)
