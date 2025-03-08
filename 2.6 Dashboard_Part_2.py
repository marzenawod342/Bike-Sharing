################################################ CITI BIKE DASHABOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image
import seaborn as sns


########################### Initial settings for the dashboard ##################################################################

st.set_page_config(page_title = 'Optimizing Citi Bike Distribution in NYC', layout='wide')
st.title("Citi Bikes Strategy Dashboard")

# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Intro page","Weather component and bike usage",
   "Most popular stations",
    "Interactive map with aggregated bike trips", "Classic vs. Electric Bikes", "Recommendations"])

########################## Import data ###########################################################################################

df = pd.read_csv('reduced_data_to_plot.csv', index_col = 0)
top20 = pd.read_csv('top20.csv', index_col = 0)


######################################### DEFINE THE PAGES #####################################################################


### INTRO PAGE

if page == "Intro page":
    st.markdown("#### The ultimate goal of this dashboard is to optimize the current bike distribution model, resolve availability issues, and identify opportunities for expansion.")
    st.markdown("Since its beginning in 2013, Citi Bike has grown into one of the most popular bike-sharing services, celebrated for promoting sustainable urban mobility. However, the surge in demand—especially post-Covid-19—has brought challenges in maintaining balanced bike availability across stations. Popular stations often face shortages, while others remain underutilized, leading to inefficiencies and customer dissatisfaction. The dashboard is separated into 4 sections:")
    st.markdown("- Most popular stations")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Classic vs. Electric Bikes")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis I looked at.")

    myImage = Image.open("Citi_bike.jpg") #source: https://www.freepik.com/vectors/citi-bikes
    st.image(myImage)

### LINE CHART PAGE: WEATHER COMPONENT AND BIKE USAGE

    
elif page == 'Weather component and bike usage':
    # Convert 'date' column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Create a sample data
    df_sample = df.resample('1D', on='date').mean(numeric_only=True).reset_index()
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
    st.markdown("The number of daily bike rides increases as temperatures rise, particularly during the warmer months (May to September). Conversely, colder months (November to February) show a decline in both temperature and ride counts, indicating a strong seasonal influence on bike usage.")
    st.markdown("The graph reveals distinct peaks in bike rides during the summer, when temperatures are around 20–30°C, and sharp declines in winter, especially when temperatures drop below 0°C. This suggests that weather conditions significantly impact ridership patterns.")
    st.markdown("While temperatures have a smoother trend throughout the year, bike ride counts show more variability, with noticeable fluctuations even within warm periods. This could point to additional factors, such as special events, weekdays vs. weekends, or sudden weather changes, influencing daily usage.")



### BAR CHART PAGE: MOST POPULAR STATIONS

    # Create the season variable
