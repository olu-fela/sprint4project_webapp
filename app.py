import streamlit as st
import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Interactive Data Visualization App", layout="wide")

# Header and Introduction
st.header("Interactive Data Visualization with Streamlit")
st.markdown("""
This application allows you to:
- Upload a CSV dataset.
- Inspect and clean missing values.
- Add new columns by setting natural language criteria for computation.
- Visualize data interactively using various Plotly charts.
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

    numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
    categorical_columns = df.select_dtypes(include=["object", "category"]).columns.tolist()

    # Display selected chart
    if chart_selection == "Histogram":
        st.write("### Histogram")
        column = st.selectbox("Select a column for the histogram", numeric_columns)
        hist_chart = px.histogram(df, x=column, nbins=20, title=f"Histogram of {column}")
        st.plotly_chart(hist_chart)

    elif chart_selection == "Scatter Plot":
        st.write("### Scatter Plot")
        x_axis = st.selectbox("Select X-axis", numeric_columns, key="scatter_x")
        y_axis = st.selectbox("Select Y-axis", numeric_columns, key="scatter_y")
        scatter_chart = px.scatter(df, x=x_axis, y=y_axis, title=f"Scatter Plot: {x_axis} vs {y_axis}")
        st.plotly_chart(scatter_chart)

    elif chart_selection == "Scatterplot Matrix":
        st.write("### Scatterplot Matrix")
        scatter_matrix_chart = px.scatter_matrix(df, dimensions=numeric_columns[:4], title="Scatterplot Matrix")
        st.plotly_chart(scatter_matrix_chart)

    elif chart_selection == "Heatmap":
        st.write("### Heatmap")
        if len(numeric_columns) > 1:
            corr_matrix = df[numeric_columns].corr()
            heatmap_fig = px.imshow(corr_matrix, text_auto=True, title="Correlation Heatmap")
            st.plotly_chart(heatmap_fig)

    elif chart_selection == "Distplot":
        st.write("### Distribution Plot")
        x_axis = st.selectbox("Select X-axis", numeric_columns, key="dist_x")
        y_axis = st.selectbox("Select Y-axis (Optional)", numeric_columns + [None], key="dist_y")
        dist_chart = px.histogram(
            df, x=x_axis, y=y_axis, marginal="violin", title=f"Distribution of {x_axis}"
        )
        st.plotly_chart(dist_chart)

    elif chart_selection == "Bar Chart":
        st.write("### Bar Chart")
        x_axis = st.selectbox("Select X-axis", categorical_columns + numeric_columns, key="bar_x")
        y_axis = st.selectbox("Select Y-axis", numeric_columns, key="bar_y")
        bar_chart = px.bar(df, x=x_axis, y=y_axis, title=f"Bar Chart: {x_axis} vs {y_axis}")
        st.plotly_chart(bar_chart)

    elif chart_selection == "Boxplot":
        st.write("### Boxplot")
        y_axis = st.selectbox("Select Y-axis", numeric_columns, key="box_y")
        x_axis = st.selectbox("Select X-axis (Optional)", categorical_columns + [None], key="box_x")
        box_chart = px.box(df, y=y_axis, x=x_axis, title=f"Box Plot of {y_axis} by {x_axis}")
        st.plotly_chart(box_chart)

    # Data Cleaning
    def look_like_datetime(col):
        if col.dtype == 'object':  # Check for object types
            try:
                pd.to_datetime(col, errors='raise')  # Attempt to convert
                col = pd.to_datetime(col, errors='coerce')
                return col.dt.date
            except (ValueError, TypeError):
                pass
        
    
    # Checkbox to show raw data
    if st.checkbox("Show raw data"):
        st.write("### Raw Dataset")
    

  
