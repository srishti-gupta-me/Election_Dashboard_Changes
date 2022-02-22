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
import geopandas as gpd
from plotly.subplots import make_subplots
import json


#Adds favicon to the website and set page title 
favicon_image = Image.open('ashoka.jpeg')
st.set_page_config(page_title="Previous Election Insights", page_icon=favicon_image, layout="wide")



#To hide hamburger menu


#st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

#To reduce padding between containers in the application
padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)




#Landing Page 
components.html("""<html>
<style>

body {
  background-color: white;
} 

#title
{ text-align: center;
font-family: Arial;
font-size: 3vw;
padding: 0px;
margin-top:0vh;
margin-left:20vw;
position: absolute;
}

#sub-heading
{ text-align: center;
font-family: Arial;
font-size: 1.8vw;
padding: 0px;
margin-top:30vh;
margin-left:50vw;
position: absolute;
}

#logo
{
  margin-top:0vh;
  margin-left:85vw;
  margin-right:auto;
  position: absolute;
  width:5vw;
  height: auto;
}


</style>
<html>
<body>

<main>
<h1 id="title">Assembly Elections 2022<h1>
<p id="sub-heading"><i>Metrics from the past</i><p>

<img id="logo" src="https://github.com/srishti-gupta-me/Election_Dashboard/blob/main/logo.png?raw=true"/>
  
</main>
</body>
</html>
""", height=150)

landing_con=st.container()

landing_con_1, landing_con_2, landing_con_3, landing_con_4=landing_con.columns([0.5,1.5,1.5,0.5])

bg=Image.open(r'./initial_bg.png')

with landing_con_2:
    st.image(bg, use_column_width='always')  

original_title = '<p style="font-family:Arial; font-size: 1vw; margin-top: 15vh;">Click on any of the links below to see what the numbers looked like in the last round of elections for the poll bound states of Punjab, Uttarakhand, Uttar Pradesh, Manipur and Goa.</p>'

landing_con_3.markdown(original_title, unsafe_allow_html=True)


def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

local_css("style.css")


linkers=""" <style>  
  a {
   justify-content: center;
  align-items: center;
  }
  
.grid-container {
  display: grid;
  grid-template-columns: auto auto auto auto;
  margin-left:0vw;
  margin-right:0vw;
  margin-top:5vh;
  position: relative;
  text-align: center;
  grid-gap: 2vh 1vw;
}

.grid-item {
  background-color: rgba(255, 255, 255, 1);
  border: 1px solid rgba(0, 0, 0, 0);
  font-size: 1vw;
   
}

.button-css {

  padding: 0px 10px;
  background-color: rgba(255, 218, 88, 1);;
  color: #000;
  height:8vh;
  width:8vw;
  border-radius: 10px;
  text-align: center;
  
}</style>

<div class="grid-container">
 <div class="grid-item"><a href=#linkto_nota><button class="button-css">NOTA</button></a></div>
 <div class="grid-item"><a href=#linkto_party><button class="button-css">Contesting Parties</button></a></div>
 <div class="grid-item"><a href=#linkto_turnout><button class="button-css">Voter Turnout</button></a></div>
 <div class="grid-item"><a href=#linkto_turnout><button class="button-css">Female Voter Turnout</button></a></div>
 <div class="grid-item"><a href=#linkto_turnout><button class="button-css">Male Voter Turnout</button></a></div>
 <div class="grid-item"><a href=#linkto_cons><button class="button-css">Constituencies</button></a></div>
 <div class="grid-item"><a href=#linkto_women><button class="button-css">Women Winners</button></a></div>
 <div class="grid-item"><a href=#linkto_newcomer><button class="button-css">Newcomers</button></a></div>
</div>


"""
landing_con_3.markdown(linkers, unsafe_allow_html=True)
st.markdown("""<hr/>""", unsafe_allow_html=True)





with open('./India_States.geojson') as f:
    gj = json.load(f)
    

