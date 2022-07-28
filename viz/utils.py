from tkinter import X
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
import requests
from bs4 import BeautifulSoup
import time


list_provinces = ['An Giang','Bà Rịa - Vũng Tàu','Bắc Giang','Bắc Kạn','Bạc Liêu','Bắc Ninh',
 'Bến Tre','Bình Định','Bình Dương','Bình Phước','Bình Thuận','Cà Mau','Cần Thơ','Cao Bằng',
 'Đà Nẵng','Đắk Lắk','Đắk Nông', 'Điện Biên','Đồng Nai','Đồng Tháp','Gia Lai','Hà Giang','Hà Nam',
 'Hà Nội','Hà Tĩnh','Hải Dương','Hải Phòng','Hậu Giang','Thành phố Hồ Chí Minh','Hòa Bình',
 'Hưng Yên','Khánh Hòa','Kiên Giang','Kon Tum','Lai Châu','Lâm Đồng','Lạng Sơn','Lào Cai',
 'Long An','Nam Định','Nghệ An','Ninh Bình','Ninh Thuận','Phú Thọ','Phú Yên','Quảng Bình',
 'Quảng Nam','Quảng Ngãi','Quảng Ninh','Quảng Trị','Sóc Trăng','Sơn La','Tây Ninh','Thái Bình',
 'Thái Nguyên','Thanh Hóa','Thừa Thiên Huế','Tiền Giang','Trà Vinh','Tuyên Quang','Vĩnh Long',
 'Vĩnh Phúc','Yên Bái']

list_eng_province =  ['An Giang Province','Ba Ria - Vung Tau Province','Bac Giang Province','Bac Kan Province','Bac Lieu Province','Bac Ninh Province',
 'Ben Tre Province','Binh Dinh Province','Binh Duong Province','Binh Phuoc Province','Binh Thuan Province','Ca Mau Province','Can Tho City','Cao Bang Province',
 'Da Nang City','Dak Lak Province','Dak Nong Province','Dien Bien Province','Dong Nai Province','Dong Thap Province','Gia Lai Province','Ha Giang Province','Ha Nam Province',
 'Ha Noi City','Ha Tinh Province','Hai Duong Province','Hai Phong City','Hau Giang Province','Ho Chi Minh City','Hoa Binh Province',
 'Hung Yen Province','Khanh Hoa Province','Kien Giang Province','Kon Tum Province','Lai Chau Province','Lam Dong Province','Lang Son Province','Lao Cai Province',
 'Long An Province','Nam Dinh Province','Nghe An Province','Ninh Binh Province','Ninh Thuan Province','Phu Tho Province','Phu Yen Province','Quang Binh Province',
 'Quang Nam Province','Quang Ngai Province','Quang Ninh Province','Quang Tri Province','Soc Trang Province','Son La Province','Tay Ninh Province','Thai Binh Province',
 'Thai Nguyen Province','Thanh Hoa Province','Thua Thien Hue Province','Tien Giang Province','Tra Vinh Province', 'Tuyen Quang Province','Vinh Long Province',
 'Vinh Phuc Province','Yen Bai Province']

list_features = ["Humidity", "Dew point", "Temperature", "Rain", "Cloud", "Wind", "Dir",
 "Pressure", "Gust", "Weather"]
 
list_years = ["All", "2022", '2021', '2020',"2019","2018","2017"]

list_months = ['1', '2',"3","4","5","6","7","8","9","10","11","12"]

month_dict = {
    "1": "January",
    "2": "February",
    "3": "March",
    "4": "April",
    "5": "May",
    "6": "June",
    "7": "July",
    "8": "August",
    "9": "September",
    "10": "October",
    "11": "November",
    "12": "December"
}


name_dict_ve = dict(zip(list_provinces, list_eng_province))

name_dict_ev = dict(zip(list_eng_province, list_provinces))

unit_mapping = {"Humidity": "%", "Dew point": "°C", "Temperature": "°C", "Rain": "mm", "Cloud": "%", "Wind": "km/h", "Dir": "°", "Pressure": "mb", "Gust": "km/h"}

def rounding_time(hour):
    time_list = [0, 3, 6, 9, 12, 15, 18, 21]
    min_dis = 30
    round_h = 0
    for i in range(len(time_list)):
        if abs(hour - time_list[i]) < min_dis:
            min_dis = abs(hour - time_list[i])
            round_h = time_list[i]
    return int(round_h)

