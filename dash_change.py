import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import math
from PIL import Image
import streamlit.components.v1 as components
import base64
import geopandas as gpd
from plotly.subplots import make_subplots
import json


#Adds favicon to the website and set page title 
favicon_image = Image.open('ashoka.jpeg')
st.set_page_config(page_title="Previous Election Insights", page_icon=favicon_image, layout="wide")

#To hide hamburger menu

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

#To reduce padding between containers in the application
padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

st.markdown("<div id='Backtotop'></div>", unsafe_allow_html=True) 

def local_html(file_name):
    with open(file_name) as f:
        st.markdown('{}'.format(f.read()), unsafe_allow_html=True)

local_html("new_landing.html")
st.markdown("""<hr/>""", unsafe_allow_html=True)



#GeoJSON
with open('./India_States.geojson') as f:
    gj = json.load(f)
    
@st.cache
def map(df,df_1,x,title_fig='', legend_show=True):
    
    fig = px.choropleth(df_1, geojson=gj, locations='ST_NM', color='Value',
                               featureidkey="properties.ST_NM",
                               color_discrete_sequence=["rgb(211,211,211)"],
                                                             
                              )
    fig.add_trace(go.Choropleth(featureidkey='properties.ST_NM',
                                  geojson=gj,
                                  locations=df['State_Name'],
                                  z=df["{}".format(x)],
                                  colorscale=[[0, 'rgb(255, 229, 180)'], [1, 'rgb(248, 131, 121)']],
                                  #colorscale='viridis',
                                  showscale=legend_show                      
                                 ))
  

    fig.update_geos(projection_type="van der grinten", fitbounds="locations", visible=False)
    fig.update_layout(autosize=False,title={'text': "{}".format(title_fig),
        'x':0.465,
        'y':0,
        'xanchor': 'center',
        'yanchor': 'bottom'},
         margin=dict(l=0, r=0, t=0, b=0, autoexpand=True),showlegend=False, height=800)
    fig.update_xaxes(mirror=True, showline=True)
    fig.update_coloraxes(cauto=False, cmin=0, cmax=100)

    return(fig)


#To create base map
df_null= pd.read_csv("./states_shapefile_name.csv",dtype={"State": str})

csv = st.cache(suppress_st_warning=True, allow_output_mutation=True)(pd.read_csv)

#Voter Turnout
st.markdown("<div id='1'></div>", unsafe_allow_html=True) 

st.markdown("""<div style="text-align:center;"><h2>Voter Turnout</h2></div>""", unsafe_allow_html=True) 

voter_container=st.container()
voter=pd.read_csv('./data/voter.csv')

config = dict({'scrollZoom': False})
#voter_2.plotly_chart(map(voter,df_null,'Percentage','',True), use_container_width=True,**{'config': config})

def local_html(file_name):
    with open(file_name) as f:
        st.markdown('{}'.format(f.read()), unsafe_allow_html=True)

local_html("voter.html")

st.markdown("""<div style="text-align:right;"><a href=#Backtotop>Back to top</a><div>""", unsafe_allow_html=True)


st.markdown("""<hr/>""", unsafe_allow_html=True)


#Constituencies percentage
st.markdown("<div id='2'></div>", unsafe_allow_html=True) 

st.markdown("""<div style="text-align:center;"><h2>Constituencies</h2></div>""", unsafe_allow_html=True) 

constituencies=pd.read_csv('./data/constituencies.csv')
constituencies['Percentage']=np.nan
constituencies['Percentage']=round(constituencies['count_i']*100/ constituencies['total'], 2)

constituencies['Constituency_Type']=constituencies['Constituency_Type'].mask(constituencies['Constituency_Type']=='GEN','General')
constituencies['Constituency_Type']=constituencies['Constituency_Type'].mask(constituencies['Constituency_Type']=='SC','Scheduled Caste')
constituencies['Constituency_Type']=constituencies['Constituency_Type'].mask(constituencies['Constituency_Type']=='ST','Scheduled Tribe')

fig = px.bar(constituencies, x="State_Name", y="Percentage",
             color='Constituency_Type', barmode='group',
             height=400, hover_name="Constituency_Type", hover_data={"count_i":True, "total":True, "Constituency_Type":False,"State_Name":False}, 
             labels = {"count_i":"Category_Constituencies","total":"Total_Constituencies", "type":"", "per":"Percentage"}, 
             color_discrete_map={
             'General': 'lightgreen',
              'Scheduled Caste': 'yellow',
                 'Scheduled Tribe':'green'}
            )

fig.update_layout(hovermode=None, plot_bgcolor="White", legend=dict(
    yanchor="bottom",
    y=0.99,
    xanchor="right",
    x=0.99
))

fig.update_xaxes(showline=True, linewidth=1, linecolor='grey')
fig.update_yaxes(showline=True, linewidth=1, linecolor='grey')


const_bar_container=st.container()
const_bar_1,const_bar_2, const_bar_3=const_bar_container.columns([0.5,3,0.5])
const_bar_2.plotly_chart(fig,use_container_width=True)

st.markdown("""<div style="text-align:right;"><a href=#Backtotop>Back to top</a><div>""", unsafe_allow_html=True)

st.markdown("""<hr/>""", unsafe_allow_html=True)


#Women Winner and Contestant

st.markdown("<div id='3'></div>", unsafe_allow_html=True) 

st.markdown("""<div style="text-align:center;"><h2>Women Winner and Contestants</h2></div>""", unsafe_allow_html=True) 

