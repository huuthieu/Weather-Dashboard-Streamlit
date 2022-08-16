import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns

from cfg import *
from utils.format import formatDate


def plotVNdataDay(VN_df, col):
    VN_df = VN_df.rename(columns={"year": "Year"})
    VN_df = formatDate(VN_df)
    province = list(VN_df.Province.unique())
    ls = []
    days = VN_df["Date"].unique()
    for c in province:
        grouped = VN_df.groupby(VN_df["Province"])
        df = grouped.get_group(c)
        t_mean = [df[df.Date == d][col].mean() for d in days]
        ls.append(t_mean)

    mean_prv = np.mean(np.array(ls), axis=0)
    year = [np.datetime64(k, "Y") for k in days]

    plt.figure(figsize=(20, 10))
    dt = pd.DataFrame(
        {col: mean_prv, "Date": days}
    )  # np.arange(VN_df[col].min(),VN_df[col].max())
    fig = px.line(dt, x="Date", y=col)  # 'Mean':t_mean,

    fig.update_layout(
        # title='Compare the national average '+ col +  ' with ' + prv,
        width=900,
        xaxis_title="Days",
        yaxis_title=col + " " + "(" + unit_mapping[col] + ")",
        font=dict(family="Courier New, monospace", size=18),
    )
    return fig


def plotVNdataMonth(VN_df, col):
    VN_df = VN_df.rename(columns={"year": "Year"})
    data = VN_df.groupby(["Month", "Year"]).mean()[col]
    x = data.reset_index(level=0)
    x = x.reset_index(level=0)
    if col == "Rain":
        x[col] = x[col] * 24
    plt.figure(figsize=(20, 10))
    fig = px.line(x, x="Month", y=col)
    fig.update_layout(
        # title='Compare the national average '+ col +  ' with ' + prv,
        width=900,
        xaxis_title="Month",
        yaxis_title=col + " " + "(" + unit_mapping[col] + ")",
        font=dict(family="Courier New, monospace", size=18),
    )

    return fig


def PLotMinMaxDay(VN_df, prov, col):
    VN_df = formatDate(VN_df)
    if prov == "All":
        df = VN_df
    else:
        df = VN_df[VN_df["Province"] == prov]
    days = list(df["Date"].unique())

    province = list(df.Province.unique())
    ls_max = []
    ls_min = []
    days = VN_df["Date"].unique()
    for c in province:
        grouped = VN_df.groupby(VN_df["Province"])
        df = grouped.get_group(c)
        t_max = [df[df.Date == d][col].max() for d in days]
        t_min = [df[df.Date == d][col].min() for d in days]
        ls_max.append(t_max)
        ls_min.append(t_min)

    mean_prv_max = np.mean(np.array(ls_max), axis=0)

    mean_prv_min = np.mean(np.array(ls_min), axis=0)

    year = [np.datetime64(k, "Y") for k in days]

    dt = pd.DataFrame({"Max": mean_prv_max, "Min": mean_prv_min, "Date": days})

    plt.figure(figsize=(20, 8))
    # dt = pd.DataFrame({'Max':t_max, 'Min':t_min, 'Date': days})
    fig = px.line(dt, x="Date", y=["Max", "Min"])  # 'Mean':t_mean,

    fig.update_layout(
        width=800,
        title=col + " Plot",
        xaxis_title="Days",
        yaxis_title=col + " " + "(" + unit_mapping[col] + ")",
        legend_title="Note",
        font=dict(family="Courier New, monospace", size=18),
    )

    return fig


def PLotMinMaxMonth(VN_df, prv, col):

    VN_df = VN_df.rename(columns={"year": "Year"})
    if prv != "All":
        df = VN_df[VN_df["Province"] == prv]
        max_df = df.groupby(["Month", "Year"]).max()[col]
        ind1 = sorted(max_df.index, key=lambda x: x[0])
        min_df = df.groupby(["Month", "Year"]).min()[col]
        ind2 = sorted(min_df.index, key=lambda x: x[0])
    else:
        df = VN_df
        max_province = (
            df.groupby(["Month", "Year", "Province"])
            .max()
            .reset_index([0, 1, 2])
        )
        max_df = max_province.groupby(["Month", "Year"]).mean()[col]
        ind1 = sorted(max_df.index, key=lambda x: x[0])
        min_province = (
            df.groupby(["Month", "Year", "Province"])
            .min()
            .reset_index([0, 1, 2])
        )
        min_df = min_province.groupby(["Month", "Year"]).mean()[col]
        ind2 = sorted(min_df.index, key=lambda x: x[0])

    data = pd.merge(
        max_df[ind1], min_df[ind2], on=["Month", "Year"], how="inner"
    )

    x = data.reset_index(level=0)
    x = x.reset_index(level=0)
    # x["Time"] = x["Month"].astype(str) + "-" + x["Year"].astype(str)
    x = x.rename(columns={f"{col}_x": "Max", f"{col}_y": "Min"})

    # t_mean = [HCM_df[HCM_df.Date == d]['Temperature(°C)'].mean() for d in days]
    if col == "Rain":
        x[["Max", "Min"]] = x[["Max", "Min"]] * 24
    plt.figure(figsize=(20, 8))

    fig = px.line(x, x="Month", y=["Max", "Min"])  # 'Mean':t_mean,

    fig.update_layout(
        width=800,
        title=col + " Plot",
        xaxis_title="Months",
        yaxis_title=col + " " + "(" + unit_mapping[col] + ")",
        legend_title="Note",
        font=dict(family="Courier New, monospace", size=18),
    )

    return fig


