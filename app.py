import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px


# Set the page title
st.set_page_config(page_title="Streamlit and Plotly App", layout="wide")

st.markdown("""
This app is my very first attempt at deploying a Web App on Exploratory Data Anaylisis performed for Car Advertisement Dataset!
* **Python libraries:** streamlit, pandas, plotly express, numpy, matplotlib, seaborn
""")

# Header
st.header("Interactive Data Visualization with Streamlit and Plotly")

# Sidebar
#st.sidebar.header('User Input Features')

# Upload dataset or read from a local CSV
uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])
if uploaded_file is not None:
    # Load the dataset
    df = pd.read_csv(uploaded_file)
    st.write("Dataset Preview:")
    st.write(df.head())

    # Histogram
    st.subheader("Histogram")
    numeric_columns = df.select_dtypes(include=['float64', 'int64', 'int32']).columns
    if len(numeric_columns) > 0:
        x_axis = st.selectbox("Select the X-axis for the histogram:", numeric_columns, key="histogram")
        histogram = px.histogram(df, x=x_axis, nbins=20, title=f"Histogram of {x_axis}")
        st.plotly_chart(histogram, use_container_width=True)
    else:
        st.warning("No numeric columns available for the histogram.")

    # Scatter plot
    st.subheader("Scatter Plot")
    if len(numeric_columns) > 1:
        x_axis = st.selectbox("Select the X-axis for the scatter plot:", numeric_columns, key="scatter_x")
        y_axis = st.selectbox("Select the Y-axis for the scatter plot:", numeric_columns, key="scatter_y")
        scatter = px.scatter(df, x=x_axis, y=y_axis, title=f"Scatter Plot: {x_axis} vs {y_axis}")
        st.plotly_chart(scatter, use_container_width=True)
    else:
        st.warning("Not enough numeric columns available for the scatter plot.")

    # Checkbox to filter data
    st.subheader("Filter Data")
    checkbox = st.checkbox("Show only rows where column 'days_listed' > 30 (if available)")
    if checkbox and 'days_listed' in df.columns:
        filtered_df = df[df['days_listed'] > 30]
        st.write(f"Filtered Dataset (rows where 'days_listed' > 30):")
        st.write(filtered_df)
    else:
        st.write("No filter applied, showing the full dataset.")
else:
    st.info("Please upload a CSV file to proceed.")