#Map function 
@st.cache
def map(df,x,df_1, title_fig=''):
    
    fig = px.choropleth(df_1, geojson=gj, locations='ST_NM', color='Value',
                               featureidkey="properties.ST_NM",
                               color_discrete_sequence=["rgb(211,211,211)"],
                                                             
                              )
    fig.add_trace(go.Choropleth(featureidkey='properties.ST_NM',
                                  geojson=gj,
                                  locations=df['State_Name'],
                                  z=df["{}".format(x)],
                                  colorscale=[[0, 'rgb(224,176,255)'], [1, 'rgb(128,0,128)']],
                                  #colorscale='viridis',
                                  showscale=False                      
                                 ))
  

    fig.update_geos(projection_type="van der grinten", fitbounds="locations", visible=False)
    fig.update_layout(autosize=False,title={'text': "{}".format(title_fig),
        'x':0.465,
        'y':0,
        'xanchor': 'center',
        'yanchor': 'bottom'},
         margin=dict(l=0, r=0, t=0, b=0, autoexpand=True),showlegend=False, height=800)
    fig.update_xaxes(mirror=True, showline=True)

    return(fig)


#To create base map
df_null= pd.read_csv("./states_shapefile_name.csv",dtype={"State": str})


csv = st.cache(suppress_st_warning=True)(pd.read_csv)

#Voter Turnout
voter_head_container=st.container()
voterh_1,voterh_2,voterh_3=voter_head_container.columns([3.5,2,3])
voterh_2.title('Voter Turnout')


voter_container=st.container()
voter_1,voter_2,voter_3=voter_container.columns([1,3,1])
voter=csv('./voterturnout.csv', nrows=100000)



fig = make_subplots(rows=1, cols=3, subplot_titles=("Voter Turnout-All", "Voter Turnout-Male", "Voter Turnout-Female"))


# All

fig.add_trace(go.Line(
    x=voter[voter['State_Name']=='Goa']['Year'],
    y=voter[voter['State_Name']=='Goa']['total'],
    name='Goa',
    marker_color='purple'
),row=1, col=1)

fig.add_trace(go.Line(
    x=voter[voter['State_Name']=='Manipur']['Year'],
    y=voter[voter['State_Name']=='Manipur']['total'],
    name='Manipur',
    marker_color='green'
),row=1, col=1)

fig.add_trace(go.Line(
    x=voter[voter['State_Name']=='Punjab']['Year'],
    y=voter[voter['State_Name']=='Punjab']['total'],
    name='Punjab',
    marker_color='red'
),row=1, col=1)


fig.add_trace(go.Line(
    x=voter[voter['State_Name']=='Uttarakhand']['Year'],
    y=voter[voter['State_Name']=='Uttarakhand']['total'],
    name='Uttarakhand',
    marker_color='yellow'
),row=1, col=1)

fig.add_trace(go.Line(
    x=voter[voter['State_Name']=='Uttar_Pradesh']['Year'],
    y=voter[voter['State_Name']=='Uttar_Pradesh']['total'],
    name='Uttar Pradesh',
    marker_color='blue'
),row=1, col=1)


#Male

fig.add_trace(go.Line(
    x=voter[voter['State_Name']=='Goa']['Year'],
    y=voter[voter['State_Name']=='Goa']['male'],showlegend=False,
    name='Goa',
    marker_color='purple'
),row=1, col=2)

fig.add_trace(go.Line(
    x=voter[voter['State_Name']=='Manipur']['Year'],
    y=voter[voter['State_Name']=='Manipur']['male'],showlegend=False,
    name='Manipur',
    marker_color='green'
),row=1, col=2)

fig.add_trace(go.Line(
    x=voter[voter['State_Name']=='Punjab']['Year'],
    y=voter[voter['State_Name']=='Punjab']['male'],showlegend=False,
    name='Punjab',
    marker_color='red'
),row=1, col=2)


