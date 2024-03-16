import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
from pathlib import Path
import sys,os
from HandleGPT import GPTHandler

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

gpt_handler = GPTHandler()
gpt_model = gpt_handler.load_gpt_model()

#Load Data
@st.cache_data
def load_data(data_path):
    df = pd.read_csv(os.path.join(data_path, 'Olympic_Games_Medal_Tally1.csv'))


    return df



#getting path of script
_root_dir_ = Path(__file__).absolute().parent.parent

#load datd frame
medal_df = load_data(_root_dir_)
import pandas as pd

#medal_df.rename(columns={'old_name': 'new_name'}, inplace=True)
medal_df.rename(columns={'Year': 'year'}, inplace=True)
medal_df.rename(columns={'Country': 'country'}, inplace=True)

#st.write(medal_df.head())


#Setup session state 
if 'filtered_df' not in st.session_state:
    st.session_state.filtered_df = medal_df.copy(deep=True)

if 'country' not in st.session_state:
    st.session_state.country = 'United States'

if 'country_noc' not in st.session_state:
    st.session_state.country_noc = 'USA'


if 'year' not in st.session_state:
    st.session_state.year = 2020
    

if 'response_value' not in st.session_state:
    st.session_state.response_value = { 'country' : ['United States'],'year':[2020] , 'country_noc':'USA'}

if 'query_value' not in st.session_state:
    st.session_state.query_value = ''




countries = sorted(medal_df['country'].unique())
#countries = ['All'] + sorted(countries)

years = sorted(medal_df['year'].unique())
default_ix = years.index(2020)
#years = [''] + years


# Function to filter data by country and year
# def filter_data(df, country, year):
#     if year == "Overall":
#         filtered_df = df[df['Country'] == country]
#     elif country == "Overall":
#         filtered_df = df[df['Year'] == int(year)]
#     else:
#         filtered_df = df[(df['Country'] == country) & (df['Year'] == int(year))]
#     return filtered_df

def draw_sidebar():
    #add sidebar

    with st.sidebar:
        # Select country and year
        st.sidebar.header("Select Country")
        select_country = st.sidebar.multiselect("", countries,default = st.session_state.get('country'))
        country_codes    = medal_df[medal_df['country'].isin(select_country)]['country_noc'].unique()
        #st.write(country_codes)

        st.sidebar.header("Select Year")

        year = st.sidebar.selectbox("Select Year", years,index = default_ix)

        st.session_state.response_value['country'] = list(map(str.lower,select_country))
        st.session_state.response_value['country_noc'] = list(map(str.lower,country_codes))

        #st.write('Country')
        #st.write(st.session_state.response_value['country'])

        st.session_state.response_value['year'] = int(year)
        #st.write(st.session_state.response_value['year'])

        #st.write(st.session_state.response_value)



        st.session_state.filtered_df = refresh_response(st.session_state.response_value,medal_df)
        return st.session_state.filtered_df

        




def refresh_response(response,df):
    
    key = ['year','country_noc']
    filtered_df = gpt_handler.apply_filter(key,response,df)

    #st.write(filtered_df)
    return(filtered_df)
        

def display_results(df):
    #Display results in a table format
    st.subheader(":blue[Medal Tally]")
    st.divider()
    st.table(df[['country','year','Gold','Silver','Bronze','Total']].set_index('country', drop=True).style.set_table_styles
             ([
        {'selector': 'th', 'props': [('font-size', '25px'), ('font-family', 'Arial, sans-serif'),('font-weight', 'bold'),('border', '2px solid #000000')]},  # Header style
        {'selector': 'td', 'props': [('font-size', '20px'), ('font-family', 'Arial, sans-serif'),('font-weight', 'bold'),('border', '2px solid #000000')]},
        {'selector': 'table', 'props': [('border-collapse', 'collapse')]},  # Cell style
    ]))

    
   