elif page == 'Most popular stations':
    
    # Create the filter on the side bar
    with st.sidebar:
        season_filter = st.multiselect(label= 'Select the season', options=df['season'].unique(),
    default=df['season'].unique())

    df1 = df.query('season == @season_filter')
    
    # Define the total rides
    total_rides = float(df1['bike_rides_daily'].count())    
    st.metric(label = 'Total Bike Rides', value= numerize(total_rides))
    
    # Bar chart
    df1['value'] = 1 
    df_groupby_bar = df1.groupby('start_station_name', as_index = False).agg({'value': 'sum'})
    top20 = df_groupby_bar.nlargest(20, 'value')
    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value']))

    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color':top20['value'],'colorscale': 'Blues'}))
    fig.update_layout(
    title = 'Top 20 most popular bike stations in New York',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 900, height = 600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("The station West St & Chambers St ranks as the busiest, highlighting a concentrated demand in certain key areas of New York City. This insight is critical for ensuring adequate bike availability and maintenance there. A stark difference in trip counts between top and lower-performing stations suggests an uneven usage pattern. This could indicate opportunities to optimize underused stations or improve connectivity in those areas.This is a finding that we could cross reference with the interactive map that you can access through the side bar select box.")


    
### MAP PAGE: INTERACTIVE MAP WITH AGGREGATED BIKE TRIPS

elif page == 'Interactive map with aggregated bike trips': 

    ### Create the map ###
    st.write("Interactive map showing aggregated bike trips over New York in 2022")

    path_to_html = "Citi_bikes_map.html" 

    # Read file and keep in variable
    with open(path_to_html,'r') as f: 
        html_data = f.read()

    ## Show in webpage
    st.header("Aggregated Bike Trips in New York")
    st.components.v1.html(html_data,height=1000)
    st.markdown("#### Using the filter on the left hand side of the map we can check whether the most popular start stations also appear in the most popular trips.")
    st.markdown("The most popular start stations are: West St & Chambers St, W 21 St & 6 Ave, and Broadway & W 58 St.")
    st.markdown("While we can see that even though Broadway & W 58 St. has a high number of trips, it doesn't seem to be a popular start or end station for multiple routes.")
    st.markdown("Based on the map, the most popular areas/stations appear to be:")
    st.markdown("1. Midtown and Lower Manhattan: 5 Ave & E 72 St")
    st.markdown("2. Hudson River Vicinity (Western Manhattan): 12 Ave & W 40 St and W 22 St & 10 Ave")


### HISTOGRAMS: CLASSIC VERSUS ELECTRIC BIKES

elif page == 'Classic vs. Electric Bikes' :

    # Create subsets for each bike type
    classic_bike = df[df['rideable_type'] == 'classic_bike']
    electric_bike = df[df['rideable_type'] == 'electric_bike']

    # Create two separate plots
    st.subheader("Bike Rentals by Temperature")

    fig1, ax1 = plt.subplots()
    sns.histplot(classic_bike['avgTemp'], kde=True, color='blue', ax=ax1)
    ax1.set_title('Classic Bike Rentals')
    ax1.set_xlabel('Average Temperature')

    fig2, ax2 = plt.subplots()
    sns.histplot(electric_bike['avgTemp'], kde=True, color='orange', ax=ax2)
    ax2.set_title('Electric Bike Rentals')
    ax2.set_xlabel('Average Temperature')

    col1, col2 = st.columns(2)

    with col1:
        st.pyplot(fig1)  # Smaller chart in one column

    with col2:
        st.pyplot(fig2)  # Smaller chart in another column


    st.markdown("Insights:")
    st.markdown("1. Both classic and electric bike rentals increase significantly as temperatures rise from below 0°C to around 20°C. This highlights the influence of weather conditions on bike usage.")
    st.markdown("2. Classic bikes are rented most frequently around 20°C, while electric bikes peak slightly above 20°C. This suggests that both types of bikes are favored in moderate weather, with electric bikes having a slight edge in warmer conditions.")
    st.markdown("3. The maximum rental count for classic bikes exceeds 10,000, whereas the peak for electric bikes is slightly above 6,000. This indicates that classic bikes remain the more popular option overall, potentially due to affordability or greater availability.")
                
                
### CONCLUSIONS PAGE: RECOMMENDATIONS
                
else:
    
    st.header("Conclusions and recommendations")
    bikes = Image.open("recs.jpg")  #https://unsplash.com/s/photos/citi-bike
    st.image(bikes)
    st.markdown("### My analysis has shown that Citi Bikes should focus on the following objectives moving forward:")
    st.markdown("- Add more stations to the locations around the Hudson River, Manhattan and Central Park as these seem to be the most popular areas.")
    st.markdown("- Improve connectivity of the stations that are heavily used as starting points but not destinations or vice versa such as Broadway & W 58 St. with other locations.") 
    st.markdown("- Ensure that bikes are fully stocked in all these stations during the warmer months in order to meet the higher demand, but provide a lower supply in winter and late fall to reduce logistics costs")
    st.markdown("- Consider adding electric bikes incrementally in high-demand zones and monitor usage trends or ensure the current electric bikes are being effectively redistributed across popular stations to meet demand")
