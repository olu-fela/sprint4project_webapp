import streamlit as st
import pandas as pd
import seaborn as sns
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
    
    # Header and Introduction
    st.title("Interactive Data Visualization with Streamlit")
    st.header("Car Sales Analysis")
    st.markdown("""
    This application allows you to:
    - Upload a CSV dataset.
    - Visualize data interactively using Plotly and Seaborn charts.
    """)

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
        bins = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]
        labels = ["1900-1910", "1910-1920", "1920-1930", "1930-1940", "1940-1950", "1950-1960", "1960-1970", "1970-1980", "1980-1990", "1990-2000", "2000-2010", "2010-2020"]
        df["model_year_range"] = pd.cut(df["model_year"], bins=bins, labels=labels, right=False)

        # Calculate total price by decade
        total_price_by_decade = df.groupby("model_year_range")["price"].sum().reset_index()
        total_price_by_decade.columns = ["model_year_range", "total_price"]

        # Create a bar plot
        plt.figure(figsize=(12, 6))
        sns.barplot(data=total_price_by_decade, x="model_year_range", y="total_price", palette="viridis")

        # Customize the plot
        plt.title("Total Price by Model Year Decade", fontsize=12)
        plt.xlabel("Model Year Decade", fontsize=10)
        plt.ylabel("Total Price (USD)", fontsize=10)
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Add bar labels
        for bar, value in zip(plt.gca().patches, total_price_by_decade["total_price"]):
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 1000,
                f"${value /1e6:,.2f}M",
                ha="center",
                fontsize=8
            )

            
        # Show the plot
        plt.tight_layout()
        st.pyplot(plt)

    # Bar Plot: Sales and Revenue by Car Make
    elif chart_type == "Bar Plot: Sales and Revenue by Car Make":
        if "make" in df.columns:
            st.subheader("Sales and Revenue by Car Make")
            # Calculate total car sales by make
            sales_by_make = df["make"].value_counts().reset_index()
            sales_by_make.columns = ["make", "total_sales"]

            # Calculate total sales revenue by make
            revenue_by_make = df.groupby("make")["price"].sum().reset_index().sort_values(by="price", ascending=False)
            revenue_by_make.columns = ["make", "total_revenue"]

            # Create subplots
            fig, axes = plt.subplots(1, 2, figsize=(20, 8), sharey=False)

            # Plot total car sales by make
            sns.barplot(data=sales_by_make, x="make", y="total_sales", palette="viridis", ax=axes[0])
            axes[0].set_title("Distribution of Car Sales by Make", fontsize=16)
            axes[0].set_xlabel("Car Make", fontsize=14)
            axes[0].set_ylabel("Total Sales", fontsize=14)
            axes[0].tick_params(axis="x", rotation=45)
            # Add labels
            for bar, value in zip(axes[0].patches, sales_by_make["total_sales"]):
                axes[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, f"{int(value):,}",
                            ha="center", va="bottom", fontsize=8, rotation=45)

            # Plot total sales revenue by make
            sns.barplot(data=revenue_by_make, x="make", y="total_revenue", palette="plasma", ax=axes[1])
            axes[1].set_title("Distribution of Sales Revenue by Make", fontsize=16)
            axes[1].set_xlabel("Car Make", fontsize=14)
            axes[1].set_ylabel("Total Revenue (USD)", fontsize=14)
            axes[1].tick_params(axis="x", rotation=45)

            # Add bar labels with values in millions
            for bar, value in zip(axes[1].patches, revenue_by_make["total_revenue"]):
                axes[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1000, f"${bar.get_height() / 1e6:.2f}M",
                            ha="center", va="bottom", fontsize=8, rotation=45)
                
            # Remove spines (outline box)
            axes[0].spines["top"].set_visible(False)
            axes[0].spines["right"].set_visible(False)
            axes[0].grid(axis='y', linestyle='--', alpha=0.7)

            axes[1].spines["top"].set_visible(False)
            axes[1].spines["right"].set_visible(False)
            axes[1].grid(axis='y', linestyle='--', alpha=0.7)

            # Adjust layout
            plt.tight_layout()

            st.pyplot(plt)
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
        avg_price_by_fuel = df.groupby("fuel")["price"].mean().reset_index().rename(columns={"price": "average_price"})
        total_sales_by_fuel = df.groupby("fuel")["price"].count().reset_index().rename(columns={"price": "total_sales"})

        # Create subplots
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        # Average Price by Fuel Type
        sns.barplot(data=avg_price_by_fuel, x="fuel", y="average_price", palette="viridis", ax=axes[0])
        axes[0].set_title("Average Price by Fuel Type", fontsize=16)
        axes[0].set_xlabel("Fuel Type", fontsize=14)
        axes[0].set_ylabel("Average Price (USD)", fontsize=14)
        axes[0].tick_params(axis="x")
        axes[0].spines["top"].set_visible(False)
        axes[0].spines["right"].set_visible(False)
        axes[0].grid(axis='y', linestyle='--', alpha=0.7)

        # Add labels
        for bar, value in zip(axes[0].patches, avg_price_by_fuel["average_price"]):
            axes[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, f"${value:,.0f}",
                        ha="center", va="bottom", fontsize=10)

        # Total Sales by Fuel Type
        sns.barplot(data=total_sales_by_fuel, x="fuel", y="total_sales", palette="plasma", ax=axes[1])
        axes[1].set_title("Total Sales by Fuel Type", fontsize=16)
        axes[1].set_xlabel("Fuel Type", fontsize=14)
        axes[1].set_ylabel("Total Sales", fontsize=14)
        axes[1].tick_params(axis="x")
        axes[1].spines["top"].set_visible(False)
        axes[1].spines["right"].set_visible(False)
        axes[1].grid(axis='y', linestyle='--', alpha=0.7)

        # Add labels
        for bar, value in zip(axes[1].patches, total_sales_by_fuel["total_sales"]):
            axes[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, f"{value:,.0f}",
                        ha="center", va="bottom", fontsize=10)

        # Adjust layout
        plt.tight_layout()
        st.pyplot(plt)

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
        bins = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]
        labels = ["1900-1910", "1910-1920", "1920-1930", "1930-1940", "1940-1950", "1950-1960", "1960-1970", "1970-1980", "1980-1990", "1990-2000", "2000-2010", "2010-2020"]
        df["model_year_range"] = pd.cut(df["model_year"], bins=bins, labels=labels, right=False)

        # Calculate median price by decade
        median_price_by_decade = df.groupby("model_year_range")["price"].median().reset_index()
        median_price_by_decade.columns = ["model_year_range", "median_price"]

        # Calculate total cars listed by decade
        total_cars_by_decade = df["model_year_range"].value_counts().reset_index()
        total_cars_by_decade.columns = ["model_year_range", "total_cars"]
        total_cars_by_decade = total_cars_by_decade.sort_values(by="model_year_range")

        # Create subplots
        fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=False)

        # Plot average price by decade
        sns.barplot(data=median_price_by_decade, x="model_year_range", y="median_price", palette="viridis", ax=axes[0])
        axes[0].set_title("Median Car Price by Decade", fontsize=16)
        axes[0].set_xlabel("Model Year Decade", fontsize=14)
        axes[0].set_ylabel("Median Car Price (USD)", fontsize=14)
        axes[0].tick_params(axis="x", rotation=90)
        axes[0].spines["top"].set_visible(False)
        axes[0].spines["right"].set_visible(False)
        axes[0].grid(axis='y', linestyle='--', alpha=0.7)

        # Add labels
        for bar, value in zip(axes[0].patches, median_price_by_decade["median_price"]):
            axes[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, f"${bar.get_height() / 1e3:.2f}k",
                        ha="center", va="bottom", fontsize=8)



        # Plot total cars listed by decade
        sns.barplot(data=total_cars_by_decade, x="model_year_range", y="total_cars", palette="plasma", ax=axes[1])
        axes[1].set_title("Total Cars Listed by Decade", fontsize=16)
        axes[1].set_xlabel("Model Year Decade", fontsize=14)
        axes[1].set_ylabel("Total Cars Listed", fontsize=14)
        axes[1].tick_params(axis="x", rotation=90)
        axes[1].spines["top"].set_visible(False)
        axes[1].spines["right"].set_visible(False)
        axes[1].grid(axis='y', linestyle='--', alpha=0.7)

        # Add bar labels with values in millions
        for bar, value in zip(axes[1].patches, total_cars_by_decade["total_cars"]):
            axes[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1000, f"{int(value):,}",
                        ha="center", va="bottom", fontsize=8)

        # Adjust layout
        plt.tight_layout()
        st.pyplot(plt)
        
    # Histogram: Price Distribution
    elif chart_type == "Histogram: Price Distribution":
        st.subheader("Price Distribution")
        plt.figure(figsize=(12, 4))
        sns.histplot(df["price"], bins=100, kde=True, color="skyblue")
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
        st.subheader("Odometer Distribution")
        plt.figure(figsize=(12, 4))
        sns.histplot(df["odometer"], bins=50, kde=True, element="bars", color="skyblue")
        plt.title("Vehicle Mileage Distribution")
        plt.xlabel("Odometer (Miles)", fontsize=10)
        plt.ylabel("Count of Cars on Sale", fontsize=10)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)
        st.pyplot(plt)

else:
    st.warning("Please upload a CSV file to proceed.")