fig.add_trace(go.Line(
    x=voter[voter['State_Name']=='Uttarakhand']['Year'],
    y=voter[voter['State_Name']=='Uttarakhand']['male'],showlegend=False,
    name='Uttarakhand',
    marker_color='yellow'
),row=1, col=2)

fig.add_trace(go.Line(
    x=voter[voter['State_Name']=='Uttar_Pradesh']['Year'],
    y=voter[voter['State_Name']=='Uttar_Pradesh']['male'],showlegend=False,
    name='Uttar Pradesh',
    marker_color='blue'
),row=1, col=2)



#Female

fig.add_trace(go.Line(
    x=voter[voter['State_Name']=='Goa']['Year'],
    y=voter[voter['State_Name']=='Goa']['female'],showlegend=False,
    name='Goa',
    marker_color='purple'
),row=1, col=3)

fig.add_trace(go.Line(
    x=voter[voter['State_Name']=='Manipur']['Year'],
    y=voter[voter['State_Name']=='Manipur']['female'],showlegend=False,
    name='Manipur',
    marker_color='green'
),row=1, col=3)

fig.add_trace(go.Line(
    x=voter[voter['State_Name']=='Punjab']['Year'],
    y=voter[voter['State_Name']=='Punjab']['female'],showlegend=False,
    name='Punjab',
    marker_color='red'
),row=1, col=3)


fig.add_trace(go.Line(
    x=voter[voter['State_Name']=='Uttarakhand']['Year'],
    y=voter[voter['State_Name']=='Uttarakhand']['female'],showlegend=False,
    name='Uttarakhand',
    marker_color='yellow'
),row=1, col=3)

fig.add_trace(go.Line(
    x=voter[voter['State_Name']=='Uttar_Pradesh']['Year'],
    y=voter[voter['State_Name']=='Uttar_Pradesh']['female'], showlegend=False,
    name='Uttar Pradesh',
    marker_color='blue'
),row=1, col=3)


#Layout

fig.update_layout(
    
      title={'text': "Voter Turnout- All",
        'y':1,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    legend_title="State Name",
    barmode='group', height=550, width=500)

fig.update_yaxes(title_text="Turnout Percentage",range=[0,100],row=1, col=1)
fig.update_xaxes(title_text="Year",range=[1960,2022], row=1, col=1)

fig.update_yaxes(title_text="Turnout Percentage",range=[0,100],row=1, col=2)
fig.update_xaxes(title_text="Year",range=[1960,2022], row=1, col=2)

fig.update_yaxes(title_text="Turnout Percentage",range=[0,100],row=1, col=3)
fig.update_xaxes(title_text="Year",range=[1960,2022], row=1, col=3)


st.plotly_chart(fig,use_container_width=True)


st.markdown("""<hr/>""", unsafe_allow_html=True)


#Women Winner and Contestant


women_head_container=st.container()
women_1,women_2,women_3=women_head_container.columns([2.5,3,2])
women_2.title('Women Winner and Contestants')


women_container=st.container()
women_1,women_2, women_3=women_container.columns([1,3,1])

contest=pd.read_csv('./data/contestant.csv')
contest['women_contestant_per']=np.nan
contest['women_contestant_per']=round(contest['Women']*100/contest['Total'],2)
contest['women_winner_per']=np.nan
contest['women_winner_per']=round(contest['Winner']*100/contest['total'],2)
contest.rename({'Total':'total_contestant','Women':'women_contestant','Winner':'women_winner','total':'total_winner'}, axis=1, inplace=True)

c_1=contest.groupby(['State_Name','Assembly_No','total_contestant','women_contestant'])['women_contestant_per'].unique().reset_index().explode('women_contestant_per')
c_1['type']='women_contestant_per'
c_1.rename({'women_contestant_per':'per'}, axis=1, inplace=True)

c_2=contest.groupby(['State_Name','Assembly_No','women_winner','total_winner'])['women_winner_per'].unique().reset_index().explode('women_winner_per')
c_2['type']='women_winner_per'
c_2.rename({'women_winner_per':'per'}, axis=1, inplace=True)

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
             labels = {"winner":"women","contestant":"total", "type":"", "per":"Percentage"}, 
             color_discrete_map={
             'women_winner_per': 'lightblue',
              'women_contestant_per': 'purple'
    })