#     #st.subheader(":green[Our Olympic medal analysis platform! We're dedicated to providing straightforward insights into Olympic medal standings. With easy-to-understand graphs, we highlight the performances of the top five countries across various Olympic years. Whether you're interested in gold, silver, bronze, or total medal counts, our platform offers a clear visual representation of each country's achievements on the Olympic stage. Explore the data effortlessly and gain a deeper understanding of the most successful nations in Olympic history.]")
#   
      #st.subheader(":black[For this analysis, please choose the 'Overall' option in the 'Country' section and select any year from the dropdown menu in the 'year' section.]")
    st.divider()
    st.subheader(":blue[Countries with Total Medals]")

    fig = px.bar(df, x='country', y='Total', labels={'x': 'Country', 'y': 'Total Medals'})
#     # Customize bar appearance

    fig.update_traces(marker_color=['gold', 'silver', 'brown', 'orange', 'lightblue'],  # Change bar colors
                   marker_line_width=3,  # Adjust bar width
                   opacity=1)  # Adjust bar opacity

# # Adjust layout
    fig.update_layout(bargap=0.3,  # Adjust gap between bars
                   height=500,  # Adjust plot height
                   xaxis=dict(tickfont=dict(size=20,color='green'),title=dict(text='Country', font=dict(size=20, color='green'))),  # Increase x-axis label size
                   yaxis=dict(tickfont=dict(size=20),showgrid=False, zeroline=False, showticklabels=False))  # Increase y-axis label size
    st.plotly_chart(fig)
    
     # Line chart for performance over the last five years
    #st.subheader(":green[Our app provides insightful analysis of a particular country's performance over the last five years. By examining key metrics such as medal counts, participation rates, and trends over time, we offer valuable insights into the country's achievements and areas for improvement in various sporting events.]")
    #st.subheader(":black[For this analysis, please choose the 'Overall' option in the 'Year' section and select any country from the dropdown menu in the 'Country' section.]")
    #st.subheader(":green[Performance over the Last Five Years]")
    
    fig1 = px.pie(df,values = 'Total',names='country')
    st.divider()
    st.subheader(":blue[Medal % won by selected countries]")
    st.plotly_chart(fig1)






#st.write(_root_dir_)

    # Displaying the styled title
st.markdown("<p class='title'>Olympic Analysis Using ChatGPT</p>", unsafe_allow_html=True)
st.sidebar.image('Olympics-Symbol.png')
#st.image("medal img.png")

with st.container():
    st.write('_________________________________________________________________')
    query = st.text_area(label= 'GPT Enabled - Ask Me',value = st.session_state.get('query_value')
                         ,placeholder = 'show me medal won by India in 2020',height = 11)
    
    result = st.button('Run')

    if result:
        st.write("Button value : ",result)
        input_text = query
        st.session_state.response_value = gpt_handler.get_gpt_response(gpt_model,input_text)
        st.session_state.response_value = gpt_handler.preprocess_response(st.session_state.response_value) #text clear and dictionary preprocess
        st.session_state.country = st.session_state.response_value['country']
        st.session_state.filtered_df = refresh_response(st.session_state.response_value,medal_df) #refresh the filters


        #update filters as per the response
        st.session_state.country = st.session_state.filtered_df['country'].unique().tolist()
        st.session_state.year = st.session_state.filtered_df['year']
        st.session_state.country_noc = st.session_state.filtered_df['country_noc']
        st.experimental_rerun() # run double click 


        

    st.session_state.filtered_df = draw_sidebar()


    




# Display analysis results
#st.subheader(f":green[Analysis for {st.session_state.country} in {st.session_state.response_value['year']}]")
heading_country = st.session_state.country

if isinstance(heading_country, list):
    countries_str = ", ".join(heading_country)
else:
    countries_str = heading_country

st.subheader(f":blue[Analysis for {countries_str} in {st.session_state.response_value['year']}]")
#st.write(st.session_state.filtered_df)
display_results(st.session_state.filtered_df)



