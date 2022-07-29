import streamlit as st
import time
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import requests
from bs4 import BeautifulSoup
from utils import *
import datetime
import re
from models import *
from preprocess import *


st.set_page_config(page_title="Forecast", page_icon="📈")

st.markdown("# Forecast")
st.sidebar.header("Forecast")
st.write(
    """This is a demo of our weather forecast dashboard. We will display current weather values and make predictions for the near future. Enjoy!"""
)
import plotly.io as pio
from plotly.subplots import make_subplots

option = st.selectbox(
    'Choose province',
    tuple(list_provinces))

province = pd.read_excel(province_path)
province_dict = dict(zip(province.columns, province.iloc[0]))


url = "https://www.worldweatheronline.com/Can-Tho-weather/vn.aspx"
url = url.replace("Can-Tho", province_dict[option])
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

now = datetime.datetime.now()

st.markdown(
    f"<p style='color: #FF5733; "
    f"font-weight: bold; font-size: 25px;'> 📍 Weather at {option} currently </p>",
    unsafe_allow_html=True,
)

with st.spinner('Wait for it...'):
    temperature = soup.find_all("div",{"class":"weather-widget-temperature"})[0].find_all("p")[0].text.strip()
    # wind_speed = soup.find_all("span", {"class": "wind-speed"})[0].text
    weather =  soup.find_all("div",{"class":"weather-widget-icon"})[0].find_all("p")[0].text.strip()
    feats = soup.find_all("div",{"class":"ws-details-item"})
    wind_speed = feats[0].find_all("span")[0].text.strip()
    dir = feats[0].find_all("img")[0]["style"]
    dir = re.findall("\(.*\)",dir)[0].strip('(deg)')
    rain = feats[1].find_all("span")[0].text.strip()
    cloud = feats[2].find_all("span")[0].text.strip()
    humidity = feats[3].find_all("span")[0].text.strip()
    pressure, dew_point = get_data_msn(option)    
    # a = soup.find_all("div",{"class":"wind-direction"})[0].find_all("img")[0]
    # dir = re.findall("\(.*\)",a["style"])[0].strip('(deg)')
    # st.markdown(f"#### ☁️ Weather: {weather}")
    col1, col2 = st.columns(2)
    col1.markdown("#### " + now.strftime("%d/%m/%Y"))
    col1.markdown("##### " + now.strftime("%H:%M"))
    col2.metric("☁️ Weather", weather)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        col1.metric("🌡️ Temperature",f"{temperature}°C")
        col1.metric("💨 Wind Speed",f"{wind_speed}")
    with col2:
        col2.metric("💧 Rain",f"{rain}")
        col2.metric("💨 Wind Dir",f"{dir}°")
        
    with col3:
        col3.metric("💦 Humidity",f"{humidity}")
        col3.metric("🕗 Pressure",f"{pressure}")
    with col4:
        col4.metric("☁️ Cloud",f"{cloud}")
        col4.metric("🌡️ Dew Point",f"{dew_point}")

# st.markdown("![](https://www.worldweatheronline.com/staticv150817/assets-202110/img/wind-direction.svg)")
# st.metric("☔ Rain Alert", "Rain")
st.markdown(
    f"<p style='color: #FF5733; "
    f"font-weight: bold; font-size: 25px;'> 📍 Alert in next 3 hours </p>",
    unsafe_allow_html=True,
)

df = pd.read_csv(dataset_path)
# genre = st.radio(
#     "",
#      options = ('Annualy', 'Monthly'))
gust = 0.0
feature_vals = [humidity, dew_point, temperature, rain, cloud, wind_speed, dir, pressure, gust, weather]
print(feature_vals)

dict_test = dict(zip(list_features, feature_vals))

time_h = rounding_time(now.hour)
if len(str(time_h)) == 1:
    time = "0" + str(time_h) + ":00"
else:
    time = str(time_h) + ":00"

dict_test.update({"Day": int(now.strftime("%d")),
                 "Month": int(now.strftime("%m")),
                    "Year": int(now.strftime("%Y")),
                    "Time": time})


data_test = pd.DataFrame([dict_test])

data_test = process_data(data_test)

res = pipeline(df, data_test, option)

if res < 0.5:
    label = "No Rain"
else: 
    label = "Rain"
st.metric("☔ Rain Alert", f"{label}")
# st.markdown("### ☔ Rain Alert in next 3 hours: Rain")