def formatDate(HCM_df):
    # Changing Formatted Date from String to Datetime
    HCM_df = HCM_df.rename(columns = {"year":"Year"})
    t = [str(HCM_df['Year'][k]) + '-' + str(HCM_df['Month'][k]) + '-' + str(HCM_df['Day'][k]) + ' ' + str(HCM_df['Time'][k]) for k in range(len(HCM_df))]
    HCM_df['Formatted Date'] = pd.to_datetime(t, utc=True)

    d=[str(HCM_df['Year'][k]) + '-' + str(HCM_df['Month'][k]) + '-' + str(HCM_df['Day'][k]) for k in range(len(HCM_df))]
    HCM_df['Date'] = pd.to_datetime(d, format='%Y-%m-%d')
    HCM_df = HCM_df.sort_values(by='Formatted Date')

    RAIN_LABEL = ['Light drizzle','Light rain','Light rain shower', 'Patchy light drizzle', 'Patchy light rain', 
                'Patchy light rain with thunder','Patchy rain possible','Heavy rain','Heavy rain at times',
                'Moderate or heavy rain shower','Moderate rain', 'Moderate rain at times', 'Overcast','Torrential rain shower']
    tmp = []
    for i, value in enumerate(HCM_df['Weather']):
        if value in RAIN_LABEL:
            tmp.append(1)
        else:
            tmp.append(0)
    HCM_df['Label'] = tmp
    # HCM_df.reset_index(inplace=True)
    return HCM_df


def compareWithNationalInDay(VN_df, prv, col):
    if prv == 'All':
        return plotVNdataDay(VN_df, col)
    VN_df = formatDate(VN_df)
    province = list(VN_df.Province.unique())
    ls = []
    days = VN_df['Date'].unique()
    m = []
    for c in province:
        grouped = VN_df.groupby(VN_df['Province'])
        df = grouped.get_group(c)  
        if c == prv:
            m = [df[df.Date == d][col].mean() for d in days]
        t_mean = [df[df.Date == d][col].mean() for d in days]
        ls.append(t_mean)

    mean_prv=np.mean(np.array(ls), axis = 0)
    year = [np.datetime64(k, 'Y') for k in days]


    plt.figure(figsize = (20,10))
    dt = pd.DataFrame({prv:m, 'VN':mean_prv, 'Date': days}) #np.arange(VN_df[col].min(),VN_df[col].max()) 
    fig = px.line(dt, x='Date', y=[prv, 'VN']) # 'Mean':t_mean,

    fig.update_layout(
        # title='Compare the national average '+ col +  ' with ' + prv,
        width = 900,
        xaxis_title="Days",
        yaxis_title=col + ' ' + '(' + unit_mapping[col] + ')',
        legend_title="Note",
        font=dict(
            family="Courier New, monospace",
            size=18))
    return fig


def plotVNdataDay(VN_df, col):
    VN_df = VN_df.rename(columns = {"year":"Year"})
    VN_df = formatDate(VN_df)
    province = list(VN_df.Province.unique())
    ls = []
    days = VN_df['Date'].unique()
    for c in province:
        grouped = VN_df.groupby(VN_df['Province'])
        df = grouped.get_group(c)  
        t_mean = [df[df.Date == d][col].mean() for d in days]
        ls.append(t_mean)

    mean_prv=np.mean(np.array(ls), axis = 0)
    year = [np.datetime64(k, 'Y') for k in days]


    plt.figure(figsize = (20,10))
    dt = pd.DataFrame({col:mean_prv, 'Date': days}) #np.arange(VN_df[col].min(),VN_df[col].max()) 
    fig = px.line(dt, x='Date', y=col) # 'Mean':t_mean,

    fig.update_layout(
        # title='Compare the national average '+ col +  ' with ' + prv,
        width = 900,
        xaxis_title="Days",
        yaxis_title=col + ' ' + '(' + unit_mapping[col] + ')',
        font=dict(
            family="Courier New, monospace",
            size=18))
    return fig



def plotVNdataMonth(VN_df, col):
    VN_df = VN_df.rename(columns = {"year":"Year"})
    data = VN_df.groupby(["Month","Year"]).mean()[col]
    x = data.reset_index(level=0)     
    x = x.reset_index(level=0)
    plt.figure(figsize = (20,10))
    fig = px.line(x, x="Month", y=col)
    fig.update_layout(
        # title='Compare the national average '+ col +  ' with ' + prv,
        width = 900,
        xaxis_title="Month",
        yaxis_title=col + ' ' + '(' + unit_mapping[col] + ')',
        font=dict(
            family="Courier New, monospace",
            size=18))

    return fig 