fig.update_layout(hovermode=None, plot_bgcolor="White")
fig.update_xaxes(showline=True, linewidth=1, linecolor='grey')
fig.update_yaxes(showline=True, linewidth=1, linecolor='grey')


women_2.plotly_chart(fig,use_container_width=True)

st.markdown("""<hr/>""", unsafe_allow_html=True)


#Constituencies percentage

constituencies=pd.read_csv('./data/constituencies.csv')
constituencies['Percentage']=np.nan
constituencies['Percentage']=round(constituencies['count_i']*100/ constituencies['total'], 2)

fig = px.bar(constituencies, x="State_Name", y="Percentage",
             color='Constituency_Type', barmode='group',
             height=400, hover_name="Constituency_Type", hover_data={"count_i":True, "total":True, "Constituency_Type":False,"State_Name":False}, 
             labels = {"count_i":"Count","total":"Total", "type":"", "per":"Percentage"}, 
             color_discrete_map={
             'GEN': 'lightgreen',
              'SC': 'yellow',
                 'ST':'green'}
            )

fig.update_layout(hovermode=None, plot_bgcolor="White")
fig.update_xaxes(showline=True, linewidth=1, linecolor='grey')
fig.update_yaxes(showline=True, linewidth=1, linecolor='grey')

const_head_container=st.container()
const_1,const_2,const_3=const_head_container.columns([3,3,2])
const_2.title('Constituencies')


const_bar_container=st.container()
const_bar_1,const_bar_2, const_bar_3=const_bar_container.columns([1,3,1])
const_bar_2.plotly_chart(fig,use_container_width=True)




#Previous File 



# # import streamlit as st
# # import pandas as pd
# # import numpy as np
# # from plotly.tools import FigureFactory as ff
# # import matplotlib.pyplot as plt
# # import plotly.graph_objects as go
# # import plotly.express as px
# # import math
# # from PIL import Image
# # import streamlit.components.v1 as components
# # import base64
# # import geopandas as gpd
# # from plotly.subplots import make_subplots


# # #Adds favicon to the website and set page title 
# # favicon_image = Image.open('ashoka.jpeg')
# # st.set_page_config(page_title="Previous Election Insights", page_icon=favicon_image, layout="wide")



# # #To hide hamburger menu

# # hide_streamlit_style = """
# # <style>
# # #MainMenu {visibility: hidden;}
# # footer {visibility: hidden;}
# # </style>

# # """
# # st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# # #To reduce padding between containers in the application
# # padding = 0
# # st.markdown(f""" <style>
# #     .reportview-container .main .block-container{{
# #         padding-top: {padding}rem;
# #         padding-right: {padding}rem;
# #         padding-left: {padding}rem;
# #         padding-bottom: {padding}rem;
# #     }} </style> """, unsafe_allow_html=True)




# # #Landing Page 
# # components.html("""<html>
# # <style>

# # body {
# #   background-color: white;
# # } 

# # #title
# # { text-align: center;
# # font-family: Arial;
# # font-size: 3vw;
# # padding: 0px;
# # margin-top:0vh;
# # margin-left:20vw;
# # position: absolute;
# # }

# # #sub-heading
# # { text-align: center;
# # font-family: Arial;
# # font-size: 1.8vw;
# # padding: 0px;
# # margin-top:30vh;
# # margin-left:50vw;
# # position: absolute;
# # }

# # #logo
# # {
# #   margin-top:0vh;
# #   margin-left:85vw;
# #   margin-right:auto;
# #   position: absolute;
# #   width:5vw;
# #   height: auto;
# # }


# # </style>
# # <html>
# # <body>

# # <main>
# # <h1 id="title">Assembly Elections 2022<h1>
# # <p id="sub-heading"><i>Metrics from the past</i><p>

