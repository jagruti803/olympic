import streamlit as st
import pandas as pd

import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

import streamlit as st
import streamlit as st

# Styling the title using Markdown and CSS syntax
st.markdown("""
    <style>
        .title {
            font-size: 50px;
            font-weight: bold;
            text-align: center;
            color:#21E5D0;
            #text-shadow: 2px 2px #008ae6;
        }
    </style>
    """, unsafe_allow_html=True)

# Displaying the styled title
st.markdown("<p class='title'>Athlete,Sport and Event Analysis</p>", unsafe_allow_html=True)
st.sidebar.image('Olympics-Symbol.png')
st.image("athelete image.png")
#st.sidebar.header(':black[Athlete Tally]',divider='rainbow')

import streamlit as st
import pandas as pd
def format_information_box(content):
    return f"""
    <div style="
        border: 2px solid #000000;
        border-radius: 10px;
        padding: 10px;
        background-color: #CBEDE6;
        color: #000000;  /* Black color */
        font-family: Arial, sans-serif; /* Font family */
        font-size: 80px; /* Font size */
        ">
        {content}
    </div>
    """

# Load the CSV dataset
#@st.cache
def load_data():
    data = pd.read_csv("Olympic_Athlete_Event_Results.csv")
    return data

# Filter athletes who won a medal
def filter_medalists(data):
    medalists = data[data['Medal'].notnull()]
    filtered_medalists = medalists.groupby('Name').filter(lambda x: len(x) > 0)
    return medalists['Name'].unique()

# Filter athlete's entries who won medals
def filter_athlete_medals(data, selected_athlete):
    athlete_medals = data[(data['Name'] == selected_athlete) & (data['Medal'].notnull())]
    return athlete_medals



# Function to filter data based on selected sport and event
def filter_data(data, selected_sport, selected_event):
    if selected_event == "All":
        filtered_data = data[data['Sport'] == selected_sport]
    else:
        filtered_data = data[(data['Sport'] == selected_sport) & (data['Event'] == selected_event)]
    return filtered_data
# Function to get country-wise medal counts
def get_country_medal_counts(data):
    country_medals = data.groupby('NOC')['Medal'].count().reset_index()
    country_medals.rename(columns={'Medal': 'Medal Count'}, inplace=True)
    return country_medals

# Function to get top 5 players with their country and medal counts
def get_top_players(data):
    top_players = data.groupby(['Name', 'Country'])['Medal'].count().reset_index().sort_values(by='Medal', ascending=False).head(5)
    return top_players



# Main function to run the Streamlit app
def main():
    
    
    # Load data
    data = load_data()
    data = pd.DataFrame(data)
    
    # Filter athletes who won a medal
    medalist_names = filter_medalists(data)
    # Sidebar - Option selection

    st.sidebar.header(':blue[Athlete Tally]')
    
    st.sidebar.header("Select Athlete")
    selected_athlete = st.sidebar.selectbox( "",medalist_names)
    
    st.sidebar.header("Select Sport")
    selected_sport = st.sidebar.selectbox("", data['Sport'].unique())

   # Events options
    events_options = data[data['Sport'] == selected_sport]['Event'].unique().tolist()
    events_options.insert(0, "All")  # Inserting "All" option at the beginning

    # Sidebar - Option selection for event
    st.sidebar.header("Select Event")
    selected_event = st.sidebar.selectbox("", events_options)

    # Filter data based on selections
    filtered_data = filter_data(data, selected_sport, selected_event)
    athlete_medals = filter_athlete_medals(data, selected_athlete)
    # Display athlete information
    st.subheader(":blue[Athlete Information]")
    st.divider()
    st.subheader(":white[On our website, you can access athlete information spanning from the 1972 Olympics to the most recent event in 2020. Once you select an athlete's name, you'll receive detailed information about that athlete.]")
    st.divider()
    # Display all medals won by the athlete
    if not athlete_medals.empty:
        st.subheader(f":blue[Medals Won by {selected_athlete}]")
        st.divider()
        st.table(athlete_medals[['Games','Event', 'Medal']])
        total_medals_count = len(athlete_medals)
        #st.write(f"Total Medals Won by {selected_athlete}: {total_medals_count}")
    else:
        st.write("This athlete has not won any Olympic medals.")
   
    
    
    selected_athlete_info = athlete_medals.iloc[0]  # Getting info from the first row since they're all the same athlete
    formatted_content = f"""
    <span style="font-weight: bold;font-size: 25px;">Name of the Athlete: {selected_athlete_info['Name']}. </span><br>
    <span style="font-weight: bold;font-size: 25px;">Wining Country: {selected_athlete_info['Country']}.</span><br>
    <span style="font-weight: bold;font-size: 25px;">Sport Category: {selected_athlete_info['Sport']}</span><br>
    <span style="font-weight: bold;font-size: 25px;">Height of the Athlete in cm: {selected_athlete_info['Height']}</span><br>
    <span style="font-weight: bold;font-size: 25px;">Weight of the Athlete: {selected_athlete_info['Weight']}</span><br>
    <span style="font-weight: bold;font-size: 25px;">Total Medals Won:  {total_medals_count}</span><br>
    """
    
    # Display formatted content inside a rectangular box
    st.markdown(format_information_box(formatted_content), unsafe_allow_html=True)
    st.divider()
     # Display top 5 players with their country and medal counts
    st.subheader(":white[In our analysis, we will identify the top five athletes who have excelled in a specific Olympic sport and its associated event, based on their medal count.]")
    st.divider()
    st.subheader(":blue[Top 5 Players with Country and Medal Counts]")
    st.divider()
    top_players = get_top_players(filtered_data)
    st.table(top_players)
    st.divider()

    st.subheader(":white[Our analysis utilizes map visualization to depict the performance of countries in the Olympic Games across specific sports and their associated events. The color coding on the map illustrates each country's medal count corresponding to the sport and event.]")
    st.divider()
    if selected_event != "All":
        # Visualization - Country-wise medal count for selected event
        st.subheader(f"Country-wise Analysis for {selected_event}")
        country_medals = get_country_medal_counts(filtered_data)
        if not country_medals.empty:
            fig = px.choropleth(country_medals, locations='NOC', color='Medal Count', 
                                hover_name='NOC', color_continuous_scale='Viridis'
                                )
            fig.update_layout(geo=dict(showcoastlines=True))
            fig.update_layout(geo=dict(showcoastlines=True),
                              margin=dict(l=0, r=0, t=40, b=0))  # Adjusting map margins
            fig.update_geos(projection_type="orthographic")
            st.plotly_chart(fig,use_container_width=True)
        else:
            st.write("No data available for the selected sport and event.")
    else:
        # Visualization - Overall country-wise medal count for selected sport
    
        st.subheader(f":blue[Overall Country-wise Analysis for {selected_sport}]")
        country_medals_overall = get_country_medal_counts(filtered_data)
        if not country_medals_overall.empty:
            fig = px.choropleth(country_medals_overall, locations='NOC', color='Medal Count', 
                                hover_name='NOC', color_continuous_scale='Viridis'
                                )
            fig.update_layout(geo=dict(showcoastlines=True))
            fig.update_layout(geo=dict(showcoastlines=True),
                              margin=dict(l=0, r=0, t=40, b=0))  
            fig.update_layout(geo=dict(showcoastlines=True))
            st.plotly_chart(fig,use_container_width=True)
        else:
            st.write("No data available for the selected sport.")


if __name__ == "__main__":
    main()