def compareWithNationalInMonth(VN_df, prv, col):
    if prv == "All":
        return plotVNdataMonth(VN_df, col)
    VN_df = VN_df.rename(columns = {"year":"Year"})
    prov_data = VN_df[VN_df["Province"] == prv].groupby(["Month","Year"]).mean()[col]
    ind1 = sorted(prov_data.index, key = lambda x: x[0])
    data = VN_df.groupby(["Month","Year"]).mean()[col]
    ind2 = sorted(data.index, key = lambda x: x[0])
    data = pd.merge(data[ind2] , prov_data[ind1] , on=["Month","Year"], how='inner')
    # ind = sorted(data.index, key = lambda x: x[0])
    # print(ind)
    # print(data)

    x = data.reset_index(level=0)
    x = x.reset_index(level=0)
    # x["Time"] = x["Month"].astype(str) + "-" + x["Year"].astype(str)
    x = x.rename(columns = {f"{col}_x": "VN", f"{col}_y": prv}) 
    plt.figure(figsize = (20,10))
    fig = px.line(x, x="Month", y=[prv,"VN"])
    fig.update_layout(
        # title='Compare the national average '+ col +  ' with ' + prv,
        width = 900,
        xaxis_title="Month",
        yaxis_title=col + ' ' + '(' + unit_mapping[col] + ')',
        legend_title="Note",
        font=dict(
            family="Courier New, monospace",
            size=18))

    return fig


def PLotMinMaxDay(VN_df, prov, col):
    VN_df = formatDate(VN_df)
    if prov == "All":
        df = VN_df
    else:
        df = VN_df[VN_df["Province"] == prov]
    days = list(df['Date'].unique())

    province = list(df.Province.unique())
    ls_max = []
    ls_min = []
    days = VN_df['Date'].unique()
    for c in province:
        grouped = VN_df.groupby(VN_df['Province'])
        df = grouped.get_group(c)  
        t_max = [df[df.Date == d][col].max() for d in days]
        t_min = [df[df.Date == d][col].min() for d in days]
        ls_max.append(t_max)
        ls_min.append(t_min)

    mean_prv_max=np.mean(np.array(ls_max), axis = 0)

    mean_prv_min=np.mean(np.array(ls_min), axis = 0)

    year = [np.datetime64(k, 'Y') for k in days]

    dt = pd.DataFrame({'Max':mean_prv_max, 'Min':mean_prv_min, 'Date': days})

    plt.figure(figsize = (20,8))
    # dt = pd.DataFrame({'Max':t_max, 'Min':t_min, 'Date': days})
    fig = px.line(dt, x='Date', y=['Max', 'Min']) # 'Mean':t_mean,

    fig.update_layout(
        width = 800,
        title=col+" Plot",
        xaxis_title="Days",
        yaxis_title=col + ' ' + '(' + unit_mapping[col] + ')',
        legend_title="Note",
        font=dict(
            family="Courier New, monospace",
            size=18))

    return fig

def PLotMinMaxMonth(VN_df, prv, col):
    
    VN_df = VN_df.rename(columns = {"year":"Year"})
    if prv != "All":
        df = VN_df[VN_df["Province"] == prv]
        max_df = df.groupby(["Month","Year"]).max()[col] 
        ind1 = sorted(max_df.index, key = lambda x: x[0])
        min_df = df.groupby(["Month","Year"]).min()[col]
        ind2 = sorted(min_df.index, key = lambda x: x[0])
    else:
        df = VN_df
        max_province = df.groupby(["Month","Year","Province"]).max().reset_index([0,1,2])
        max_df = max_province.groupby(["Month","Year"]).mean()[col]
        ind1 = sorted(max_df.index, key = lambda x: x[0])
        min_province = df.groupby(["Month","Year","Province"]).min().reset_index([0,1,2])
        min_df = min_province.groupby(["Month","Year"]).mean()[col]
        ind2 = sorted(min_df.index, key = lambda x: x[0])

    data = pd.merge(max_df[ind1] , min_df[ind2] , on=["Month","Year"], how='inner')

    x = data.reset_index(level=0)
    x = x.reset_index(level=0)
    # x["Time"] = x["Month"].astype(str) + "-" + x["Year"].astype(str)
    x = x.rename(columns = {f"{col}_x": "Max", f"{col}_y": "Min"}) 

    # t_mean = [HCM_df[HCM_df.Date == d]['Temperature(°C)'].mean() for d in days]
    
    plt.figure(figsize = (20,8))

    fig = px.line(x, x='Month', y=['Max', 'Min']) # 'Mean':t_mean,

    fig.update_layout(
        width = 800,
        title=col+" Plot",
        xaxis_title="Months",
        yaxis_title=col + ' ' + '(' + unit_mapping[col] + ')',
        legend_title="Note",
        font=dict(
            family="Courier New, monospace",
            size=18))

    return fig