# # <img id="logo" src="https://github.com/srishti-gupta-me/Election_Dashboard/blob/main/logo.png?raw=true"/>
  
# # </main>
# # </body>
# # </html>
# # """, height=150)

# # landing_con=st.container()

# # landing_con_1, landing_con_2, landing_con_3, landing_con_4=landing_con.columns([0.5,1.5,1.5,0.5])

# # bg=Image.open(r'./initial_bg.png')

# # with landing_con_2:
# #     st.image(bg, use_column_width='always')  

# # original_title = '<p style="font-family:Arial; font-size: 1vw; margin-top: 15vh;">Click on any of the links below to see what the numbers looked like in the last round of elections for the poll bound states of Punjab, Uttarakhand, Uttar Pradesh, Manipur and Goa.</p>'

# # landing_con_3.markdown(original_title, unsafe_allow_html=True)


# # def local_css(file_name):
# #     with open(file_name) as f:
# #         st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

# # local_css("style.css")


# # linkers=""" <style>  
# #   a {
# #    justify-content: center;
# #   align-items: center;
# #   }
  
# # .grid-container {
# #   display: grid;
# #   grid-template-columns: auto auto auto auto;
# #   margin-left:0vw;
# #   margin-right:0vw;
# #   margin-top:5vh;
# #   position: relative;
# #   text-align: center;
# #   grid-gap: 2vh 1vw;
# # }

# # .grid-item {
# #   background-color: rgba(255, 255, 255, 1);
# #   border: 1px solid rgba(0, 0, 0, 0);
# #   font-size: 1vw;
   
# # }

# # .button-css {

# #   padding: 0px 10px;
# #   background-color: rgba(255, 218, 88, 1);;
# #   color: #000;
# #   height:8vh;
# #   width:8vw;
# #   border-radius: 10px;
# #   text-align: center;
  
# # }</style>

# # <div class="grid-container">
# #  <div class="grid-item"><a href=#linkto_nota><button class="button-css">NOTA</button></a></div>
# #  <div class="grid-item"><a href=#linkto_party><button class="button-css">Contesting Parties</button></a></div>
# #  <div class="grid-item"><a href=#linkto_turnout><button class="button-css">Voter Turnout</button></a></div>
# #  <div class="grid-item"><a href=#linkto_turnout><button class="button-css">Female Voter Turnout</button></a></div>
# #  <div class="grid-item"><a href=#linkto_turnout><button class="button-css">Male Voter Turnout</button></a></div>
# #  <div class="grid-item"><a href=#linkto_cons><button class="button-css">Constituencies</button></a></div>
# #  <div class="grid-item"><a href=#linkto_women><button class="button-css">Women Winners</button></a></div>
# #  <div class="grid-item"><a href=#linkto_newcomer><button class="button-css">Newcomers</button></a></div>
# # </div>


# # """
# # landing_con_3.markdown(linkers, unsafe_allow_html=True)
# # st.markdown("""<hr/>""", unsafe_allow_html=True)





# # #Bar Chart function 
# # @st.cache
# # def bar_chart(df,x_var,y_var, title="", x_axis_title="",y_axis_title=""):
# #     fig = px.bar(
# #         df,
# #         x=x_var,
# #         y=y_var,
# #         title=title
# #     )

# #     fig.update_layout(
        
# #         margin=dict(l=0, r=20, t=100, b=0),
# #         autosize=False,
# #         width=200,
# #         height=500,
# #         title={
# #         'text': title,
# #         'y':1,
# #         'x':0.6,
# #         'xanchor':'center',
# #         'yanchor':'top'}
# #     )

# #     fig.update_xaxes(
# #         title=x_axis_title,
# #     )

# #     fig.update_yaxes(
# #         title=y_axis_title,
# #         showgrid=False,
# #     )


