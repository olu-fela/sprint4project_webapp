# TripleTen Sprint 4 Project - Web Application Deployment: EDA for Car Advertisement Dataset

## Project Description
This is an interactive web application built using Streamlit, Pandas and Plotly Express.
This app allows users to:
- Upload a CSV file.
- Clean and preprocess the dataset.
- Generate various interactive visualizations.

The app is designed to simplify data exploration and visualization tasks, making it easy to analyze datasets and identify trends.

## Features
1. Upload Dataset: Upload a CSV file for analysis.
2. Data Cleaning:
    - Inspect missing values.
    - Drop columns or fill missing values with a custom value.
3. Visualizations:
    - Histogram: View the distribution of numeric columns.
    - Scatter Plot: Display relationships between two numeric columns.
    - Scatterplot Matrix: Explore pairwise relationships in the dataset.
    - Heatmap: Visualize correlations between numeric columns.
    - Distplot: Show distributions with optional marginal views.
    - Bar Chart: Compare values of categorical or numeric columns.
    - Boxplot: Display spread and outliers of numeric data.
4. Interactive Sidebar:
    - Navigate through visualization options.
    - Filter the dataset based on categorical columns.
    - Customize plot behavior using checkboxes and dropdown menus.
5. Raw Data Display:
    - View the uploaded dataset after cleaning and filtering.


## Technologies and Packages Used
This project leverages Python for its implementation and uses several libraries to streamline its functionality:
- Python: The core language used to implement the project.
- Pandas: For organizing and analyzing simulation data.
- Streamlit: For building and sharing interactive web apps.
- Altair: For creating interactive declarative visualizations.
- Plotly Express: For quick and easy creation of interactive plots and charts.


## Installation and Setup
To run the application on your local machine, follow these steps:

## Prerequisites
Ensure you have Python 3.8 or above installed on your system. You can check your Python version by running:
- `python --version`

## Step 1: Clone the Repository
Clone the project repository from GitHub or download the source code.
- `git clone https://github.com/olu-fela/sprint4project_webapp.git`
- `cd sprint4project_webapp`

## Step 2: Create a Virtual Environment (Optional but Recommended)
Create and activate a virtual environment to isolate project dependencies.

## Step 3: Install Dependencies
Install the required Python libraries listed in the requirements.txt file.
- `pip install streamlit`
- `pip install -r requirements.txt`

## Step 4: Run the Application Locally
- Navigate to the project directory.
- Run the Streamlit app:
`streamlit run app.py`
- Open the local development server link in your browser (e.g. `http://localhost:10000`)

## Step 5: Deployment Instructions
This app can be deployed on platforms like Render, Streamlit Cloud, or Heroku. Below are the steps for deployment on Render:
- Create a new GitHub repository and push your code.
- Log in to Render.
- Create a new Web Service and link it to your GitHub repository.
- Set the start command to: `streamlit run app.py`
- Deploy the app. Render will provide a public URL to access your application.

## Contributing
Contributions are welcome! To contribute:
- Fork the repository.
- Create a new branch for your feature or bug fix.
- Submit a pull request with a detailed explanation of your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
If you have any questions or feedback, please contact:
- Name: Fela Soyemi
- Email: felasoyemi@gmail.com
- GitHub: olu-fela

