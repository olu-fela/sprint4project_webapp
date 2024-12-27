import streamlit as st
import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Data Visualization App", layout="wide")

# Header and Introduction
st.header("Interactive Data Visualization and Analysis App")
st.markdown("""This app is my very first attempt at deploying a Web App on Exploratory Data Anaylisis performed for Car Advertisement Dataset! 
This app allows you to:
- Upload a dataset (CSV format).
- Clean the dataset by handling missing values.
- Filter data using an interactive sidebar.
- Visualize the data with multiple charts including histograms, scatter plots, box plots, heatmaps, and more.
""")

# File uploader
uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

if uploaded_file:
    # Load dataset
    df = pd.read_csv(uploaded_file)
    st.write("### Dataset Preview")
    st.write(df.head())

    # Sidebar menu for visualizations
    st.sidebar.header("Visualization Menu")
    chart_selection = st.sidebar.selectbox(
        "Select a chart to display:",
        ["Histogram", "Scatter Plot", "Scatterplot Matrix", "Heatmap", "Distplot", "Bar Chart", "Boxplot"]
    )

    # Handle missing values
    st.sidebar.header("Data Cleaning")
    
    if st.sidebar.checkbox("Show Missing Values Summary"):
        missing_summary = df.isnull().sum()
        st.write("### Missing Values Summary")
        st.write(missing_summary)

    missing_columns = [col for col in df.columns if df[col].isnull().sum() > 0]
    if missing_columns:
        st.sidebar.markdown("### Handle Missing Values")
        drop_cols = st.sidebar.multiselect("Select columns to drop", missing_columns)
        fill_cols = st.sidebar.multiselect("Select columns to fill", missing_columns)
        fill_value = st.sidebar.number_input("Value to fill missing data", value=0)

        df_cleaned = df.copy()
        if drop_cols:
            df_cleaned = df_cleaned.drop(columns=drop_cols)
            st.sidebar.write(f"Dropped columns: {drop_cols}")
        if fill_cols:
            df_cleaned[fill_cols] = df_cleaned[fill_cols].fillna(fill_value)
            st.sidebar.write(f"Filled missing values in columns: {fill_cols} with {fill_value}")
    else:
        df_cleaned = df

    st.write("### Cleaned Dataset Preview")
    st.write(df_cleaned.head())

    

    numeric_columns = df_cleaned.select_dtypes(include=["float64", "int64"]).columns.tolist()
    categorical_columns = df_cleaned.select_dtypes(include=["object", "category"]).columns.tolist()

    if chart_selection == "Histogram":
        st.write("### Histogram")
        column = st.selectbox("Select a column for the histogram", numeric_columns)
        hist_chart = px.histogram(df_cleaned, x=column, nbins=20, title=f"Histogram of {column}")
        st.plotly_chart(hist_chart)

    elif chart_selection == "Scatter Plot":
        st.write("### Scatter Plot")
        x_axis = st.selectbox("Select X-axis", numeric_columns, key="scatter_x")
        y_axis = st.selectbox("Select Y-axis", numeric_columns, key="scatter_y")
        scatter_chart = px.scatter(df_cleaned, x=x_axis, y=y_axis, title=f"Scatter Plot: {x_axis} vs {y_axis}")
        st.plotly_chart(scatter_chart)

    elif chart_selection == "Scatterplot Matrix":
        st.write("### Scatterplot Matrix")
        scatter_matrix_chart = px.scatter_matrix(df_cleaned, dimensions=numeric_columns[:4], title="Scatterplot Matrix")
        st.plotly_chart(scatter_matrix_chart)

    elif chart_selection == "Heatmap":
        st.write("### Heatmap")
        if len(numeric_columns) > 1:
            corr_matrix = df_cleaned[numeric_columns].corr()
            heatmap_fig = px.imshow(corr_matrix, text_auto=True, title="Correlation Heatmap")
            st.plotly_chart(heatmap_fig)

    elif chart_selection == "Distplot":
        st.write("### Distribution Plot")
        x_axis = st.selectbox("Select X-axis", numeric_columns, key="dist_x")
        y_axis = st.selectbox("Select Y-axis (Optional)", numeric_columns + [None], key="dist_y")
        dist_chart = px.histogram(
            df_cleaned, x=x_axis, y=y_axis, marginal="violin", title=f"Distribution of {x_axis}"
        )
        st.plotly_chart(dist_chart)

    elif chart_selection == "Bar Chart":
        st.write("### Bar Chart")
        x_axis = st.selectbox("Select X-axis", categorical_columns + numeric_columns, key="bar_x")
        y_axis = st.selectbox("Select Y-axis", numeric_columns, key="bar_y")
        bar_chart = px.bar(df_cleaned, x=x_axis, y=y_axis, title=f"Bar Chart: {x_axis} vs {y_axis}")
        st.plotly_chart(bar_chart)

    elif chart_selection == "Boxplot":
        st.write("### Boxplot")
        y_axis = st.selectbox("Select Y-axis", numeric_columns, key="box_y")
        box_chart = px.box(df_cleaned, y=y_axis, title=f"Box Plot of {y_axis}")
        st.plotly_chart(box_chart)

    # Checkbox to show raw data
    if st.checkbox("Show raw data"):
        st.write("### Raw Dataset")
        st.write(df_cleaned)

else:
    st.info("Please upload a CSV file to proceed.")