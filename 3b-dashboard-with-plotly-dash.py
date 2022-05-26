#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 22 20:53:07 2022

@author: duyentran
"""

# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px


url = '/Users/duyentran/My stuff/2022/Datacamp/IBM Data Science/10. Applied Data Science Capstone/3. Interactive Visual Analytics and Dashboard/3. spacex_launch_dash.csv'
spacex_df = pd.read_csv(url, header = 0)


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
spacex_df['class'] = spacex_df['class'].apply(str)
spacex_df['launches'] = 1
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                    options = [
                                        {'label': 'All sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'VAFB FLC-4E', 'value': 'VAFB FLC-4E'}
                                    ],
                                    value = 'ALL',
                                    placeholder = "place holder here",
                                    searchable = True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                       2500: '2500',
                                                       5000: '5000',
                                                       7500: '7500',
                                                       10000: '10000'},
                                                value=[min_payload, max_payload]
                                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

# return the outcomes piechart for a selected site
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['class']=='1']
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Success rate for all launch sites')
        return fig
    elif entered_site == 'CCAFS LC-40':
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'CCAFS LC-40']
        fig = px.pie(filtered_df, values='launches', 
        names='class',
        title='Success rate for site: CCAFS LC-40')
        return fig
    elif entered_site == 'CCAFS SLC-40':
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'CCAFS SLC-40']
        fig = px.pie(filtered_df, values='launches', 
        names='class',
        title='Success rate for site: CCAFS SLC-40')
        return fig
    elif entered_site == 'KSC LC-39A':
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'KSC LC-39A']
        fig = px.pie(filtered_df, values='launches', 
        names='class',
        title='Success rate for site: KSC LC-39A')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'VAFB SLC-4E']
        fig = px.pie(filtered_df, values='launches', 
        names='class', 
        title='Success rate for site: VAFB SLC-4E')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
             [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value")])
def get_scatter_plot(entered_site,value):
    if entered_site == 'ALL':
        filtered_df = spacex_df
        filtered_df = filtered_df[filtered_df['Payload Mass (kg)']>=value[0]]
        filtered_df = filtered_df[filtered_df['Payload Mass (kg)']<=value[1]]
        scatter_fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
        color='Booster Version Category', 
        title='All launch site')
        return scatter_fig
    elif entered_site == 'CCAFS LC-40':
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'CCAFS LC-40']
        filtered_df = filtered_df[filtered_df['Payload Mass (kg)']>=value[0]]
        filtered_df = filtered_df[filtered_df['Payload Mass (kg)']<=value[1]]
        scatter_fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
        color='Booster Version Category', 
        title='Launch site CCAFS LC-40')
        return scatter_fig
    elif entered_site == 'CCAFS SLC-40':
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'CCAFS SLC-40']
        filtered_df = filtered_df[filtered_df['Payload Mass (kg)']>=value[0]]
        filtered_df = filtered_df[filtered_df['Payload Mass (kg)']<=value[1]]
        scatter_fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
        color='Booster Version Category', 
        title='Launch site CCAFS SLC-40')
        return scatter_fig
    elif entered_site == 'KSC LC-39A':
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'KSC LC-39A']
        filtered_df = filtered_df[filtered_df['Payload Mass (kg)']>=value[0]]
        filtered_df = filtered_df[filtered_df['Payload Mass (kg)']<=value[1]]
        scatter_fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
        color='Booster Version Category', 
        title='Launch site KSC LC-39A')
        return scatter_fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'VAFB SLC-4E']
        filtered_df = filtered_df[filtered_df['Payload Mass (kg)']>=value[0]]
        filtered_df = filtered_df[filtered_df['Payload Mass (kg)']<=value[1]]
        scatter_fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
        color='Booster Version Category', 
        title='Launch site VAFB SLC-4E')
        return scatter_fig                      

# Run the app
if __name__ == '__main__':
    app.run_server()

                   


