# #     return fig.update_traces(
# #         hoverinfo="text",
# #         insidetextfont=dict(
# #             color="white"
# #         ),
# #     )
# # import json
# # with open('./India_States.geojson') as f:
# #     gj = json.load(f)
    

# # #Map function 
# # @st.cache
# # def map(df,x,df_1, title_fig=''):
    
# #     fig = px.choropleth(df_1, geojson=gj, locations='ST_NM', color='Value',
# #                                featureidkey="properties.ST_NM",
# #                                color_discrete_sequence=["rgb(211,211,211)"],
                               
                               
# #                               )
# #     fig.add_trace(go.Choropleth(featureidkey='properties.ST_NM',
# #                                   geojson=gj,
# #                                   locations=df['State_Name'],
# #                                   z=df["{}".format(x)],
# #                                   colorscale=[[0, 'rgb(224,176,255)'], [1, 'rgb(128,0,128)']],
# #                                   #colorscale='viridis',
# #                                   showscale=False                      
# #                                  ))
  

# #     fig.update_geos(fitbounds="locations", visible=False)
# #     fig.update_layout(title={'text': "{}".format(title_fig),
# #         'x':0.465,
# #         'y':0,
# #         'xanchor': 'center',
# #         'yanchor': 'bottom'},
# #          margin=dict(l=0, r=0, t=0, b=0),showlegend=False)
# #     fig.update_xaxes(mirror=True)

# #     return(fig)


# # #To create base map
# # df_null= pd.read_csv("./states_shapefile_name.csv",dtype={"State": str})

# # #Need 6 containers which are horizontal 



# # #NOTA
# # st.markdown("<div id='linkto_nota'></div>", unsafe_allow_html=True)   


# # nota_head_container=st.container()
# # nota_1,nota_2,nota_3=nota_head_container.columns([2,2,1])
# # nota_2.title('NOTA Percentage')


# # nota_body_container=st.container()
# # nota_b1,nota_b2,nota_b3=nota_body_container.columns([1,3,1])

# # csv = st.cache(suppress_st_warning=True)(pd.read_csv)
# # df_nota= csv("./data/nota.csv",dtype={"State_Name": str})
# # nota_b2.plotly_chart(map(df_nota,'Percentage',df_null),use_container_width=True)

# # st.markdown("""<hr/>""", unsafe_allow_html=True)
 
# # #Contesting and Represented Parties

# # st.markdown("<div id='linkto_party'></div>", unsafe_allow_html=True)   


# # party_head_container=st.container()
# # party_1,party_2,party_3=party_head_container.columns([1.4,2,1])
# # party_2.title('Party Contested and Represented')

# # party_body_container=st.container()
# # party_b1,party_b2=party_body_container.columns([1,1])

# # df_party= csv("./data/party.csv",dtype={"State_Name": str})

# # party_b1.plotly_chart(map(df_party,'Contested_Count',df_null,'Contested'),use_container_width=True)
# # party_b2.plotly_chart(map(df_party,'Represented_Count',df_null,'Represented'),use_container_width=True)

# # st.markdown("""<hr/>""", unsafe_allow_html=True)

# # #Voter Turnout

# # st.markdown("<div id='linkto_turnout'></div>", unsafe_allow_html=True)   


# # vot_head_container=st.container()
# # vot_1,vot_2,vot_3=vot_head_container.columns([2,2,1])
# # vot_2.title('Voter Turnout')



# # df_vot=csv("./data/voter.csv",dtype={"State_Name": str})

# # st.plotly_chart(map(df_vot,'total',df_null,'Overall'),use_container_width=True)

# # vot_body_container=st.container()
# # vot_b1,vot_b2=vot_body_container.columns([1,1])
# # vot_b1.plotly_chart(map(df_vot,'male',df_null,'Male Turnout'),use_container_width=True)
# # vot_b2.plotly_chart(map(df_vot,'female',df_null,'Female Turnout'),use_container_width=True)

# # st.markdown("""<hr/>""", unsafe_allow_html=True)

# # #Constituencies 