def plotCountAndDistribution(data, feat_name):
    max_val = data.max()
    sns.set(font_scale=1.3)
    fig = plt.figure(figsize=(8, 4))
    b = sns.distplot(data, color="blue", bins=int(max_val))
    b.set_xlabel(
        feat_name + " " + "(" + unit_mapping[feat_name] + ")", fontsize=20
    )
    b.set_ylabel("Density", fontsize=20)

    return fig


def plot_5y_annualy(df, col):
    feat = df.groupby(["Year"]).mean()[col]
    ind = sorted(feat.index)

    x = feat[ind]
    x = x.reset_index(level=0)
    x["Time"] = x["Year"].astype(str)
    if col == "Rain":
        x[col] = x[col] * 24 * 12
    plt.figure(figsize=(20, 8))
    fig = px.line(x, x="Time", y=col)
    fig.update_layout(
        width=800,
        yaxis_title=col + " " + "(" + unit_mapping[col] + ")",
        font=dict(family="Courier New, monospace", size=18),
    )

    return fig


def plot_5y_monthly(df, col):
    feat = df.groupby(["Month", "Year"]).mean()[col]
    ind = sorted(feat.index, key=lambda x: x[1])

    x = feat[ind].reset_index(level=0)
    x = x.reset_index(level=0)
    x["Time"] = x["Month"].astype(str) + "-" + x["Year"].astype(str)
    if col == "Rain":
        x[col] = x[col] * 24
    plt.figure(figsize=(20, 8))
    fig = px.line(x, x="Time", y=col)
    fig.update_layout(
        width=800,
        yaxis_title=col + " " + "(" + unit_mapping[col] + ")",
        font=dict(family="Courier New, monospace", size=18),
    )

    return fig


def compareWithNationalInDay(VN_df, prv, col):
    if prv == "All":
        return plotVNdataDay(VN_df, col)
    VN_df = formatDate(VN_df)
    province = list(VN_df.Province.unique())
    ls = []
    days = VN_df["Date"].unique()
    m = []
    for c in province:
        grouped = VN_df.groupby(VN_df["Province"])
        df = grouped.get_group(c)
        if c == prv:
            m = [df[df.Date == d][col].mean() for d in days]
        t_mean = [df[df.Date == d][col].mean() for d in days]
        ls.append(t_mean)

    mean_prv = np.mean(np.array(ls), axis=0)
    year = [np.datetime64(k, "Y") for k in days]

    plt.figure(figsize=(20, 10))
    dt = pd.DataFrame(
        {prv: m, "VN": mean_prv, "Date": days}
    )  # np.arange(VN_df[col].min(),VN_df[col].max())
    fig = px.line(dt, x="Date", y=[prv, "VN"])  # 'Mean':t_mean,

    fig.update_layout(
        # title='Compare the national average '+ col +  ' with ' + prv,
        width=900,
        xaxis_title="Days",
        yaxis_title=col + " " + "(" + unit_mapping[col] + ")",
        legend_title="Note",
        font=dict(family="Courier New, monospace", size=18),
    )
    return fig


def compareWithNationalInMonth(VN_df, prv, col):
    if prv == "All":
        return plotVNdataMonth(VN_df, col)
    VN_df = VN_df.rename(columns={"year": "Year"})
    prov_data = (
        VN_df[VN_df["Province"] == prv].groupby(["Month", "Year"]).mean()[col]
    )
    ind1 = sorted(prov_data.index, key=lambda x: x[0])
    data = VN_df.groupby(["Month", "Year"]).mean()[col]
    ind2 = sorted(data.index, key=lambda x: x[0])
    data = pd.merge(
        data[ind2], prov_data[ind1], on=["Month", "Year"], how="inner"
    )
    # ind = sorted(data.index, key = lambda x: x[0])
    # print(ind)
    # print(data)

    x = data.reset_index(level=0)
    x = x.reset_index(level=0)
    # x["Time"] = x["Month"].astype(str) + "-" + x["Year"].astype(str)
    x = x.rename(columns={f"{col}_x": "VN", f"{col}_y": prv})
    if col == "Rain":
        x[["Vn", prv]] = x[["VN", prv]] * 24
    plt.figure(figsize=(20, 10))
    fig = px.line(x, x="Month", y=[prv, "VN"])
    fig.update_layout(
        # title='Compare the national average '+ col +  ' with ' + prv,
        width=900,
        xaxis_title="Month",
        yaxis_title=col + " " + "(" + unit_mapping[col] + ")",
        legend_title="Note",
        font=dict(family="Courier New, monospace", size=18),
    )

    return fig
