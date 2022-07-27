import streamlit as st
import time
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils import *

st.set_page_config(page_title="Plotting Features", page_icon="📈")

st.markdown("# Plotting Features")
st.sidebar.header("Plotting Features")
st.write(   
    """This demo will visualize the data of each province. Enjoy!"""
)



# @st.experimental_memo
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_path)



col1, col2, col3 = st.columns(3)
with col1:
    option1 = st.selectbox(
     'Choose year',
     tuple(list_years[1:]))

with col2:
    option2 = st.selectbox(
        'Choose province',
        tuple(["All"] + list_provinces))

with col3:
    option3 = st.selectbox(
        'Choose feature',
        tuple(list_features))

dataset_path = f"../../data/vietnam/vietnam_[2017-2022]_fix.csv"
df = get_data()


st.header(f"{option3} Chart in 5 years")
if option2 == "All":
    df_prov = df
else:
    df_prov = df[df["Province"] == option2]

genre = st.radio(
    "Visualization in",
     options = ('Annualy', 'Monthly'))

if genre == "Annualy":
    fig = plot_5y_annualy(df_prov, option3)
else:
    fig = plot_5y_monthly(df_prov, option3)
st.plotly_chart(fig)


df = df[df["Year"] == int(option1)].reset_index(drop=True)

if option2 == "All":
    st.header(f"{option3} of Viet Nam in {option1}")
else:
    st.header(f"{option3} of {option2} vs national average")
genre = st.radio(
     "Type of visualization",
     ('Monthly', 'Daily'))

if genre == "Monthly":
    with st.spinner('Wait for it...'):
        fig = compareWithNationalInMonth(df, option2, option3)
else:
    with st.spinner('Wait for it...'):
        fig = compareWithNationalInDay(df, option2, option3)  

st.plotly_chart(fig)



if option2 == "All":
    st.header(f"Maximum and Minimum of {option3} in Viet Nam")
else:
    st.header(f"Maximum and Minimum of {option3} in {option2}")

genre1 = st.radio(
     "Choose type of visualization",
     ('Monthly', 'Daily'))

if genre1 == "Monthly":
    with st.spinner('Wait for it...'):
        fig = PLotMinMaxMonth(df, option2, option3)
else:
    with st.spinner('Wait for it...'):
        fig = PLotMinMaxDay(df, option2, option3)  

st.plotly_chart(fig)


st.header(f"Distribution of {option3}")
if option2 == "All":
    data = df[option3]
else:
    data = df[df.Province == option2][option3]
fig = plotCountAndDistribution(data, option3)
with st.spinner('Wait for it...'):
    st.plotly_chart(fig)


# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")