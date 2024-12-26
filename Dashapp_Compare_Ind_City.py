import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go # or plotly.express as px
fig = go.Figure() # or any Plotly Express function e.g. px.bar(...)
from dash import Dash
import dash

df_zomato_final = pd.read_csv("E:/DATA SCIENCE - COURSE - GUVI/New folder/Zomato_final.csv")


# Filter data for India
india_df = df_zomato_final[df_zomato_final['Country'] == 'India']

# Report 1: Comparison Between Cities in India
fig_cities = px.bar(
    india_df.groupby('City').size().reset_index(),
    x='City', y=0, title='Number of Restaurants per City',
    color_discrete_sequence=px.colors.qualitative.Plotly  # Change color scheme
)
fig_cities.update_traces(texttemplate='%{y}', textposition='outside')  # Add labels

# Report 2: Online Delivery Expenses in Different Cities
fig_online_delivery = px.bar(
    india_df.groupby(['City', 'Online Delivery']).size().reset_index(),
    x='City', y=0, color='Online Delivery',
    title='Online Delivery Expenses in Different Cities',
    color_discrete_sequence=px.colors.qualitative.Plotly
)
fig_online_delivery.update_traces(texttemplate='%{y}', textposition='outside')

# Report 3: Dine-In Expenses in Different Cities
fig_dine_in = px.bar(
    india_df.groupby(['City', 'Accepts_Table_Booking']).size().reset_index(),
    x='City', y=0, color='Accepts_Table_Booking',
    title='Dine-In Expenses in Different Cities',
    color_discrete_sequence=px.colors.qualitative.Plotly
)
fig_dine_in.update_traces(texttemplate='%{y}', textposition='outside')

# Report 4: High Living Cost vs. Low Living Cost
fig_cost_cities = px.bar(
    india_df.groupby('City')['Avg_Cost'].mean().reset_index(),
    x='City', y='Avg_Cost',
    title='Average Cost for Two in Different Cities',
    color_discrete_sequence=px.colors.qualitative.Plotly
)
fig_cost_cities.update_traces(texttemplate='%{y:.2f}', textposition='outside')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1('Restaurant Dashboard', style={'textAlign': 'center', 'backgroundColor': '#f0f0f0', 'padding': '10px'}),

    # Report 1
    html.Div([
        dcc.Graph(figure=fig_cities)
    ], style={'width': '100%', 'display': 'block', 'border': '2px solid #2c3e50', 'backgroundColor': '#ecf0f1', 'padding': '20px', 'margin': '10px'}),

    # Report 2
    html.Div([
        dcc.Graph(figure=fig_online_delivery)
    ], style={'width': '100%', 'display': 'block', 'border': '2px solid #2c3e50', 'backgroundColor': '#ecf0f1', 'padding': '20px', 'margin': '10px'}),

    # Report 3
    html.Div([
        dcc.Graph(figure=fig_dine_in)
    ], style={'width': '100%', 'display': 'block', 'border': '2px solid #2c3e50', 'backgroundColor': '#ecf0f1', 'padding': '20px', 'margin': '10px'}),

    # Report 4
    html.Div([
        dcc.Graph(figure=fig_cost_cities)
    ], style={'width': '100%', 'display': 'block', 'border': '2px solid #2c3e50', 'backgroundColor': '#ecf0f1', 'padding': '20px', 'margin': '10px'}),
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
