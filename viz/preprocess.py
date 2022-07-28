import pandas as pd
import os

def split_m1(x):
    x = str(x)
    if len(x) == 7:
        return  x[0]
    else:
        return str(int(x[:2]))

def split_d1(x):
    x = str(x)
    if len(x) == 7:
        return str(int(x[1:3]))
    else:
        return str(int(x[2:4]))

def split_y1(x):
    x = str(x)
    if len(x) == 7:
        return x[3:]
    else:
        return x[4:]

def split(x):
    x = str(x)
    if len(x) == 7:
        return x[0]
    else:
        return x[:2]

def split_m(x):
    x = str(x)
    if len(x) == 7:
        return str(int(x[1:3]))
    else:
        return str(int(x[2:4]))

def split_y(x):
    x = str(x)
    if len(x) == 7:
        return x[3:]
    else:
        return x[4:]


def process_data_world_sung(data):
    data["Day"] = data["Date"].apply(split_d1)
    data["Month"] = data["Date"].apply(split_m1)
    data["year"] = data["Date"].apply(split_y1)
    data = data.drop(columns=["Date","Sunrise", "Sunset", "Moonrise", "Moonset","Icon", "Forecast"])
    return data


def parse_all_province(year):
    path = f"../../data/{year}"
    first = True
    for file in os.listdir(path):
        if file.endswith(".csv") and file != "weather_data_[2020].csv" and file != "worldweatheronline2021.csv" and "VietNam" not in file:
            if first:
                data = pd.read_csv(f"{path}/{file}")
                data["Province"] = file.split("_")[2]
                data = data.rename(columns={"Thời gian": "Time",'date':"Day","month":"Month", "Độ ẩm tương đối":"Humidity", "Điểm sương":"Dew point"})
                data["Humidity"] = data.Humidity.astype(str).apply(lambda x: x.strip("%")).astype(float)
                data["Dew point"] = data["Dew point"].astype(str).apply(lambda x: x.strip("°C")).astype(float)
                data["Humidity"] = data["Humidity"].fillna(data["Humidity"].mean())
                data["Dew point"] = data["Dew point"].fillna(data["Dew point"].mean())
                
                first = False
            else:
                # print(file)
                tmp = pd.read_csv(f"{path}/{file}")
                tmp["Province"] = file.split("_")[2]
                tmp = tmp.rename(columns={"Thời gian": "Time",'date':"Day","month":"Month", "Độ ẩm tương đối":"Humidity", "Điểm sương":"Dew point"})
                tmp["Humidity"] = tmp.Humidity.astype(str).apply(lambda x: x.strip("%")).astype(float)
                tmp["Dew point"] = tmp["Dew point"].astype(str).apply(lambda x: x.strip("°C")).astype(float)
                tmp["Humidity"] = tmp["Humidity"].fillna(tmp["Humidity"].mean())
                tmp["Dew point"] = tmp["Dew point"].fillna(tmp["Dew point"].mean())
                data = data.append(tmp, ignore_index=True)
                
            print(f"{file} done")
    return data
        



# data_sung = pd.read_csv("/home/primedo/hcmus/DA/Datascience_2016-2/data_sung/worldweatheronline2021.csv")
# data_sung = process_data_world_sung(data_sung)

# data_thieu = pd.read_csv("")
# data_thieu = data_thieu.rename(columns={"Thời gian": "Time",'date':"Day","month":"Month"})

# data_thieu["Day"] = data_thieu["Day"].astype(str)
# data_thieu["Month"] = data_thieu["Month"].astype(str)
# data_thieu["year"] = data_thieu["year"].astype(str)

# merged_df = pd.merge(data_thieu , data_sung , on=['Time',"Day","Month","Province","year"], how='inner')

# merged_df.drop_duplicates(subset=['Time',"Day","Month","Province","year"], keep='first', inplace=True, ignore_index=True)

# merged_df = merged_df.drop(columns = ["Rain%","Gió","Gió giật","Nhiệt độ tương đối","Nhiệt độ","Áp suất","Biểu tượng"])

def split_temperature(x):
    if type(x) == float:
        return x
    x = x.split("°")[0]
    return float(x)

def split_humidity(x):
    if type(x) == float:
        return x
    x = x.strip("%")
    return x

def split_dew_point(x):
    if type(x) == float:
        return x
    x = x.strip("°C")
    return x

def split_rain(x):
    if type(x) == float:
        return x
    x = x.strip("mm")
    return x

def split_wind(x):
    if type(x) == float:
        return x
    x = x.strip("km/h")
    return x

def split_pressure(x):
    if type(x) == float:
        return x
    x = x.strip("mb")
    return x

def split_cloud(x):
    if type(x) == float:
        return x
    x = x.strip("%")
    return x

def split_gust(x):
    if type(x) == float:
        return x
    x = x.strip("km/h")
    return x

def split_dir(x):
    if type(x) == float:
        return x
    x = x.strip("deg")
    return x

def process_merged_data(merged_df):

    merged_df["Humidity"] = merged_df["Humidity"].apply(lambda x: x.strip("%")).astype(float)
    merged_df["Dew point"] = merged_df["Dew point"].apply(lambda x: x.strip("°C")).astype(float)
    merged_df["Rain"] = merged_df["Rain"].apply(lambda x: x.strip("mm")).astype(float)
    merged_df["Cloud"] = merged_df["Cloud"].apply(lambda x: x.strip("%")).astype(float)
    merged_df["Pressure"] = merged_df["Pressure"].apply(lambda x: x.strip("mb")).astype(float)
    merged_df["Wind"] = merged_df["Wind"].apply(lambda x: x.strip("km/h")).astype(float)
    merged_df["Gust"] = merged_df["Gust"].apply(lambda x: x.strip("km/h")).astype(float)
    merged_df["Dir"] = merged_df["Dir"].apply(lambda x: x.strip("deg")).astype(float)
    merged_df["Temperature"] = merged_df["Temperature"].apply(split_temperature)

    merged_df.to_csv("merged_data.csv", index=False)

def process_data(df, save = False):
    print(df)
    df["Humidity"] = df["Humidity"].apply(split_humidity).astype(float)
    df["Dew point"] = df["Dew point"].apply(split_dew_point).astype(float)
    df["Rain"] = df["Rain"].apply(split_rain).astype(float)
    df["Cloud"] = df["Cloud"].apply(split_cloud).astype(float)
    df["Pressure"] = df["Pressure"].apply(split_pressure).astype(float)
    df["Wind"] = df["Wind"].apply(split_wind).astype(float)
    df["Gust"] = df["Gust"].apply(split_gust).astype(float)
    df["Dir"] = df["Dir"].apply(split_dir).astype(float)
    df["Temperature"] = df["Temperature"].apply(split_temperature)
    if save:
        df.to_csv("../../data/vietnam/vietnam_[2017-2022]_fix.csv", index=False)
    else:
        return df

if __name__ == "__main__":
    data = pd.read_csv("../../data/vietnam/vietnam[2017-2022].csv")
    process_data(data)