women_container=st.container()
women_1,women_2, women_3=women_container.columns([0.5,3,0.5])

contest=pd.read_csv('./data/contestant.csv')
contest['Women Percentage across Contestants']=np.nan
contest['Women Percentage across Contestants']=round(contest['Women']*100/contest['Total'],2)
contest['Women Percentage across Winner']=np.nan
contest['Women Percentage across Winner']=round(contest['Winner']*100/contest['total'],2)
contest.rename({'Total':'total_contestant','Women':'women_contestant','Winner':'women_winner','total':'total_winner'}, axis=1, inplace=True)


c_1=contest.groupby(['State_Name','Assembly_No','total_contestant','women_contestant'])['Women Percentage across Contestants'].unique().reset_index().explode('Women Percentage across Contestants')
c_1['type']='Women Percentage across Contestants'
c_1.rename({'Women Percentage across Contestants':'per'}, axis=1, inplace=True)

c_2=contest.groupby(['State_Name','Assembly_No','women_winner','total_winner'])['Women Percentage across Winner'].unique().reset_index().explode('Women Percentage across Winner')
c_2['type']='Women Percentage across Winner'
c_2.rename({'Women Percentage across Winner':'per'}, axis=1, inplace=True)

c=c_2.append(c_1)

c['winner']=np.nan
c['winner']=c['winner'].mask( (c['women_winner'].isna()==True), c['women_contestant'])
c['winner']=c['winner'].mask( (c['women_winner'].isna()==False), c['women_winner'])
c['contestant']=np.nan
c['contestant']=c['contestant'].mask( (c['total_contestant'].isna()==True), c['total_winner'])
c['contestant']=c['contestant'].mask( (c['total_contestant'].isna()==False), c['total_contestant'])


fig = px.bar(c, x="State_Name", y="per",
             color='type', barmode='group',
             height=400, hover_name="type", hover_data={"winner":True, "contestant":True, "type":False,"State_Name":False}, 
             labels = {"winner":"Women","contestant":"Total", "type":"", "per":"Percentage"}, 
             color_discrete_map={
             'Women Percentage across Winner': 'lightblue',
              'Women Percentage across Contestants': 'purple'
    })

fig.update_layout(hovermode=None, plot_bgcolor="White", legend=dict(
    yanchor="bottom",
    y=0.99,
    xanchor="right",
    x=0.99
))
fig.update_xaxes(showline=True, linewidth=1, linecolor='grey')
fig.update_yaxes(showline=True, linewidth=1, linecolor='grey')



women_2.plotly_chart(fig,use_container_width=True)

st.markdown("""<div style="text-align:right;"><a href=#Backtotop>Back to top</a><div>""", unsafe_allow_html=True)
st.markdown("""<hr/>""", unsafe_allow_html=True)



#Party Seat Share
st.markdown("<div id='4'></div>", unsafe_allow_html=True) 

st.markdown("""<div style="text-align:center;"><h2>Party Seat Share</h2></div>""", unsafe_allow_html=True) 

df_party=csv('./data/party_seat_share.csv')
fig= px.sunburst(df_party, path=['State_Name','Party','Party_Seat_Percentage'], 
                 values='Party_Seat',width=600, height=600, color='State_Name',
                 color_continuous_scale='Tealgrn', custom_data=['State_Name','Party', 'Party_Seat', 'Party_Seat_Percentage']
                )

fig.update_traces(insidetextorientation='radial',  hovertemplate="<br>".join([
        "Seat: %{customdata[2]}"
    ]))

party_seat=st.container()
party_seat_1,party_seat_2,party_seat_3=party_seat.columns([0.5,3,0.5])
party_seat_2.plotly_chart(fig,use_container_width=True)

st.markdown("""<div style="text-align:right;"><a href=#Backtotop>Back to top</a><div>""", unsafe_allow_html=True)
st.markdown("""<hr/>""", unsafe_allow_html=True)



#Party Performance Across States

st.markdown("<div id='5'></div>", unsafe_allow_html=True) 

st.markdown("""<div style="text-align:center;"><h2>Party Seat Share Across State</h2></div>""", unsafe_allow_html=True) 

components.html("""
""", height=10)


components.html("""
<html>
<head>
  
<style>
body {
  height: 800px;  
} 
iframe{
  width:50vw;
}
.flex-container {
  display: flex;
  flex-direction: row;
}

.flex-item-left {
<!--   background-color: #f1f1f1; -->
  flex: 50%;
  align-items: stretch;

}

.flex-item-right {
<!--   background-color: dodgerblue; -->
  flex: 50%;
  align-items: stretch;

}

@media (max-width: 700px) {
  .flex-container {
    flex-direction: column;
  }
 
iframe{
  width:90vw;
}
 
}
</style>
</head>
<body>
<main>

 <div class="flex-container">
   
  <div class="flex-item-left"><iframe title="INC" aria-label="Map" id="datawrapper-chart-kVAmg" src="https://datawrapper.dwcdn.net/kVAmg/2/" scrolling="no" frameborder="0" style="border: none;" width="600" height="754"></iframe></div>
   
  <div class="flex-item-right"><iframe title="BJP" aria-label="Map" id="datawrapper-chart-yg7Zy" src="https://datawrapper.dwcdn.net/yg7Zy/1/" scrolling="no" frameborder="0" style="border: none;" width="600" height="754"></iframe></iframe></div>
  
</div>

</main>
</body>
</html>

""", height=1600)

st.markdown("""<div style="text-align:right;"><a href=#Backtotop>Back to top</a><div>""", unsafe_allow_html=True)




