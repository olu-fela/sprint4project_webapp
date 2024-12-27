import streamlit as st
import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns
import plotly.express as px

# Set the page configuration
st.set_page_config(page_title="Data Visualization App", layout="wide")

# Header
st.header("Interactive Data Analysis and Visualization App")

# Markdown
st.markdown("""
This app is my very first attempt at deploying a Web App on Exploratory Data Anaylisis performed for Car Advertisement Dataset!
* **Python libraries:** streamlit, pandas, plotly express, numpy, matplotlib, seaborn
""")

# File uploader
uploaded_file = st.file_uploader("Upload your dataset (CSV format)", type=["csv"])
if uploaded_file:
    # Load the dataset
    df = pd.read_csv(uploaded_file)
    st.write("### Dataset Preview")
    st.write(df.head())

    # Sidebar for data cleaning options
    st.sidebar.header("Data Cleaning Options")
    if st.sidebar.checkbox("Show missing values summary"):
        st.write("### Missing Values Summary")
        st.write(df.isnull().sum())

    # Allow user to choose to drop or fill missing values
    missing_option = st.sidebar.radio(
        "How would you like to handle missing values?",
        ("Drop rows with missing values", "Fill missing values with a specific value")
    )

    if missing_option == "Drop rows with missing values":
        df_cleaned = df.dropna()
        st.sidebar.write("Rows with missing values dropped.")
    else:
        fill_value = st.sidebar.number_input("Enter value to fill missing data", value=0)
        df_cleaned = df.fillna(fill_value)
        st.sidebar.write(f"Missing values filled with: {fill_value}")

    st.write("### Cleaned Dataset Preview")
    st.write(df_cleaned.head())

    # Sidebar filtering
    st.sidebar.header("Filter Options")
    numeric_columns = df_cleaned.select_dtypes(include=["float64", "int64"]).columns
    categorical_columns = df_cleaned.select_dtypes(include=["object", "category"]).columns

    filter_column = st.sidebar.selectbox("Select a column to filter", categorical_columns)
    filter_value = st.sidebar.text_input(f"Enter value to filter by {filter_column}")

    if filter_value:
        df_filtered = df_cleaned[df_cleaned[filter_column] == filter_value]
        st.write(f"### Filtered Dataset by {filter_column} = {filter_value}")
        st.write(df_filtered.head())
    else:
        df_filtered = df_cleaned

    # Plotly Express histogram
    st.write("### Histogram")
    if numeric_columns.any():
        hist_column = st.selectbox("Select a numeric column for the histogram", numeric_columns)
        hist_chart = px.histogram(df_filtered, x=hist_column, nbins=20, title=f"Histogram of {hist_column}")
        st.plotly_chart(hist_chart)

    # Plotly Express scatter plot
    st.write("### Scatter Plot")
    if len(numeric_columns) > 1:
        x_axis = st.selectbox("Select X-axis for scatter plot", numeric_columns, key="scatter_x")
        y_axis = st.selectbox("Select Y-axis for scatter plot", numeric_columns, key="scatter_y")
        scatter_chart = px.scatter(df_filtered, x=x_axis, y=y_axis, title=f"Scatter Plot: {x_axis} vs {y_axis}")
        st.plotly_chart(scatter_chart)

    # Checkbox to show additional plots
    st.write("### Additional Visualizations")
    if st.checkbox("Show bar plot"):
        if categorical_columns.any():
            bar_column = st.selectbox("Select a categorical column for the bar plot", categorical_columns)
            bar_chart = px.bar(df_filtered, x=bar_column, title=f"Bar Plot of {bar_column}")
            st.plotly_chart(bar_chart)

    if st.checkbox("Show box plot"):
        if numeric_columns.any():
            box_column = st.selectbox("Select a numeric column for the box plot", numeric_columns)
            box_chart = px.box(df_filtered, y=box_column, title=f"Box Plot of {box_column}")
            st.plotly_chart(box_chart)

    if st.checkbox("Show scatter matrix"):
        scatter_matrix_chart = px.scatter_matrix(df_filtered, dimensions=numeric_columns[:4], title="Scatter Matrix")
        st.plotly_chart(scatter_matrix_chart)

else:
    st.info("Please upload a CSV file to proceed.")
