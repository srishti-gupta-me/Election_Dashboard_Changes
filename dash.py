import streamlit as st
import pandas as pd
import numpy as np
from plotly.tools import FigureFactory as ff
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import math
from PIL import Image
import streamlit.components.v1 as components
import base64

favicon_image = Image.open('ashoka.jpeg')
st.set_page_config(page_title="Previous Election Insights", page_icon=favicon_image, layout="wide")

# landing_container=st.container()
# land_col1,land_col2,land_col3=landing_container.columns([1,8,1])

components.html("""<html>
<style>

body {
  height: 800px;  
  background-image:url("https://github.com/srishti-gupta-me/Election_Dashboard/blob/main/initial_bg.png?raw=true");
  background-repeat: no-repeat;
  background-position: center;
  background-color:#fffffa;

} 

#title
{ text-align: center;
font-family: Limelight;
font-size: 60px;
padding: 0px;
margin-top:10vh;
margin-left:30vw;
position: absolute;
}

#sub-heading
{ text-align: center;
font-family: Limelight;
font-size: 30px;
padding: 0px;
margin-top:20vh;
margin-left:50vw;
position: absolute;
}

#text{
  text-align: center;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 20px;
  
  margin-top:40vh;
  margin-left:20vw;
  margin-right:20vw;
  position: absolute;
}

#logo
{
  margin-top:0vh;
  margin-left:85vw;
  margin-right:auto;
  position: absolute;
}

.grid-container {
  display: grid;
  grid-template-columns: auto auto auto auto;
  margin-left:20vw;
  margin-right:20vw;
  margin-top:50vh;
  position: absolute;
  text-align: center;
  grid-gap: 3vh 3vw;
}

.grid-item {
  background-color: rgba(255, 218, 88, 1);
  border: 1px solid rgba(0, 0, 0, 0.8);
  font-size: 10vh;
  border-radius: 5px;
  padding: 2vh;
  font-size: 2vh;
  text-align: center;
}

</style>
<html>
<body>

<main>
<h1 id="title">Assembly Elections 2022<h1>
<p id="sub-heading"><i>Metrics from the past</i><p>

<p id="text">Click on any of the buttons below to see what the numbers looked like in the last round of elections for the poll bound states of Punjab, Uttarakhand, Uttar Pradesh, Manipur and Goa</p>
  
<img id="logo" src="https://github.com/srishti-gupta-me/Election_Dashboard/blob/main/logo.png?raw=true"/>
  
<div class="grid-container">
 <div class="grid-item">NOTA</div>
 <div class="grid-item">Contesting Parties</div>
 <div class="grid-item">Voter Turnout</div>
 <div class="grid-item">Female Voter Turnout</div>
 <div class="grid-item">Male Voter Turnout</div>
 <div class="grid-item">Constituencies</div>
 <div class="grid-item">Women Winners</div>
 <div class="grid-item">Newcomers</div>
</div>
  
</main>
</body>
</html>
""", height=900)




st.markdown("""<hr/>""", unsafe_allow_html=True)

nota_container=st.container()
nota_1,nota_2, nota_3=nota_container.columns([3,1,3])

read_and_cache_csv = st.cache(suppress_st_warning=True)(pd.read_csv)
data = read_and_cache_csv('./nota.csv', nrows=100000)


@st.cache
def bar_chart(df,x_var,y_var, title="", x_axis_title="",y_axis_title=""):
    fig = px.bar(
        df,
        x=x_var,
        y=y_var,
        title=title
    )

    fig.update_layout(
        autosize=False,
        height=500,
        title={
        'text': title,
        'y':0.9,
        'x':0.5,
        'xanchor':'center',
        'yanchor':'top'}
    )

    fig.update_xaxes(
        title=x_axis_title,
    )

    fig.update_yaxes(
        title=y_axis_title,
        showgrid=False,
    )


    return fig.update_traces(
        hoverinfo="text",
        insidetextfont=dict(
            color="white"
        ),
    )

st.markdown("<div id='linkto_nota'></div>", unsafe_allow_html=True)    

nota_1.plotly_chart(bar_chart(data.astype(str), data.State,data.Nota_Percentage,"Nota Vote","State","Percentage"), use_container_width=True)

nota_3.image('./geo.png')

st.markdown("""<hr/>""", unsafe_allow_html=True)


st.markdown("<div id='linkto_party'></div>", unsafe_allow_html=True)    



party_container=st.container()
party_1,party_2, party_3=party_container.columns([3,1,3])


read_and_cache_csv = st.cache(suppress_st_warning=True)(pd.read_csv)
data = read_and_cache_csv('./party.csv', nrows=100000)


party_1.plotly_chart(bar_chart(data.astype(str), data.State,data.Contesting_Parties,"Party Contesting Election","State","Count"), use_container_width=True)

party_3.image('./geo.png')

st.markdown("""<hr/>""", unsafe_allow_html=True)



