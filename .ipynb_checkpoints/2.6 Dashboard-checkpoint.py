################################################ DIVVY BIKES DASHABOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt


########################### Initial settings for the dashboard ##################################################################


st.set_page_config(page_title = 'Citi Bikes Strategy Dashboard', layout='wide')
st.title("Citi Bikes Strategy Dashboard")
st.markdown("The dashboard will help with the expansion problems Citi currently faces")
st.markdown("Right now, Citi bikes runs into a situation where customers complain about bikes not being avaibale at certain times. This analysis aims to look at the potential reasons behind this.")

########################## Import data ###########################################################################################

df = pd.read_csv('reduced_data_to_plot.csv', index_col = 0)
top20 = pd.read_csv('top20.csv', index_col = 0)

# ######################################### DEFINE THE CHARTS #####################################################################

## Bar chart

fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color': top20['value'],'colorscale': 'Blues'}))
fig.update_layout(
    title = 'Top 20 most popular bike stations in New York',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 1200, height = 700
)
st.plotly_chart(fig, use_container_width=True)

## Line chart 

# Convert 'date' column to datetime
df['date'] = pd.to_datetime(df['date'])

# Create a sample data
df_sample = df.resample('1D', on='date').mean().reset_index()

# Line chart with dual y-axes
fig_2= make_subplots(specs=[[{"secondary_y": True}]])

fig_2.add_trace(
    go.Scatter(x=df_sample['date'], y=df_sample['bike_rides_daily'], name='Daily Bike Rides',
               line=dict(color='blue', width=2), opacity=0.7),
    secondary_y=False
)

fig_2.add_trace(
    go.Scatter(x=df_sample['date'], y=df_sample['avgTemp'], name='Daily Temperatures',
               line=dict(color='red', width=2), opacity=0.7),
    secondary_y=True
)

# Add figure title
fig_2.update_layout(
    title_text="Daily Bike Rides and Temperatures"
)

# Set x-axis title
fig_2.update_xaxes(title_text="Date", showgrid=True)

# Set y-axes titles
fig_2.update_yaxes(title_text="Bike Rides", secondary_y=False, showgrid=True)
fig_2.update_yaxes(title_text="Temperature (°C)", secondary_y=True)


st.plotly_chart(fig_2, use_container_width=True)



### Add the map ###

path_to_html = "Citi Bikes map.html" 

# Read file and keep in variable
with open(path_to_html,'r') as f: 
    html_data = f.read()

## Show in webpage
st.header("Aggregated Bike Trips in New York")
st.components.v1.html(html_data,height=1000)