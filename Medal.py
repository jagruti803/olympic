import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
from pathlib import Path
import sys,os
from HandleGPT import GPTHandler


# Function to load CSV file and process data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

# Function to filter data by country and year
def filter_data(df, country, year):
    if year == "Overall":
        filtered_df = df[df['Country'] == country]
    elif country == "Overall":
        filtered_df = df[df['Year'] == int(year)]
    else:
        filtered_df = df[(df['Country'] == country) & (df['Year'] == int(year))]
    return filtered_df

def display_results(df):
    gold = df['Gold'].sum()
    silver = df['Silver'].sum()
    bronze = df['Bronze'].sum()
    total_medals = gold + silver + bronze


    results_df = pd.DataFrame({
        'Medal': ['Gold', 'Silver', 'Bronze', 'Total'],
        'Count': [gold, silver, bronze, total_medals]
    })

    # Display results in a table format
    st.subheader(":blue[Medal Tally]")
    st.divider()
    st.table(results_df.style.set_table_styles([
        {'selector': 'th', 'props': [('font-size', '25px'), ('font-family', 'Arial, sans-serif'),('font-weight', 'bold'),('border', '2px solid #000000')]},  # Header style
        {'selector': 'td', 'props': [('font-size', '20px'), ('font-family', 'Arial, sans-serif'),('font-weight', 'bold'),('border', '2px solid #000000')]},
        {'selector': 'table', 'props': [('border-collapse', 'collapse')]},  # Cell style
    ]))
    st.subheader(":green[Our Olympic medal analysis platform! We're dedicated to providing straightforward insights into Olympic medal standings. With easy-to-understand graphs, we highlight the performances of the top five countries across various Olympic years. Whether you're interested in gold, silver, bronze, or total medal counts, our platform offers a clear visual representation of each country's achievements on the Olympic stage. Explore the data effortlessly and gain a deeper understanding of the most successful nations in Olympic history.]")
    st.divider()
    st.subheader(":black[For this analysis, please choose the 'Overall' option in the 'Country' section and select any year from the dropdown menu in the 'year' section.]")
    st.divider()
    st.subheader(":blue[Top 5 Countries with Total Medals]")
    st.divider()
    top_5_df = df.groupby('Country').sum().sort_values(by='Total', ascending=False).head(5)
    fig = px.bar(top_5_df, x=top_5_df.index, y='Total', labels={'x': 'Country', 'y': 'Total Medals'})
    # Customize bar appearance
    fig.update_traces(marker_color=['gold', 'silver', 'brown', 'orange', 'lightblue'],  # Change bar colors
                  marker_line_width=3,  # Adjust bar width
                  opacity=1)  # Adjust bar opacity

# Adjust layout
    fig.update_layout(bargap=0.3,  # Adjust gap between bars
                  height=500,  # Adjust plot height
                  xaxis=dict(tickfont=dict(size=20,color='green'),title=dict(text='Country', font=dict(size=20, color='green'))),  # Increase x-axis label size
                  yaxis=dict(tickfont=dict(size=20),showgrid=False, zeroline=False, showticklabels=False))  # Increase y-axis label size
    
    st.plotly_chart(fig)
    
    # Line chart for performance over the last five years
    st.subheader(":green[Our app provides insightful analysis of a particular country's performance over the last five years. By examining key metrics such as medal counts, participation rates, and trends over time, we offer valuable insights into the country's achievements and areas for improvement in various sporting events.]")
    st.divider()
    st.subheader(":black[For this analysis, please choose the 'Overall' option in the 'Year' section and select any country from the dropdown menu in the 'Country' section.]")
    st.divider()
    st.subheader(":blue[Performance over the Last Five Years]")
    st.divider()
    line_chart_data = df.groupby('Year').sum().tail(5)
    line_chart_fig = px.line(line_chart_data, x=line_chart_data.index, y='Total')
    line_chart_fig.update_traces(line=dict(color='red', width=3))  # Change line color to red and increase width
    line_chart_fig.update_layout(xaxis=dict(tickmode='linear', tickfont=dict(size=20,color='green'),tickvals=line_chart_data.index[-5:], ticktext=line_chart_data.index[-5:],title=dict(text="Year", font=dict(size=25, color='green'))),  # Display only five years on x-axis
                                  yaxis=dict(visible=False),  # Remove y-axis
                                  xaxis_title="Year",  # Set x-axis label
                                  yaxis_title="Total Medals",  # Set y-axis label
                                  xaxis_showgrid=False,  # Remove x-axis gridlines
                                  yaxis_showgrid=False)  # Remove y-axis gridlines
    
    st.plotly_chart(line_chart_fig)

def main():
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
    
    _root_dir_ = Path(__file__).absolute().parent
    
    
    # Displaying the styled title
    st.markdown("<p class='title'>Olympic Data Analysis</p>", unsafe_allow_html=True)
    

    st.sidebar.image('Olympics-Symbol.png')
    st.image("medal img.png")
    st.sidebar.header(':black[Medal Tally]')
    gpt_handler = GPTHandler()
    gpt_model = gpt_handler.load_gpt_model()
    

    st.subheader(":blue[Olympic Medals Analysis]")
    st.divider()
    st.subheader(':green[Our website provides comprehensive Olympic medal analysis, allowing users to explore medal counts for specific countries and years. Users can select any year, with data available from all Olympic events up to the most recent Games held in 2020. Additionally, due to the impact of COVID-19, certain events were postponed to 2022, and our analysis covers all the correct information for those years as well.]')
    st.divider()
    # Load CSV file from predefined path or URL
    file_path = "Olympic_Games_Medal_Tally1.csv"
    df = load_data(file_path)

    
    countries = df['Country'].unique()
    countries = ['Overall'] + sorted(countries)
    years = sorted(df['Year'].unique())
    years = ['Overall'] + years


    # Select country and year
    st.sidebar.header(":blue[Select Country]")
    country = st.sidebar.selectbox("", countries)
    st.sidebar.header(":blue[Select Year]")
    year = st.sidebar.selectbox("", years)

    # Filter data based on selection
    filtered_df = filter_data(df, country, year)

    # Display analysis results
    countries = df['Country'].unique()
    st.subheader(f":blue[Analysis for {country} in {year}]")
    display_results(filtered_df)


    

if __name__ == "__main__":
    main()


