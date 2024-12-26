import streamlit as st
import base64
import pandas as pd
import plotly.express as px

# Load Zomato logo (Ensure 'zomato_logo.png' is in the correct directory)
logo_path = "E:/DATA SCIENCE - COURSE - GUVI/GUVI Project/Zomoto Data Analysis and Visualisation/work_banner_vyEql_Zomato.jpg"

# Reading the dataframe
data = pd.read_csv('Zomato_final.csv')
df = pd.DataFrame(data)


# Function to encode the image as base64 and set it as background
def set_background(image_file):
    with open(image_file, "rb") as image:
        encoded_string = base64.b64encode(image.read()).decode("utf-8")
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('data:image/png;base64,{encoded_string}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        .content {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            color: white;
        }}
        .button {{
            display: inline-block;
            padding: 10px 20px;
            margin: 10px;
            border: none;
            border-radius: 5px;
            color: white;
            font-size: 16px;
            cursor: pointer;
            text-decoration: none;
        }}
        .restaurant-analysis {{
            background-color: #3498db;
        }}
        .city-analysis {{
            background-color: #e74c3c;
        }}
        .restaurants-per-city {{
            background-color: #2ecc71;
        }}
        button[data-baseweb="button"][id="previous"] {{
            position: fixed;
            bottom: 20px;
            left: 20px;
            background-color: #3498db;
            color: white;
            font-size: 16px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Initialize session state to manage page navigation
if 'page' not in st.session_state:
    st.session_state.page = 'login'  # Set the default page to login

# Function to display the login page
def login_page():
    # Set background image
    set_background(logo_path)

    # Center the title and button
    st.markdown('<div class="content">', unsafe_allow_html=True)
    st.title("Welcome to Zomato Data Analysis and Visualization")
    
    if st.button("Explore Zomato Data Analysis"):
        st.session_state.page = 'login_dashboard'  # Switch to login_dashboard page

    st.markdown('</div>', unsafe_allow_html=True)

# Function to display specific analysis page
def analysis_page(page_name):
    st.title(f"{page_name} Page")
    if st.button("Previous Page"):
        st.session_state.page = 'login_dashboard'

# Function to display login dashboard with a "Previous Page" button
def login_dashboard():
    st.markdown('<div class="center-content">', unsafe_allow_html=True)  # Center content
    st.title("Zomato Analysis and Visualization Dashboard")
    st.markdown("Select any of the analysis and visualization options.")

    # Buttons for analysis options
    if st.button("💼 Country_Based Analysis Dashboard"):
        st.session_state.page = 'Country_Based_Analysis'
        
    if st.button("🏙️ City_Based Analysis Dashboard"):
        st.session_state.page = 'City_Based_Analysis'

    if st.button("🍽️Comparison_Based Indian_Cities Analysis Dashboard"):
        st.session_state.page = 'Comparison_Based Indian_Cities Analysis'

    st.markdown('</div>', unsafe_allow_html=True)

    # "Previous Page" button at the bottom-left corner
    if st.button("Previous Page", key="previous"):
        st.session_state.page = 'login'

# Example function calls based on session state
def main_dash():
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = 'login'

    # Page navigation logic
    if st.session_state.page == 'login':
        login_page()
        
    elif st.session_state.page == 'login_dashboard':
        login_dashboard()

    elif st.session_state.page == 'Country_Based_Analysis':
        st.set_page_config(layout="wide")
        analysis_page("Country_Based_Analysis")
        def Country_Based():
            # Dropdown for country selection
            selected_country = st.selectbox("Select Country", df['Country'].unique(), index=0)

            # Filter DataFrame based on user input
            df_filter = df[df['Country'] == selected_country]

            # Cuisine Analysis
            st.plotly_chart(px.bar(df_filter,x='Cuisines',title='Cuisine Analysis',color_discrete_sequence=px.colors.qualitative.Set1,
                            hover_data={'Cuisines': True}))

            # Ratings Analysis - Restaurant-wise
            st.plotly_chart(px.bar(df_filter, x='Restaurant Name', y='Aggregate_Rating', title='Ratings Analysis', color_discrete_sequence=px.colors.qualitative.Set2))

            # Delivery Services
            st.plotly_chart(px.pie(df_filter.drop_duplicates(subset=['Restaurant Name']), names='Online Delivery', title='Delivery Services', color_discrete_sequence=px.colors.qualitative.Plotly))

            # Cost Analysis using Converted Cost (INR)
            st.plotly_chart(px.box(df_filter.groupby('Cuisines').agg({'Converted Cost (INR)': 'mean'}).reset_index(), 
                                   x='Cuisines', y='Converted Cost (INR)', title='Cost Analysis'))

            # Find the most costly cuisine
            most_costly_cuisine = df_filter.groupby('Cuisines')['Converted Cost (INR)'].mean().idxmax()

            st.write(f'The most costly cuisine in {selected_country} is "{most_costly_cuisine}"')

        if __name__ == '__main__':
            Country_Based()

    elif st.session_state.page == 'City_Based_Analysis':
        st.set_page_config(layout="wide")
        analysis_page("City_Based_Analysis")
        def City_Based():
           
            # Dropdown for country selection
            selected_country = st.selectbox("Select Country", df['Country'].unique(), index=0)

            # Dropdown for city selection
            selected_city = st.selectbox("Select City", df[df['Country'] == selected_country]['City'].unique(), index=0)

            # Filter DataFrame based on user input
            df_filter = df[(df['Country'] == selected_country) & (df['City'] == selected_city)]

            # Famous Cuisine in the City
            st.plotly_chart(px.bar(
                                    df_filter['Cuisines'].value_counts().nlargest(10).reset_index(),
                                    x='Cuisines',  # 'index' is the column name created by reset_index() for cuisine names
                                    y='count',  # Number of occurrences
                                    title='Famous Cuisine in the City',
                                    labels={'index': 'Cuisine', 'Cuisines': 'Number of Occurrences'},
                                    color_discrete_sequence=px.colors.qualitative.Plotly
            ))

            # Costlier Cuisine in the City
            st.plotly_chart(px.box(df_filter.groupby('Cuisines').agg({'Converted Cost (INR)': 'mean'}).reset_index(), x='Cuisines', y='Converted Cost (INR)', 
                                   title='Costlier Cuisine in the City',color_discrete_sequence=px.colors.qualitative.Plotly))

            # Rating Count in the City
            st.plotly_chart(px.bar(df_filter, x='Cuisines', y='Votes', title='Rating Count in the City',
                                   color_discrete_sequence=px.colors.qualitative.Plotly))

            # Pie Chart Online Delivery vs Dine-In
            st.plotly_chart(px.pie(df_filter, names='Online Delivery', title='Delivery Mode in the City', color_discrete_sequence=px.colors.qualitative.Plotly))

        if __name__ == '__main__':
            City_Based()
        

    elif st.session_state.page == 'Comparison_Based Indian_Cities Analysis':
        st.set_page_config(layout="wide")
        analysis_page("Comparison_Based Indian_Cities Analysis")
        df_india =df[df['Country'] == 'India']

        def City_Comparision_In_India():

            # Report 1: Comparison Between Cities in India
            df_grouped = df_india.groupby('City').size().reset_index(name='Number of Restaurants')
            st.plotly_chart(px.bar(df_grouped, x='City', y='Number of Restaurants', title='Number of Restaurants per City',
                            color_discrete_sequence=px.colors.qualitative.Plotly  # Change color scheme
                            ))

            # Report 2: Online Delivery Expenses in Different Cities
            online_delivery_data = df_india.groupby(['City', 'Online Delivery']).size().reset_index(name='Count')
            st.plotly_chart(px.bar(online_delivery_data,x='City', y='Count', color='Online Delivery',
                            title='Online Delivery Expenses in Different Cities',color_discrete_sequence=px.colors.qualitative.Plotly))

            # Report 3: Dine-In Expenses in Different Cities
            dine_in_data = df_india.groupby(['City', 'Accepts_Table_Booking']).size().reset_index(name='Count')
            st.plotly_chart(px.bar(dine_in_data,x='City', y='Count',color='Accepts_Table_Booking',
                                   title='Dine-In Expenses in Different Cities',color_discrete_sequence=px.colors.qualitative.Plotly))

            # Report 4: High Living Cost vs. Low Living Cost
            avg_cost_data = df_india.groupby('City')['Avg_Cost'].mean().reset_index(name='Avg_Cost')
            st.plotly_chart(px.bar(avg_cost_data,x='City', y='Avg_Cost',title='Average Cost for Two in Different Cities',
                                   color_discrete_sequence=px.colors.qualitative.Plotly))

        if __name__ == '__main__':
            City_Comparision_In_India()

if __name__ == "__main__":
    main_dash()