# # st.markdown("<div id='linkto_cons'></div>", unsafe_allow_html=True)   
# # df_con=csv("./data/constituencies.csv",dtype={"State_Name": str})

# # cons_head_container=st.container()
# # cons_1,cons_2,cons_3=cons_head_container.columns([2,2,1])
# # cons_2.title('Constituencies')

# # cons_body_container=st.container()
# # cons_b1,cons_b2=cons_body_container.columns([1,1])

# # #Group Bar Chart
# # fig_1 = go.Figure()
# # fig_1.add_trace(go.Bar(
# #     x=df_con[df_con['Constituency_Type']=='GEN']['State_Name'],
# #     y=df_con[df_con['Constituency_Type']=='GEN']['count_i'],
# #     name='GEN',
# #     marker_color='purple'
# # ))
# # fig_1.add_trace(go.Bar(
# #     x=df_con[df_con['Constituency_Type']=='SC']['State_Name'],
# #     y=df_con[df_con['Constituency_Type']=='SC']['count_i'],
# #     name='SC',
# #     marker_color='red'
# # ))
# # fig_1.add_trace(go.Bar(
# #     x=df_con[df_con['Constituency_Type']=='ST']['State_Name'],
# #     y=df_con[df_con['Constituency_Type']=='ST']['count_i'],
# #     name='ST',
# #     marker_color='yellow'
# # ))
# # fig_1.update_layout(barmode='group')

# # cons_b1.plotly_chart(fig_1,use_container_width=True)
# # cons_b2.plotly_chart(map(df_con,'total',df_null,'Total Constituencies'),use_container_width=True)

# # st.markdown("""<hr/>""", unsafe_allow_html=True)

# # #Women and New-Comer

# # st.markdown("<div id='linkto_women'></div>", unsafe_allow_html=True)  
# # st.markdown("<div id='linkto_newcomer'></div>", unsafe_allow_html=True)   

# # wo_head_container=st.container()
# # wo_1,wo_2,wo_3,wo_4,wo_5,wo_6=wo_head_container.columns([1,2,1,1,2,1])

# # wo_2.title('Women Winners')
# # wo_5.title('Newcomers')

# # wo_body_container=st.container()

# # wo_b1,wo_b2=wo_body_container.columns([1,1])

# # df_women=csv("./data/women_winner.csv",dtype={"State_Name": str})
# # df_newcomer=csv("./data/newcomer.csv",dtype={"State_Name": str})


# # wo_b1.plotly_chart(map(df_women,'count',df_null,''),use_container_width=True)
# # wo_b2.plotly_chart(map(df_newcomer,'count',df_null,''),use_container_width=True)


# # st.markdown("""<hr/>""", unsafe_allow_html=True)




# # assembly_head_container=st.container()
# # assh_1,assh_2,assh_3=assembly_head_container.columns([1,2,1])
# # assh_2.title('General Elections with Assembly Numbers')

# # assembly_container=st.container()
# # # assembly_container.subheader('General Elections with Assembly Numbers')

# # ass_1,ass_2,ass_3=assembly_container.columns([3,0.1,2.5])

# # ass_csv = st.cache(suppress_st_warning=True)(pd.read_csv)
# # ass_data = ass_csv('./Assembly_Chart.csv', nrows=100000)
# # fig_1 = px.sunburst(ass_data, path=['State_Name','Assembly_No','Year'], values='Count',width=600, height=600)

# # ass_1.plotly_chart(fig_1, use_container_width=True)

# # ass_data_label = pd.DataFrame({'State_Name':["State_Name"],'Assembly_Number':['Assembly Number'],'Year':['General Election Year']})
# # fig_2 = px.sunburst(ass_data_label, path=['State_Name','Assembly_Number','Year'],width=600, height=500)

# # ass_3.markdown("<br/><br/>",unsafe_allow_html=True)
# # ass_3.plotly_chart(fig_2, use_container_width=True)

# # st.markdown("""<hr/>""", unsafe_allow_html=True)








