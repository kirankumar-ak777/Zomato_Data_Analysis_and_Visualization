import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go # or plotly.express as px
fig = go.Figure() # or any Plotly Express function e.g. px.bar(...)
from dash import Dash

df_zomato_final = pd.read_csv("E:/DATA SCIENCE - COURSE - GUVI/New folder/Zomato_final.csv")

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Restaurant Analysis Dashboard"),

    # Dropdown for country selection
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in df_zomato_final['Country'].unique()],
        value="India",
        multi=False,
        style={'width': '50%'}
    ),

    # Cuisine Analysis
    dcc.Graph(id='cuisine-analysis'),

    # Ratings Analysis
    dcc.Graph(id='ratings-analysis'),

    # Delivery Services
    dcc.Graph(id='delivery-services'),

    # Cost Analysis
    dcc.Graph(id='cost-analysis'),

    # Display the most costly cuisine
    html.Div(id='most-costly-cuisine', style={'margin-top': '20px', 'font-size': '18px'})
])

# Callback to update graphs based on user input
@app.callback(
    [Output('cuisine-analysis', 'figure'),
     Output('ratings-analysis', 'figure'),
     Output('delivery-services', 'figure'),
     Output('cost-analysis', 'figure'),
     Output('most-costly-cuisine', 'children')],
    [Input('country-dropdown', 'value')]
)
def update_graphs(selected_country):
    # Filter DataFrame based on user input
    df_filter = df_zomato_final[df_zomato_final['Country'] == selected_country]

    # Cuisine Analysis
    fig_cuisine = px.bar(df_filter,x='Cuisines',title='Cuisine Analysis',color_discrete_sequence=px.colors.qualitative.Set1,
    hover_data={'Cuisines': True}  ) # Enables hover data for the 'Cuisines' column)   
    # Ratings Analysis - Restaurant-wise
    fig_ratings = px.bar(df_filter, x='Restaurant Name', y='Aggregate_Rating', title='Ratings Analysis', color_discrete_sequence=px.colors.qualitative.Set2)

    # Delivery Services
    fig_delivery = px.pie(df_filter.drop_duplicates(subset=['Restaurant Name']), names='Online Delivery', title='Delivery Services', color_discrete_sequence=px.colors.qualitative.Plotly)

    # Cost Analysis using Converted Cost (INR)
    fig_cost = px.box(df_filter.groupby('Cuisines').agg({'Converted Cost (INR)': 'mean'}).reset_index(), x='Cuisines', y='Converted Cost (INR)', title='Cost Analysis',hover_data={'Converted Cost (INR)': True}, color_discrete_sequence=px.colors.qualitative.Set3)

    # Find the most costly cuisine
    most_costly_cuisine = df_filter.groupby('Cuisines')['Converted Cost (INR)'].mean().idxmax()

    return fig_cuisine, fig_ratings, fig_delivery, fig_cost, f'The most costly cuisine is "{most_costly_cuisine}"'

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)