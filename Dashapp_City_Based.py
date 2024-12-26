import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go # or plotly.express as px
fig = go.Figure() # or any Plotly Express function e.g. px.bar(...)
from dash import Dash
import dash

df_zomato_final = pd.read_csv("E:/DATA SCIENCE - COURSE - GUVI/New folder/Zomato_final.csv")


# Create Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("City Analysis Dashboard"),

    # Dropdown for country selection
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in df_zomato_final['Country'].unique()],
        value='India',
        multi=False,
        style={'width': '50%'}
    ),

    # Dropdown for city selection
    dcc.Dropdown(
        id='city-dropdown',
        multi=False,
        style={'width': '50%'}
    ),

    # Famous Cuisine in the City
    dcc.Graph(id='famous-cuisine'),

    # Costlier Cuisine in the City
    dcc.Graph(id='costlier-cuisine'),

    # Rating Count in the City
    dcc.Graph(id='rating-count'),

    # Pie Chart Online Delivery vs Dine-In
    dcc.Graph(id='delivery-mode')
])

# Callback to update city dropdown based on country selection
@app.callback(
    Output('city-dropdown', 'options'),
    [Input('country-dropdown', 'value')]
)
def update_cities(selected_country):
    cities = df_zomato_final[df_zomato_final['Country'] == selected_country]['City'].unique()
    city_options = [{'label': city, 'value': city} for city in cities]
    return city_options

# Callback to update graphs based on user input
@app.callback(
    [Output('famous-cuisine', 'figure'),
     Output('costlier-cuisine', 'figure'),
     Output('rating-count', 'figure'),
     Output('delivery-mode', 'figure')],
    [Input('country-dropdown', 'value'),
     Input('city-dropdown', 'value')]
)
def update_city_graphs(selected_country, selected_city):
    # Filter DataFrame based on user input
    filtered_df = df_zomato_final[(df_zomato_final['Country'] == selected_country) & (df_zomato_final['City'] == selected_city)]

    # Famous Cuisine in the City
    fig_famous_cuisine = px.bar(
        filtered_df['Cuisines'].value_counts().nlargest(10).reset_index(),
        x='Cuisines',  # 'index' is the column name created by reset_index() for cuisine names
        y='count',  # Number of occurrences
        title='Famous Cuisine in the City',
        labels={'index': 'Cuisine', 'Cuisines': 'Number of Occurrences'},
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    # Add data labels to the bar chart
    fig_famous_cuisine.update_traces(texttemplate='%{y}', textposition='outside')


    # Costlier Cuisine in the City
    fig_costlier_cuisine = px.box(filtered_df.groupby('Cuisines').agg({'Converted Cost (INR)': 'mean'}).reset_index(), x='Cuisines', y='Converted Cost (INR)', title='Costlier Cuisine in the City',color_discrete_sequence=px.colors.qualitative.Plotly)

    
    # Rating Count in the City
    fig_rating_count = px.bar(filtered_df, x='Cuisines', y='Votes', title='Rating Count in the City',color_discrete_sequence=px.colors.qualitative.Plotly)
    # Add data labels to the bar chart
    fig_rating_count.update_traces(texttemplate='%{y}', textposition='outside')


    # Pie Chart Online Delivery vs Dine-In
    fig_delivery_mode = px.pie(filtered_df, names='Online Delivery', title='Delivery Mode in the City', color_discrete_sequence=px.colors.qualitative.Plotly)
    # Show percentage labels on the pie chart
    fig_delivery_mode.update_traces(textinfo='percent+label')

    return fig_famous_cuisine, fig_costlier_cuisine, fig_rating_count, fig_delivery_mode

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
