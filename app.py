import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')

#importing the Census data
finalData=pd.read_csv('India_census.csv')
list_of_state=finalData['State'].unique().tolist()
list_of_state.insert(0, 'Overall India')
state_level_data=finalData.groupby('State').sum().reset_index().drop(columns=['District', 'Latitude', 'Longitude'])

#sidebar
st.sidebar.title('India Census Data Analysis')
selectedState=st.sidebar.selectbox("Select a State", list_of_state)
primary=st.sidebar.selectbox("Select a Primary Parameter",finalData.columns[5:])
secondary=st.sidebar.selectbox("Select a Secondary Parameter",finalData.columns[5:])
plotMap=st.sidebar.button("Plot graph")
topfive=st.sidebar.selectbox("Select a Parameter to get top/bottom analysis",finalData.columns[5:])
radio = st.sidebar.radio(
    "Select Top/Bottom five or All",
    ["Top/Bottom five", "All"])

plotbar=st.sidebar.button("Plot Bar graph for top 5 state/district")

#main screen
#map

if plotMap==True or plotbar==True:
    pass
else:
    st.title("India 2011 Census data analysis")
    st.text(f"Total Population of India (as of 2011): {finalData.groupby('State').sum().reset_index().drop(columns=['District', 'Latitude', 'Longitude'])['Population'].sum()}.")
    
    st.text("Top Five State in terms of population and other metrics:")
    st.dataframe(finalData.groupby('State').sum().reset_index().drop(columns=['District', 'Latitude', 'Longitude']).sort_values('Population', ascending=False).head()[['State', 'Population', 'Male', 'Female', 'Literate', 'Male_Literate', 'Female_Literate', 'Sex Ratio']].set_index('State'))

    st.text("Bottom Five State in terms of population and other metrics:")
    st.dataframe(finalData.groupby('State').sum().reset_index().drop(columns=['District', 'Latitude', 'Longitude']).sort_values('Population', ascending=False).tail()[['State', 'Population', 'Male', 'Female', 'Literate', 'Male_Literate', 'Female_Literate', 'Sex Ratio']].set_index('State'))

if plotMap==True:
    if selectedState=='Overall India':
        fig=px.scatter_mapbox(finalData, lat=finalData['Latitude'], lon=finalData['Longitude'], mapbox_style='carto-positron', zoom=3, size=primary, color=secondary, width=900, height=600, hover_name=finalData['District'], title="Size represents primary parameter and color represents secondary parameter.", template='simple_white')
        st.plotly_chart(fig, use_container_width=True)
    else:
        state_df=finalData[finalData['State']==selectedState]
        fig=px.scatter_mapbox(state_df, lat=state_df['Latitude'], lon=state_df['Longitude'], mapbox_style='carto-positron', zoom=3, size=primary, color=secondary, width=900, height=600, hover_name=state_df['District'], title="Size represents primary parameter and color represents secondary parameter.",template='simple_white')
        st.plotly_chart(fig, use_container_width=True)

#top/bottom
if plotbar==True:
    if selectedState=="Overall India":
        if radio=="Top/Bottom five":
            fig1=px.bar(state_level_data.sort_values(topfive, ascending=False).head(), x='State', y=topfive, color='Sex Ratio', hover_data=['Male', 'Female'], template='simple_white', height=300, title="Top Five")
            st.plotly_chart(fig1, use_container_width=True)

            fig2=px.bar(state_level_data.sort_values(topfive, ascending=True).head(), x='State', y=topfive, color='Sex Ratio', hover_data=['Male', 'Female'], template='simple_white', height=300, title="Bottom Five")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            fig1=px.bar(state_level_data.sort_values(topfive, ascending=False), x='State', y=topfive, color='Sex Ratio', hover_data=['Male', 'Female'], template='simple_white', height=600)
            st.plotly_chart(fig1, use_container_width=True)
    else:
        if radio=="Top/Bottom five":
            filtered1=finalData[finalData['State']==selectedState].sort_values(topfive, ascending=False).head()
            fig1=px.bar(filtered1, x='District', y=topfive, color='Sex Ratio', hover_data=['Male', 'Female'], template='simple_white', height=300, title="Top Five")
            st.plotly_chart(fig1, use_container_width=True)

            filtered2=finalData[finalData['State']==selectedState].sort_values(topfive, ascending=True).head()
            fig2=px.bar(filtered2, x='District', y=topfive, color='Sex Ratio', hover_data=['Male', 'Female'], template='simple_white', height=300, title="Bottom Five")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            filtered=finalData[finalData['State']==selectedState].sort_values(topfive, ascending=False)
            fig=px.bar(filtered, x='District', y=topfive, color='Sex Ratio', hover_data=['Male', 'Female'], template='simple_white', height=600)
            st.plotly_chart(fig, use_container_width=True)
    