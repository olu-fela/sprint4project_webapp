import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Interactive Data Visualization App", layout="wide")

# Load the dataset from a CSV file
@st.cache
def load_data():
    # Replace 'path_to_csv_file' with the actual path to your CSV file
    try:
        df = pd.read_csv("https://github.com/olu-fela/sprint4project_webapp/blob/main/vehicles_us.csv?raw=true")
        return df
    except FileNotFoundError:
        uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            return df
        else:
            st.warning("Please upload a CSV file to proceed.")
            return None

# Load data
df = load_data()

if df is not None:
    # Split the 'model' column into 'make' and 'model_type'
    if "model" in df.columns:
        df[["make", "model_type"]] = df["model"].str.split(" ", n=1, expand=True)

        # Reorder columns to place 'brand' and 'model_number' next to 'model'
        columns_order = (
            df.columns[:2].tolist() +  # Columns before 'model'
            ["model", "make", "model_type"] +  # 'model' and the new columns
            df.columns[3:-2].tolist()  # Remaining columns after 'model'
        )
        df = df[columns_order]

    if "date_posted" in df.columns:
        df["date_posted"] = pd.to_datetime(df["date_posted"])
        df["date_sold"] = df["date_posted"] + pd.to_timedelta(df["days_listed"], unit="d")

    if "is_4wd" in df.columns:
        df['is_4wd'].fillna(0, inplace=True)

    if "paint_color" in df.columns:
        df['paint_color'].fillna('Unknown', inplace=True)

    if "cylinders" in df.columns:
        # Group by model and model_year and compute the median for cylinders
        grouped_medians = (
            df.groupby(["model", "model_year"])["cylinders"]
            .median()
            .reset_index()
            .rename(columns={"cylinders": "median_cylinders"})
        )

        # Ensure median_cylinders is an integer
        grouped_medians["median_cylinders"] = grouped_medians["median_cylinders"].round().astype("Int64")

        # Merge the median values back into the original dataframe
        df = pd.merge(df, grouped_medians, on=["model", "model_year"], how="left")

        # Fill missing values in cylinders with the median
        df["cylinders"] = df["cylinders"].fillna(df["median_cylinders"])

        # Drop the auxiliary column
        df = df.drop(columns=["median_cylinders"])

    if "odometer" in df.columns:
        # Group by relevant columns and compute the mean for odometer
        group_by_columns = ["model_year", "model", "fuel", "transmission", "type", "is_4wd"]

        # Compute mean odometer for each group
        grouped_means = (
            df.groupby(group_by_columns, dropna=False)["odometer"]
            .mean()
            .reset_index()
            .rename(columns={"odometer": "mean_odometer"})
        )

        # Merge the mean values back into the original dataframe
        df = pd.merge(df, grouped_means, on=group_by_columns, how="left")

        # Fill missing values in odometer with the computed mean
        df["odometer"] = df["odometer"].fillna(df["mean_odometer"])

        # Drop the auxiliary column
        df = df.drop(columns=["mean_odometer"])

    
    
    # Header and Introduction
    st.title("Interactive Data Visualization with Streamlit")
    st.header("Car Advertisement Data Analysis")
    st.markdown("""
    This application allows you to visualize Car Advertisement data interactively using Plotly and Seaborn charts.
    """)

    st.write("### Dataset Preview")
    st.write(df.head(10))

    # Streamlit app layout

    st.sidebar.header("Visualization Options")

    # Sidebar menu for chart selection
    chart_type = st.sidebar.selectbox(
        "Select a chart to display:",
        [
            "Scatter Plot: Odometer vs. Days Listed (Segmented by Condition)",
            "Scatter Plot: Price vs. Days Listed (Segmented by Condition)",
            "Scatter Plot: Price vs. Odometer (Segmented by Condition)",
            "Bar Plot: Total Price by Decade Range",
            "Bar Plot: Sales and Revenue by Car Make",
            "Bar Plot: Car Brand - Pricing Distribution",
            "Bar Plot: Average Price and Total Sales by Fuel Type",
            "Bar Plot: Average Days Listing by Car Brand",
            "Bar Plot: Sales by Model Year Decade Range",
            "Histogram: Price Distribution",
            "Histogram: Days Listed Distribution",
            "Histogram: Odometer Distribution"
        ],
    )

    # Display the selected chart
    st.write("### Data Visualization")
    st.write("Select a chart type from the sidebar to display.")
    # Scatter Plot: Odometer vs. Days Listed (Segmented by Condition)
    if chart_type == "Scatter Plot: Odometer vs. Days Listed (Segmented by Condition)":
        st.subheader("Odometer vs. Days Listed (Segmented by Condition)")
        # Create a scatter plot segmented by condition
        fig = px.scatter(
            df,
            x="odometer",
            y="days_listed",
            color="condition",
            title="Odometer vs. Days Listed by Condition",
            labels={"odometer": "Odometer (miles)", "days_listed": "Days Listed"},
            hover_data=["condition"],  # Additional details on hover
        )
        st.plotly_chart(fig)

    # Scatter Plot: Price vs. Days Listed (Segmented by Condition)
    if chart_type == "Scatter Plot: Price vs. Days Listed (Segmented by Condition)":
        st.subheader("Price vs. Days Listed (Segmented by Condition)")
        # Create a scatter plot segmented by condition
        fig = px.scatter(
            df,
            x="price",
            y="days_listed",
            color="condition",
            title="Price vs. Days Listed by Condition",
            labels={"price": "Total Price (USD)", "days_listed": "Days Listed"},
            hover_data=["condition"],  # Additional details on hover
        )
        st.plotly_chart(fig)

    # Scatter Plot: Price vs. Odometer (Segmented by Condition)
    if chart_type == "Scatter Plot: Price vs. Odometer (Segmented by Condition)":
        st.subheader("Price vs. Odometer (Segmented by Condition)")
        # Create a scatter plot segmented by condition
        fig = px.scatter(
            df,
            x="price",
            y="odometer",
            color="condition",
            title="Price vs. Odometer by Condition",
            labels={"price": "Total Price (USD)", "odometer": "Odometer (Miles)"},
            hover_data=["condition"],  # Additional details on hover
        )
        st.plotly_chart(fig)

    # Bar Plot: Total Price by Decade Range
    elif chart_type == "Bar Plot: Total Price by Decade Range":
        st.subheader("Total Sale Price by Decade Range")
        # Define bins and labels for model year ranges
        bins = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]
        labels = ["1900-1910", "1910-1920", "1920-1930", "1930-1940", "1940-1950", "1950-1960", 
                "1960-1970", "1970-1980", "1980-1990", "1990-2000", "2000-2010", "2010-2020"]

        # Create a new column for model year ranges
        df["model_year_range"] = pd.cut(df["model_year"], bins=bins, labels=labels, right=False)

        # Calculate total price by model year range and make
        total_price_by_decade_make = (
            df.groupby(["model_year_range", "make"])["price"]
            .sum()
            .reset_index()
        )

        # Sort the data by model year range (ascending order)
        total_price_by_decade_make["model_year_range"] = pd.Categorical(
            total_price_by_decade_make["model_year_range"],
            categories=labels,  # Ensure correct order based on predefined labels
            ordered=True
        )
        total_price_by_decade_make = total_price_by_decade_make.sort_values(by="model_year_range")


        # Create an interactive bar plot with Plotly Express
        fig = px.bar(
            total_price_by_decade_make,
            x="model_year_range",
            y="price",
            color="make",  # Differentiate by car make
            title="Total Price by Model Year Decade and Make",
            labels={"model_year_range": "Model Year Decade", "price": "Total Price (USD)", "make": "Car Make"},
            #text=total_price_by_decade_make["price"].apply(lambda x: f"${x / 1e6:,.2f}M"),  # Add formatted labels
        )

        # Customize layout
        fig.update_traces(textposition="outside")  # Position text labels outside bars
        fig.update_layout(
            xaxis=dict(title="Model Year Decade", tickangle=0, tickfont=dict(size=10)),
            yaxis=dict(title="Total Price (USD)", tickfont=dict(size=10)),
            title=dict(font=dict(size=14)),
            #plot_bgcolor="white",
            legend_title="Car Make",  # Add legend for car makes
        )

        st.plotly_chart(fig)

    # Bar Plot: Sales and Revenue by Car Make
    elif chart_type == "Bar Plot: Sales and Revenue by Car Make":
        if "make" in df.columns:
            st.subheader("Sales and Revenue by Car Make")
            # Calculate total car sales by make and condition
            sales_by_make_condition = (
                df.groupby(["make", "condition"])["price"]
                .count()
                .reset_index()
                .rename(columns={"price": "total_sales"})
            )

            # Calculate total sales revenue by make and condition
            revenue_by_make_condition = (
                df.groupby(["make", "condition"])["price"]
                .sum()
                .reset_index()
                .rename(columns={"price": "total_revenue"})
            )

            # Create the first Plotly bar chart: Total car sales by make and condition
            fig1 = px.bar(
                sales_by_make_condition,
                x="make",
                y="total_sales",
                color="condition",
                title="Distribution of Car Sales by Make and Condition",
                labels={"make": "Car Make", "total_sales": "Total Sales", "condition": "Condition"},
                text="total_sales",
                color_discrete_sequence=px.colors.sequential.Viridis,
            )

            # Customize the layout for fig1
            fig1.update_traces(textposition="outside")
            fig1.update_layout(
                xaxis=dict(title="Car Make", tickangle=45),
                yaxis=dict(title="Total Sales"),
                title=dict(font=dict(size=16)),
                legend_title="Condition",
                #plot_bgcolor="white",
            )

            # Create the second Plotly bar chart: Total sales revenue by make and condition
            fig2 = px.bar(
                revenue_by_make_condition,
                x="make",
                y="total_revenue",
                color="condition",
                title="Distribution of Sales Revenue by Make and Condition",
                labels={"make": "Car Make", "total_revenue": "Total Revenue (USD)", "condition": "Condition"},
                text=revenue_by_make_condition["total_revenue"].apply(lambda x: f"${x / 1e6:.2f}M"),
                color_discrete_sequence=px.colors.sequential.Plasma,
            )

            # Customize the layout for fig2
            fig2.update_traces(textposition="outside")
            fig2.update_layout(
                xaxis=dict(title="Car Make", tickangle=45),
                yaxis=dict(title="Total Revenue (USD)"),
                title=dict(font=dict(size=16)),
                legend_title="Condition",
                #plot_bgcolor="white",
            )

            # Display the plots
            #fig1.show()
            #fig2.show()

            #st.pyplot(plt)
            st.plotly_chart(fig1)
            st.plotly_chart(fig2)
        else:
            st.warning("The dataset must include 'make' for this chart.")

    # Bar Plot: Car Brand - Pricing Distribution
    elif chart_type == "Bar Plot: Car Brand - Pricing Distribution":
        if "make" in df.columns:
            st.subheader("Average Price by Car Make")
            # Calculate the average price by make and condition, sorted by price
            avg_price_by_make_condition = (
                df.groupby(["make", "condition"])["price"]
                .mean()
                .reset_index()
                .sort_values(by="price", ascending=False)
            )

            # Capitalize the first letter of each "make" and "condition" for better display
            avg_price_by_make_condition["make"] = avg_price_by_make_condition["make"].str.capitalize()
            avg_price_by_make_condition["condition"] = avg_price_by_make_condition["condition"].str.capitalize()

            # Create the Plotly bar chart
            fig = px.bar(
                avg_price_by_make_condition,
                x="make",
                y="price",
                color="condition",  # Use condition as the color-coded category
                title="Dealership Car Brand Average Pricing by Condition",
                labels={"make": "Car Brand", "price": "Average Price (USD)", "condition": "Condition"},
                #text=avg_price_by_make_condition["price"].apply(lambda x: f"${x / 1e3:.1f}K"),  # Add labels
                color_discrete_sequence=px.colors.qualitative.Set3,  # Set a qualitative color palette
            )

            # Customize the layout
            fig.update_traces(textposition="outside")  # Position labels outside the bars
            fig.update_layout(
                xaxis=dict(title="Car Brand", tickangle=90, tickfont=dict(size=10)),
                yaxis=dict(title="Average Price (USD)", tickfont=dict(size=10)),
                title=dict(font=dict(size=14)),  # Adjust title font size
                #plot_bgcolor="white",  # Set background color
            )


            st.plotly_chart(fig)
        else:
            st.warning("The dataset must include 'make' for this chart.")

    # Bar Plot: Average Price and Total Sales by Fuel Type
    elif chart_type == "Bar Plot: Average Price and Total Sales by Fuel Type":
        # Calculate average price and total sales by fuel type
        st.subheader("Average Price and Total Sales by Fuel Type")
        # Calculate average price by fuel type and condition
        avg_price_by_fuel_condition = (
            df.groupby(["fuel", "condition"])["price"]
            .mean()
            .reset_index()
            .rename(columns={"price": "average_price"})
        )

        # Calculate total sales by fuel type and condition
        total_sales_by_fuel_condition = (
            df.groupby(["fuel", "condition"])["price"]
            .count()
            .reset_index()
            .rename(columns={"price": "total_sales"})
        )

        # Create the first Plotly bar chart: Average Price by Fuel Type and Condition
        fig1 = px.bar(
            avg_price_by_fuel_condition,
            x="fuel",
            y="average_price",
            color="condition",  # Differentiate bars by condition
            title="Average Price by Fuel Type and Condition",
            labels={"fuel": "Fuel Type", "average_price": "Average Price (USD)", "condition": "Condition"},
            text=avg_price_by_fuel_condition["average_price"].apply(lambda x: f"${x:,.0f}"),  # Add labels
            color_discrete_sequence=px.colors.qualitative.Vivid,  # Set a qualitative color palette
        )

        # Customize the layout for fig1
        fig1.update_traces(textposition="outside")
        fig1.update_layout(
            xaxis=dict(title="Fuel Type"),
            yaxis=dict(title="Average Price (USD)"),
            title=dict(font=dict(size=16)),
            legend_title="Condition",
        )

        # Create the second Plotly bar chart: Total Sales by Fuel Type and Condition
        fig2 = px.bar(
            total_sales_by_fuel_condition,
            x="fuel",
            y="total_sales",
            color="condition",  # Differentiate bars by condition
            title="Total Sales by Fuel Type and Condition",
            labels={"fuel": "Fuel Type", "total_sales": "Total Sales", "condition": "Condition"},
            text=total_sales_by_fuel_condition["total_sales"],  # Add labels
            color_discrete_sequence=px.colors.qualitative.Pastel,  # Set a qualitative color palette
        )

        # Customize the layout for fig2
        fig2.update_traces(textposition="outside")
        fig2.update_layout(
            xaxis=dict(title="Fuel Type"),
            yaxis=dict(title="Total Sales"),
            title=dict(font=dict(size=16)),
            legend_title="Condition",
        )

        # Display the plots
        st.plotly_chart(fig1)
        st.plotly_chart(fig2)

    # Bar Plot: Sales by Car Brand
    elif chart_type == "Bar Plot: Average Days Listing by Car Brand":
        if "make" in df.columns:
            st.subheader("Average Days Listing by Car Brand")
            # Calculate the average number of days listed by brand
            fastest_selling_brands = df.groupby("make")["days_listed"].mean().reset_index()
            fastest_selling_brands = fastest_selling_brands.sort_values(by="days_listed")

            # Create the bar plot
            plt.figure(figsize=(12, 6))
            sns.barplot(data=fastest_selling_brands, x="make", y="days_listed", palette="coolwarm")

            # Highlight the fastest selling brand
            fastest_brand = fastest_selling_brands.iloc[0]
            bar_x_position = fastest_selling_brands[fastest_selling_brands["make"] == fastest_brand["make"]].index[0]

            # Highlight the fastest selling brand
            fastest_brand = fastest_selling_brands.iloc[0]
            plt.text(
                0.1,
                fastest_brand["days_listed"] + 0.5,
                f"{fastest_brand['days_listed']:.1f} days",
                ha="center",
                fontsize=10,
                color="red",
                rotation=0,
            )

            # Customize the plot
            plt.title("Fastest Selling Car Brands", fontsize=16)
            plt.xlabel("Car Brand", fontsize=14)
            plt.ylabel("Average Days Listed", fontsize=14)
            plt.xticks(fontsize=9, rotation=90)
            plt.yticks(fontsize=10)
            plt.gca().spines["top"].set_visible(False)
            plt.gca().spines["right"].set_visible(False)
            plt.grid(axis='y', linestyle='--', alpha=0.7)

            # Adjust layout and display
            plt.tight_layout()
            st.pyplot(plt)
        else:
            st.warning("The dataset must include 'make' for this chart.")

    # Bar Plot: Sales by Model Year Decade Range
    elif chart_type == "Bar Plot: Sales by Model Year Decade Range":
        st.subheader("Sales by Model Year Decade Range")
        # Define bins and labels for model year ranges
        bins = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]
        labels = ["1900-1910", "1910-1920", "1920-1930", "1930-1940", "1940-1950", "1950-1960", 
                "1960-1970", "1970-1980", "1980-1990", "1990-2000", "2000-2010", "2010-2020"]

        # Add a new column for model year ranges
        df["model_year_range"] = pd.cut(df["model_year"], bins=bins, labels=labels, right=False)

        # Calculate median price by model year range and make
        median_price_by_decade_make = (
            df.groupby(["model_year_range", "make"])["price"]
            .median()
            .reset_index()
            .rename(columns={"price": "median_price"})
        )

        # Calculate total cars listed by model year range and make
        total_cars_by_decade_make = (
            df.groupby(["model_year_range", "make"])
            .size()
            .reset_index(name="total_cars")
        )

        # Create the first Plotly bar chart: Median Price by Decade and Make
        fig1 = px.bar(
            median_price_by_decade_make,
            x="model_year_range",
            y="median_price",
            color="make",  # Differentiate by car make
            title="Median Car Price by Decade and Make",
            labels={"model_year_range": "Model Year Decade", "median_price": "Median Price (USD)", "make": "Car Make"},
            text=median_price_by_decade_make["median_price"].apply(lambda x: f"${x / 1e3:.2f}K"),  # Add formatted labels
            color_discrete_sequence=px.colors.qualitative.Vivid,
        )

        # Customize layout for fig1
        fig1.update_traces(textposition="outside")
        fig1.update_layout(
            xaxis=dict(title="Model Year Decade", tickangle=0),
            yaxis=dict(title="Median Price (USD)"),
            title=dict(font=dict(size=16)),
            legend_title="Car Make",
        )

        # Create the second Plotly bar chart: Total Cars Listed by Decade and Make
        fig2 = px.bar(
            total_cars_by_decade_make,
            x="model_year_range",
            y="total_cars",
            color="make",  # Differentiate by car make
            title="Total Cars Listed by Decade and Make",
            labels={"model_year_range": "Model Year Decade", "total_cars": "Total Cars Listed", "make": "Car Make"},
            text=total_cars_by_decade_make["total_cars"],  # Add labels
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )

        # Customize layout for fig2
        fig2.update_traces(textposition="outside")
        fig2.update_layout(
            xaxis=dict(title="Model Year Decade", tickangle=0),
            yaxis=dict(title="Total Cars Listed"),
            title=dict(font=dict(size=16)),
            legend_title="Car Make",
        )

        # Display the plots
        st.plotly_chart(fig1)
        st.plotly_chart(fig2)
        
    # Histogram: Price Distribution
    elif chart_type == "Histogram: Price Distribution":
        st.subheader("Price Distribution")
        plt.figure(figsize=(12, 5))
        sns.histplot(data=df, x='price', bins=50, palette='viridis')
        plt.title("Price Distribution")
        plt.xlabel("Price (USD)", fontsize=10)
        plt.ylabel("Count of Cars on Sale", fontsize=10)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)
        st.pyplot(plt)

    # Histogram: Days Listed Distribution
    elif chart_type == "Histogram: Days Listed Distribution":
        st.subheader("Days Listed Distribution")
        plt.figure(figsize=(12, 5))
        sns.histplot(data=df, x='days_listed', hue="condition", bins=np.arange(0, 300, 10), palette='viridis')
        plt.title('Vehicle Listing Days Distribution')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.xticks(np.arange(0, 300, 20))
        plt.xlabel('Days Listed')
        plt.ylabel('# of Vehicles Listed for Sale')
        st.pyplot(plt)

    # Histogram: Odometer Distribution
    elif chart_type == "Histogram: Odometer Distribution":
        st.subheader("Vehicle Mileage Distribution")
        # Create the histogram using Plotly Express
        fig = px.histogram(
            df,
            x="odometer",
            color="condition",  # Segment by condition
            nbins=50,  # Equivalent to bins=50
            title="Vehicle Mileage Distribution by Condition",
            labels={"odometer": "Odometer (Miles)", "count": "Count of Cars on Sale", "condition": "Condition"},
            opacity=0.8,  # Adjust bar opacity
            color_discrete_sequence=px.colors.qualitative.Set2,  # Use a qualitative color palette
            marginal="rug",  # Optional: add a rug plot for distribution
        )

        # Customize the layout
        fig.update_layout(
            xaxis=dict(title="Odometer (Miles)", title_font=dict(size=12)),
            yaxis=dict(title="Count of Cars on Sale", title_font=dict(size=12)),
            title=dict(font=dict(size=16)),
            legend_title="Condition",
            bargap=0.1,  # Adjust spacing between bars
        )

        # Add gridlines
        fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor="lightgray")
        fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor="lightgray")

        # Show the plot
        st.plotly_chart(fig)

else:
    st.warning("Please upload a CSV file to proceed.")


