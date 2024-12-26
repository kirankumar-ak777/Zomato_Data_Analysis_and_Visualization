
# Zomato Data Analysis and Visualization

## Introduction
This project focuses on exploring Zomato's restaurant data through data preprocessing, exploratory data analysis (EDA), and interactive visualization. The goal is to extract valuable insights into customer behavior, preferences, and industry trends, enabling better decision-making for restaurant businesses.

## Project Workflow

### 1.Data Preprocessing
   **Importing Necessary Packages**  
   - Essential libraries like Plotly, Dash, Pandas, Seaborn, and Matplotlib are used for analysis and visualization.

   **Reading and Merging Data**  
   - Zomato's main dataset and the country information dataset are loaded and merged based on the 'Country Code'.

   **Feature Engineering**  
   - A new column, 'Converted Cost (INR)', is created by converting the 'Average Cost for two' to Indian currency.
   - The 'Cuisines' column is split, and the data is exploded for further analysis.

   **Saving Processed Data**  
   - The processed data is saved to a new CSV file for further use.

## 2. Exploratory Data Analysis (EDA)
   **Loading Processed Data**  
   - The processed data is loaded for analysis.

   **Basic Statistics and Visualization**  
   - Various statistical analyses and visualizations are performed, such as histograms, count plots, scatter plots, and box plots.

## Dashboard Modules

### 1. Country-Based Analysis Dashboard
   **Dashboard Layout**  
   - A Dash app is created with a dropdown for country selection. Graphs display cuisine analysis, ratings, delivery services, and cost analysis. 
   - The most costly cuisine is dynamically displayed based on user selection.

   **Dashboard Callbacks**  
   - Callbacks are implemented to update graphs and display dynamic information based on user input. 

   **Access the Dashboard**  
   - [Country-Based Analysis Dashboard](https://zomato-data-visualization-01.streamlit.app/)

### 2. City-Based Analysis Dashboard
   **Dashboard Layout**  
   - A Dash app is created with dropdowns for country and city selection. Graphs display famous cuisine, costlier cuisine, rating count, and delivery mode.

   **Dashboard Callbacks**  
   - Callbacks are implemented to update city dropdown options and update graphs based on user input. 

   **Access the Dashboard**  
   - [City-Based Analysis Dashboard](https://zomato-data-visualization-02.streamlit.app/)

### 3. City Comparison within India
   **Analysis**  
   - Data is filtered for India, and reports are generated on the number of restaurants per city, online delivery expenses, dine-in expenses, and average cost for two.

   **Dashboard**  
   - The figures are displayed to compare cities within India.

   **Access the Dashboard**  
   - [City Comparison Dashboard](https://zomato-data-visualization-03.streamlit.app/)

## Technologies Used
- **Python**: Main programming language for data processing and building the dashboards.
- **Pandas**: For data manipulation and preprocessing.
- **Plotly & Dash**: For creating interactive visualizations and web-based dashboards.
- **Streamlit**: For deploying the interactive dashboards online.
- **Seaborn & Matplotlib**: For additional data visualizations during EDA.
