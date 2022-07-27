import streamlit as st
import time
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Forecast", page_icon="📈")

st.markdown("# Forecast")
st.sidebar.header("Forecast")
st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)


import plotly.io as pio
from plotly.subplots import make_subplots

dataset_path = "/home/primedo/hcmus/DA/Datascience_2016-2/data/weather_data_hcm_[2017-2022]_preprocess.csv"

# @st.experimental_memo
def get_data(year) -> pd.DataFrame:
    dataset_path = f"../../data/{year}/weather_data_VietNam_[{year}].csv"
    return pd.read_csv(dataset_path)


col1, col2, col3, col4 = st.columns(4)
with col1:
    option1 = st.selectbox(
     'Choose year',
     ('2021', '2020',"2019","2018","2017"))

with col2:
    # st.subheader("Choose month")
    option2 = st.selectbox(
     'Choose month',
     ('1', '2',"3","4","5","6","7","8","9","10","11","12"))

with col3:
    # st.subheader("Choose feature")
    option3 = st.selectbox(
     'Choose day',
     ('1', '2',"3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"))

with col4:
    # st.subheader("Choose province")
    option4 = st.selectbox(
     'Choose province',
     ('An Giang',
 'Bà Rịa - Vũng Tàu',
 'Bắc Giang',
 'Bắc Kạn',
 'Bạc Liêu',
 'Bắc Ninh',
 'Bến Tre',
 'Bình Định',
 'Bình Dương',
 'Bình Phước',
 'Bình Thuận',
 'Cà Mau',
 'Cần Thơ',
 'Cao Bằng',
 'Đà Nẵng',
 'Đắk Lắk',
 'Đắk Nông', 
'Điện Biên',
 'Đồng Nai',
 'Đồng Tháp',
 'Gia Lai',
 'Hà Giang',
 'Hà Nam',
 'Hà Nội',
 'Hà Tĩnh',
 'Hải Dương',
 'Hải Phòng',
 'Hậu Giang',
'Thành phố Hồ Chí Minh',
 'Hòa Bình',
 'Hưng Yên',
 'Khánh Hòa',
 'Kiên Giang',
 'Kon Tum',
 'Lai Châu',
 'Lâm Đồng',
 'Lạng Sơn',
  'Lào Cai',
 'Long An',
 'Nam Định',
 'Nghệ An',
 'Ninh Bình',
 'Ninh Thuận',
 'Phú Thọ',
 'Phú Yên',
 'Quảng Bình',
 'Quảng Nam',
 'Quảng Ngãi',
 'Quảng Ninh',
 'Quảng Trị',
 'Sóc Trăng',
 'Sơn La',
 'Tây Ninh',
 'Thái Bình',
'Thái Nguyên',
 'Thanh Hóa',
 'Thừa Thiên Huế',
 'Tiền Giang',
 'Trà Vinh',
 'Tuyên Quang',
 'Vĩnh Long',
 'Vĩnh Phúc',
 'Yên Bái'))

df = get_data(option1)

df = df[(df.Province == option4) & (df.Day == int(option3)) & (df.Month == int(option2))]

df = df.drop(columns = ["Province","Day","Month","year"])

# print(df)

# data
pio.templates.default = "plotly_white"
cols = df.columns[3:-1]
ncols = len(cols)

# subplot setup
fig = make_subplots(rows=ncols, cols=1, shared_xaxes=True)

for i, col in enumerate(cols, start=1):
    fig.add_trace(go.Scatter(name = col, x=df["Time"], y=df[col].values), row=i, col=1)

fig.update_layout(width=800, height=1000)
fig.for_each_trace(lambda t: t.update(textfont_size=30, textposition='top center'))

st.plotly_chart(fig)