def plotCountAndDistribution(data, feat_name):
    # f, axes = plt.subplots(2, 1, figsize=(8, 20))
    # a = sns.countplot(data, ax=axes[0])
    # a.set_xlabel(feat_name, fontsize=20)
    # a.set_ylabel("Count", fontsize=20)
    # b= sns.distplot(data, ax=axes[1])
    # b.set_xlabel(feat_name,fontsize=20)
    # b.set_ylabel("Density", fonstsize=20)
    max_val = data.max()
    print(data)
    sns.set(font_scale=1.3)
    fig = plt.figure(figsize = (8,4))
    b= sns.distplot(data, color = 'blue', bins = int(max_val))
    b.set_xlabel(feat_name + ' ' + '(' + unit_mapping[feat_name] + ')',fontsize=20)
    b.set_ylabel("Density", fontsize=20)

    return fig


def plot_5y_annualy(df, col):
    feat = df.groupby(["Year"]).mean()[col]
    ind = sorted(feat.index)

    x = feat[ind]
    x = x.reset_index(level=0)
    x["Time"] =  x["Year"].astype(str)
    print(x)
    plt.figure(figsize = (20,8))
    fig = px.line(x, x="Time", y=col)
    fig.update_layout(
        width = 800,
        yaxis_title=col + ' ' + '(' + unit_mapping[col] + ')',
        font=dict(
            
            family="Courier New, monospace",
            size=18))

    return fig

def plot_5y_monthly(df, col):
    feat = df.groupby(["Month","Year"]).mean()[col]
    ind = sorted(feat.index, key = lambda x: x[1])

    x = feat[ind].reset_index(level=0)
    x = x.reset_index(level=0)
    x["Time"] = x["Month"].astype(str) + "-" + x["Year"].astype(str)
    plt.figure(figsize = (20,8))
    fig = px.line(x, x="Time", y=col)
    fig.update_layout(
        width = 800,
        yaxis_title=col + ' ' + '(' + unit_mapping[col] + ')',
        font=dict(
            
            family="Courier New, monospace",
            size=18))

    return fig


def get_data_msn(tinh,path = r"../../data_sung/tinhthanh_1.xlsx"):
    data_tinh = pd.read_excel(path)
    tinh_id = data_tinh.iloc[1].to_dict()[tinh]
    try:
        url = "https://www.msn.com/vi-vn/weather/forecast/in-"+tinh_id.replace(" ","-")+",Việt-Nam"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        titles = soup.findAll('div', class_='overallContainer-E1_1')
        Time = titles[0].findAll('div', class_='labelUpdatetime-E1_1')[0].string
        Temp = titles[0].findAll('a', class_='summaryTemperatureCompact-E1_1 summaryTemperatureHover-E1_1')[0].get_text()[0:2]
        Humidity = titles[0].findAll('a', class_='detailItemGroup-E1_1 detailItemGroupHover-E1_1')[1].findAll('span')[-1].get_text()
        Pressure = titles[0].findAll('a', class_='detailItemGroup-E1_1 detailItemGroupHover-E1_1')[3].findAll('span')[-1].get_text()
        DewPoint = titles[0].findAll('a', class_='detailItemGroup-E1_1 detailItemGroupHover-E1_1')[4].findAll('span')[-1].get_text()
        Wind = (titles[0].findAll('a', class_='detailItemGroup-E1_1 detailItemGroupHover-E1_1')[0].findAll("div")[-1]).get_text()
        Dir = (titles[0].findAll('a', class_='detailItemGroup-E1_1 detailItemGroupHover-E1_1')[0].findAll("div")[-1]).find("svg")['style'].replace("transform:rotate(","").replace(")","")
    except:
        time.sleep(5)
        url = "https://www.msn.com/vi-vn/weather/forecast/in-"+tinh_id.replace(" ","-")+",Việt-Nam"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        titles = soup.findAll('div', class_='overallContainer-E1_1')
        Time = titles[0].findAll('div', class_='labelUpdatetime-E1_1')[0].string
        Temp = titles[0].findAll('a', class_='summaryTemperatureCompact-E1_1 summaryTemperatureHover-E1_1')[0].get_text()[0:2]
        Humidity = titles[0].findAll('a', class_='detailItemGroup-E1_1 detailItemGroupHover-E1_1')[1].findAll('span')[-1].get_text()
        Pressure = titles[0].findAll('a', class_='detailItemGroup-E1_1 detailItemGroupHover-E1_1')[3].findAll('span')[-1].get_text()
        DewPoint = titles[0].findAll('a', class_='detailItemGroup-E1_1 detailItemGroupHover-E1_1')[4].findAll('span')[-1].get_text()
        Wind = (titles[0].findAll('a', class_='detailItemGroup-E1_1 detailItemGroupHover-E1_1')[0].findAll("div")[-1]).get_text()
        Dir = (titles[0].findAll('a', class_='detailItemGroup-E1_1 detailItemGroupHover-E1_1')[0].findAll("div")[-1]).find("svg")['style'].replace("transform:rotate(","").replace(")","")

    return [Pressure,DewPoint + "C"]

