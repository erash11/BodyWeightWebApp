import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import hashlib

# Set page configuration
st.set_page_config(page_title="Body Weight Trends", layout="wide")

# Password Protection
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        # Simple password check
        # Change "your_password_here" to your desired password
        if st.session_state["password"] == "Bears2025":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    # First run, show input for password
    if "password_correct" not in st.session_state:
        st.text_input(
            "🔐 Enter Password", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        st.info("Please enter the password to access the dashboard.")
        return False
    # Password incorrect, show input + error
    elif not st.session_state["password_correct"]:
        st.text_input(
            "🔐 Enter Password", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        st.error("😕 Password incorrect")
        return False
    # Password correct
    else:
        return True

# Check password before showing the app
if not check_password():
    st.stop()  # Do not continue if check_password is not True

# Add logout button in sidebar
with st.sidebar:
    if st.button("🚪 Logout"):
        st.session_state["password_correct"] = False
        st.rerun()

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
    
    # Add Year column
    data['Year'] = data['DATE'].dt.year
    
    # Add YearMonth column
    data['YearMonth'] = data['DATE'].dt.to_period('M')
    
    return data

# Load data
data = load_data()

# Title with last updated indicator
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Body Weight Trends Over Time")
with col2:
    # Show when data was last loaded
    import datetime
    st.caption(f"🕐 Data loaded: {datetime.datetime.now().strftime('%I:%M %p')}")
    
# Get the most recent entry date from the dataset
most_recent_entry = data['DATE'].max()
st.info(f"📊 Latest data entry: {most_recent_entry.strftime('%B %d, %Y')} | Total records: {len(data)}")

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

# Year selector
st.markdown("### 📆 Select Year(s)")
available_years = sorted(data['Year'].unique())
selected_years = st.multiselect(
    "Filter by Year:",
    options=available_years,
    default=available_years,
    help="Select one or more years to filter the data"
)

# Date range slider
st.markdown("### 📅 Select Date Range")
min_date = data['Date'].min()
max_date = data['Date'].max()

# Create two columns for date range
col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input(
        "Start Date",
        value=min_date,
        min_value=min_date,
        max_value=max_date,
        key="start_date"
    )

with col2:
    end_date = st.date_input(
        "End Date",
        value=max_date,
        min_value=min_date,
        max_value=max_date,
        key="end_date"
    )

# Add a slider for quick range selection
date_range = st.slider(
    "Or use slider to select date range:",
    min_value=min_date,
    max_value=max_date,
    value=(start_date, end_date),
    format="MM/DD/YY",
    key="date_slider"
)

# Use slider values if they differ from date inputs
if date_range != (start_date, end_date):
    start_date, end_date = date_range

# Validate date range
if start_date > end_date:
    st.error("⚠️ Error: End date must be after start date")
    st.stop()

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

# Apply year filter
if selected_years:
    ind_data = ind_data[ind_data['Year'].isin(selected_years)]

# Apply date range filter
ind_data = ind_data[(ind_data['Date'] >= start_date) & (ind_data['Date'] <= end_date)]

# Check if filtered data is empty
if len(ind_data) == 0:
    st.warning("⚠️ No data available for the selected filters. Please adjust your selection.")
    st.stop()

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
        line=dict(color='rgba(0,128,128,0.6)'), 
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
        textfont=dict(color='darkred', family='Arial', size=12, weight='bold')
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

# Add spacing
st.markdown("---")

# Data Table Section
st.subheader("📋 Data Table")

# Create tabs for different views
tab1, tab2, tab3 = st.tabs(["Daily Data", "Monthly Averages", "Raw Data"])

with tab1:
    st.markdown("**Daily Average Weight**")
    
    # Format the daily data for display
    daily_display = avg_weight_by_day.copy()
    daily_display['Date'] = pd.to_datetime(daily_display['Date'])
    daily_display = daily_display.sort_values('Date', ascending=False)
    daily_display['WEIGHT'] = daily_display['WEIGHT'].round(1)
    daily_display.columns = ['Date', 'Average Weight (lbs)']
    
    # Display the dataframe
    st.dataframe(daily_display, use_container_width=True, hide_index=True)
    
    # Export button for daily data
    csv_daily = daily_display.to_csv(index=False)
    st.download_button(
        label="📥 Download Daily Data as CSV",
        data=csv_daily,
        file_name=f"daily_weight_data_{selected_value.replace(' ', '_')}.csv",
        mime="text/csv",
        key="download_daily"
    )

with tab2:
    st.markdown("**Monthly Average Weight**")
    
    # Format the monthly data for display
    monthly_display = avg_weight_by_month.copy()
    monthly_display['YearMonth'] = monthly_display['YearMonth'].dt.strftime('%B %Y')
    monthly_display['WEIGHT'] = monthly_display['WEIGHT'].round(1)
    monthly_display = monthly_display.sort_values('YearMonth', ascending=False)
    monthly_display.columns = ['Month', 'Average Weight (lbs)']
    
    # Display the dataframe
    st.dataframe(monthly_display, use_container_width=True, hide_index=True)
    
    # Export button for monthly data
    csv_monthly = monthly_display.to_csv(index=False)
    st.download_button(
        label="📥 Download Monthly Data as CSV",
        data=csv_monthly,
        file_name=f"monthly_weight_data_{selected_value.replace(' ', '_')}.csv",
        mime="text/csv",
        key="download_monthly"
    )

with tab3:
    st.markdown("**All Raw Data (Filtered)**")
    
    # Format the raw filtered data for display
    raw_display = ind_data[['DATE', 'NAME', 'POS', 'WEIGHT']].copy()
    raw_display = raw_display.sort_values('DATE', ascending=False)
    raw_display['DATE'] = raw_display['DATE'].dt.strftime('%Y-%m-%d')
    raw_display['WEIGHT'] = raw_display['WEIGHT'].round(1)
    raw_display.columns = ['Date', 'Name', 'Position', 'Weight (lbs)']
    
    # Display the dataframe
    st.dataframe(raw_display, use_container_width=True, hide_index=True)
    
    # Export button for raw data
    csv_raw = raw_display.to_csv(index=False)
    st.download_button(
        label="📥 Download Raw Data as CSV",
        data=csv_raw,
        file_name=f"raw_weight_data_{selected_value.replace(' ', '_')}.csv",
        mime="text/csv",
        key="download_raw"
    )

# Summary statistics
st.markdown("---")
st.subheader("📊 Summary Statistics")

# Display date range info
st.caption(f"Showing data from {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Records", len(ind_data))

with col2:
    avg_weight = ind_data['WEIGHT'].mean()
    st.metric("Average Weight", f"{avg_weight:.1f} lbs")

with col3:
    min_weight = ind_data['WEIGHT'].min()
    st.metric("Minimum Weight", f"{min_weight:.1f} lbs")

with col4:
    max_weight = ind_data['WEIGHT'].max()
    st.metric("Maximum Weight", f"{max_weight:.1f} lbs")
