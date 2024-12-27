import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Interactive Data Visualization App", layout="wide")

# Header and Introduction
st.header("Interactive Data Visualization App with Natural Language Processing")
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

    # Identify and suggest columns to convert to datetime
    st.header("Identify Date-Like Columns")
    st.markdown("""
    This section identifies columns in your dataset that might contain date-like content and suggests converting them to datetime format.
    """)

    # Function to identify date-like columns
    def suggest_datetime_conversion(df):
        date_like_columns = []
        for col in df.columns:
            if df[col].dtype == 'object':  # Check for object types
                try:
                    pd.to_datetime(df[col], errors='raise')  # Attempt to convert
                    date_like_columns.append(col)
                except (ValueError, TypeError):
                    pass
        return date_like_columns

    # Run the function and display suggestions
    date_like_columns = suggest_datetime_conversion(df_cleaned)

    if date_like_columns:
        st.write("The following columns may contain date-like content:")
        st.write(date_like_columns)
        
        # Allow user to select columns to convert
        columns_to_convert = st.multiselect(
            "Select columns to convert to datetime format:",
            options=date_like_columns
        )
        
        if st.button("Convert to Datetime"):
            for col in columns_to_convert:
                df_cleaned[col] = pd.to_datetime(df_cleaned[col], errors='coerce')
            st.success(f"Converted columns to datetime format: {columns_to_convert}")
            st.write("Updated Dataset:")
            st.write(df_cleaned.head())
    else:
        st.write("No date-like columns were detected in the dataset.")

    def look_like_datetime(col):
        if col.dtype == 'object':  # Check for object types
            try:
                pd.to_datetime(col, errors='raise')  # Attempt to convert
                col = pd.to_datetime(col, errors='coerce')
                return col.dt.date
            except (ValueError, TypeError):
                pass
        


    # Sidebar menu for visualizations
    st.sidebar.header("Visualization Menu")
    chart_selection = st.sidebar.selectbox(
        "Select a chart to display:",
        ["Histogram", "Scatter Plot", "Scatterplot Matrix", "Heatmap", "Distplot", "Bar Chart", "Boxplot"]
    )

    numeric_columns = df_cleaned.select_dtypes(include=["float64", "int64"]).columns.tolist()
    categorical_columns = df_cleaned.select_dtypes(include=["object", "category"]).columns.tolist()

    # Display selected chart
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
        x_axis = st.selectbox("Select X-axis (Optional)", categorical_columns + [None], key="box_x")
        box_chart = px.box(df_cleaned, y=y_axis, x=x_axis, title=f"Box Plot of {y_axis} by {x_axis}")
        st.plotly_chart(box_chart)

    # Checkbox to show raw data
    if st.checkbox("Show raw data"):
        st.write("### Raw Dataset")
       
    # Function to process natural language criteria
    def process_natural_language_criteria(df, new_column_name, formula):
        try:
            # Ensure all column names in the formula are properly referenced
            for col in df.columns:
                if col in formula:
                    formula = formula.replace(col, f"df['{col}']")

            # Handle specific cases for datetime and integer operations
            for col1 in df.columns:
                for col2 in df.columns:
                    if f"df['{col1}'] + df['{col2}']" in formula:
                        if (
                            df[col1].dtype == 'object' and
                            df[col2].dtype in ["int32", "int64", "float64"]
                        ):
                            formula = formula.replace(
                                f"df['{col1}'] + df['{col2}']",
                                f"look_like_datetime(df['{col1}']) + pd.to_timedelta(df['{col2}'], unit='d')"
                            )
                        elif (
                            df[col2].dtype == "datetime64[ns]" and
                            df[col1].dtype in ["int64", "float64"]
                        ):
                            formula = formula.replace(
                                f"df['{col1}'] + df['{col2}']",
                                f"df['{col2}'] + pd.to_timedelta(df['{col1}'], unit='d')"
                            )
                        elif (
                            df[col1].dtype == "object" and
                            df[col2].dtype in ["int64", "float64"]
                        ):
                            formula = formula.replace(
                                f"df['{col1}'] + df['{col2}']",
                                f"df['{col1}'] + df['{col2}'].astype(str)"
                            )
                        elif (
                            df[col2].dtype == "object" and
                            df[col1].dtype in ["int64", "float64"]
                        ):
                            formula = formula.replace(
                                f"df['{col1}'] + df['{col2}']",
                                f"df['{col1}'].astype(str) + df['{col2}']"
                            )

            # Evaluate the formula
            df[new_column_name] = eval(formula)
            st.sidebar.success(f"New column '{new_column_name}' created successfully!")
            return df
        except Exception as e:
            st.sidebar.error(f"Error creating column: {e}")
            return df


    # Sidebar for column addition
    st.sidebar.header("Add Columns")
    st.sidebar.markdown("""
    Add new columns to your dataset by providing natural language criteria. Examples:
    - Add 30 days to a datetime column: `date_posted + 30`
    - Concatenate string and integer: `string_col + int_col`
    - Create a column that sums two columns: `col1 + col2`
    """)

    new_column_name = st.sidebar.text_input("Enter the name of the new column:", key="new_column_name")
    formula = st.sidebar.text_area("Enter the formula for the new column (use existing column names):", key="formula")

    if st.sidebar.button("Create Column"):
        if new_column_name and formula:
            df_cleaned = process_natural_language_criteria(df_cleaned, new_column_name, formula)
            st.write("Updated Dataset with New Column:")
            st.write(df_cleaned.head())
        else:
            st.sidebar.error("Please provide both a column name and a formula.")

