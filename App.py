import streamlit as st
import pandas as pd
import plotly.express as px

# Load the cleaned dataset
df = pd.read_csv("C:\\Users\\mahdi\\OneDrive\\Desktop\\5DATA005C.1_20024657_w2002465_Mahdi_Ishak\\orders_cleaned.csv")

# Convert "Order Date" to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Sidebar for filtering
st.sidebar.title('Filter Data')
selectedcategory = st.sidebar.selectbox("Select Category", ['All'] + list(df["Category"].unique()))
selectedsegment = st.sidebar.selectbox("Select Segment", ['All'] + list(df["Segment"].unique()))
selectedcountry = st.sidebar.selectbox("Select Country", ['All'] + list(df["Country"].unique()))

# Filter the data based on the selections
filtered_data = df.copy()
if selectedcategory != 'All':
    filtered_data = filtered_data[filtered_data["Category"] == selectedcategory]
if selectedsegment != 'All':
    filtered_data = filtered_data[filtered_data["Segment"] == selectedsegment]
if selectedcountry != 'All':
    filtered_data = filtered_data[filtered_data["Country"] == selectedcountry]

# Organize the visualizations
st.title('Sales and Profit Analysis')

# Visualization 01 & 02- Sum of sales and profit
selected_year = st.selectbox("Select Year", ['All'] + list(df["Order Date"].dt.year.unique()))

# setting up filter so you could see sales and profit for each year
if selected_year != 'All':
    filtered_df = df[df["Order Date"].dt.year == selected_year]
else:
    filtered_df = df

total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
col1, col2 = st.columns(2)

with col1:
    st.subheader('Total Sales')
    st.metric(label="Sales", value=f"${total_sales:,.0f}", delta=None)

with col2:
    st.subheader('Total Profit')
    st.metric(label="Profit", value=f"${total_profit:,.0f}", delta=None)

# Sales vs. Discount Scatter Plot
st.header('Sales vs. Discount Analysis')
fig = px.scatter(filtered_data, x='Discount', y='Sales', color='Category', title=f'Sales vs. Discount for {selectedcategory}',
                 labels={'Discount': 'Discount (%)', 'Sales': 'Sales ($)'},
                 template='plotly_dark')  # Change the template for a dark theme
st.plotly_chart(fig)

# Total Sales by Category (Pie Chart)
st.header('Total Sales by Category')
TotalSalesCategory = filtered_data.groupby('Category')['Sales'].sum().reset_index()
fig = px.pie(TotalSalesCategory, values='Sales', names='Category', title='Total Sales by Category')
st.plotly_chart(fig)

# Top 5 Products by Sales
st.header('Top 5 Products by Sales')
Topproducts = filtered_data.groupby('Product ID')['Sales'].sum().nlargest(5).reset_index()
fig = px.bar(Topproducts, x='Product ID', y='Sales', title='Top 5 Products by Sales',
             labels={'Product ID': 'Product ID', 'Sales': 'Total Sales ($)'},
             color='Product ID',  # Change to color by Product ID for differentiation
             color_continuous_scale='Blues')  # Change the color scale
st.plotly_chart(fig)

# Sales Trends Over Time (Line Chart)
st.header('Sales Trends Over Time')
filtered_data['Order Date'] = pd.to_datetime(filtered_data['Order Date'])
SalesTrends = filtered_data.groupby(filtered_data['Order Date'].dt.to_period("M"))['Sales'].sum().reset_index()
SalesTrends['Order Date'] = SalesTrends['Order Date'].astype(str)  # Convert period index to string
fig = px.line(SalesTrends, x='Order Date', y='Sales', title='Sales Trends Over Time',
              labels={'Order Date': 'Date', 'Sales': 'Total Sales ($)'},
              template='plotly_dark')  # Change the template for a dark theme
st.plotly_chart(fig)

# Profit by Market and Segment (Bar Chart)
st.header('Profit by Market and Segment')
ProfitMarketSegment = filtered_data.groupby(['Market', 'Segment'])['Profit'].sum().reset_index()
fig = px.bar(ProfitMarketSegment, x='Market', y='Profit', color='Segment', title='Profit by Market and Segment',
             labels={'Profit': 'Total Profit ($)'},
             barmode='group', template='plotly_dark')  # Change the template for a dark theme
st.plotly_chart(fig)



































