import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import numpy as np
import termcolor as tc
import colored as c
import plotly.graph_objects as go
import math


#[theme]
primaryColor="#a88e7a"
backgroundColor="#f7f0e9"
secondaryBackgroundColor="#d4cec3"
textColor="#6b513d"


st.set_page_config(layout="wide")

@st.cache
def loadata():
    data = pd.read_excel('data/data.xlsx', index_col=None)
    return data

data = loadata()


st.title("Schools Based on Your Preferences")

#Sidebar#
st.sidebar.title("Filters")

Location = st.sidebar.multiselect('Location',
                 options=data["STABBR"].unique())

Tuition = st.sidebar.slider('Choose Maximum Tuition',
                            min_value=int(data["COSTT4_A"].min()), max_value=int(data["COSTT4_A"].max()))

DegreeType = st.sidebar.multiselect('Choose which type of degree you are interested in',
                                    options=['Certification', 'Associates Degree', "Bachelor's Degree", "Graduate Degree"])

Testing = st.sidebar.radio('Standardized testing Required',
                                   options=['Yes', 'No', "It doesn't matter"])
#FILTER
mask=data["STABBR"].isin(Location)
data=data[mask]

mask=data["COSTT4_A"]<=Tuition
data=data[mask]

if Testing != "It doesn't matter":
    mask=data["ADMCON7"].isin([Testing])
    data=data[mask]


mask=data["HIGHDEG"].isin(DegreeType)
data=data[mask]

#Accordian#

datagender = pd.melt(data,
                               id_vars=["INSTNM"],
                               value_vars=['UGDS_MEN', 'UGDS_WOMEN'],
                               var_name="Gender",
                               value_name="Population"
                               )

datagender["Gender"] = datagender["Gender"].replace({"UGDS_MEN":"Men",'UGDS_WOMEN':'Women'})

datarace = pd.melt(data,
                               id_vars=["INSTNM"],
                               value_vars=["UGDS_WHITE", "UGDS_BLACK", "UGDS_HISP", "UGDS_ASIAN", "UGDS_AIAN", "UGDS_NHPI", "UGDS_2MOR", "UGDS_NRA", "UGDS_UNKN"],
                               var_name="Ethnicity",
                               value_name="Population"
                               )
datarace["Ethnicity"] = datarace["Ethnicity"].replace({"UGDS_WHITE":"White", 'UGDS_BLACK':'Black','UGDS_HISP':'Hispanic', 'UGDS_ASIAN':'Asian','UGDS_AIAN':'American Indian/Alaskan Native','UGDS_NHPI':'Native Hawaiian/Pacific Islander','UGDS_2MOR':'Two or more Races','UGDS_NRA':'NonResident','UGDS_UNKN':'Race Unknown'})

for index, row in data.iterrows():


    with st.expander(row["INSTNM"]):

        col1, col2 = st.columns(2)

        with col1:

            mask = data["INSTNM"] == row["INSTNM"]
            datamap = data[mask]
            fig = px.scatter_mapbox(lat= datamap["LATITUDE"],
                                    lon=datamap["LONGITUDE"],
                                    hover_name=datamap["INSTNM"],
                                    color_discrete_sequence=["fuchsia"],
                                    zoom=3,
                                    height=300, width = 500
                                    )
            fig.update_layout(mapbox_style="open-street-map")
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
            st.plotly_chart(fig)


        with col2:
            st.markdown('[Webpage](https://{})'.format(row['INSTURL']))
            st.write("Highest Enrollment Offered: {}".format(row["HIGHDEG"]))

            if not (math.isnan(row["ADM_RATE_ALL"])):
                st.write("Admissions Rate: {:.2f}%".format(row["ADM_RATE_ALL"] *100))

        st.subheader("Student Demographics")

        col3, col4 = st.columns(2)

        with col3:
            mask=datarace["INSTNM"]==row["INSTNM"]
            dataSchool=datarace[mask]
            fig = px.pie(dataSchool, values='Population', names='Ethnicity', title='By Race',
                         width=600, height=600
                         )
            st.plotly_chart(fig)

        with col4:
            mask = datagender["INSTNM"] == row["INSTNM"]
            dataSchoolg = datagender[mask]
            fig = px.pie(dataSchoolg, values='Population', names='Gender', title='By Gender',
                         width=500, height=500)
            st.plotly_chart(fig)