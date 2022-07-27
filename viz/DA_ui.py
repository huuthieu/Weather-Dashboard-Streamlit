import time  # to simulate a real time data, time loop

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
# import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development

import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(
    page_title="Weather Analysis Dashboard",
    page_icon="✅",
    layout="wide",
)

dataset_path = "/home/primedo/hcmus/DA/Datascience_2016-2/data/weather_data_hcm_[2017-2022]_preprocess.csv"

# @st.experimental_memo
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_path)

df = get_data()

# dashboard title
st.title("Weather Analysis Dashboard")

temperature = df.groupby(["Month","Year"]).mean()["Temperature"]
ind = sorted(temperature.index, key = lambda x: x[1])

x = temperature[ind].reset_index(level=0)
x = x.reset_index(level=0)
x["Time"] = x["Month"].astype(str) + "-" + x["Year"].astype(str)


title = "Temperature in Ho Chi Minh City"
x.plot(x="Time", y="Temperature", kind="line", figsize = (12, 6),grid=True, colormap = 'PRGn', title = title)
plt.ylabel('Temperature (degree Celsius)', fontsize = 15)
plt.xlabel('Time', fontsize = 15)
plt.title('Temperature in Ho Chi Minh City', fontsize = 19)

buf = BytesIO()
plt.savefig(buf, format="png")
st.image(buf)