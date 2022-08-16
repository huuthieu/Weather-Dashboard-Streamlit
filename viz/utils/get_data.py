import requests
from bs4 import BeautifulSoup
from time import time
import streamlit as st
import pandas as pd

from cfg import *


@st.experimental_memo
def get_data(
    dataset_path=dataset_path, feature=None, year=None
) -> pd.DataFrame:
    data = pd.read_csv(dataset_path)
    if feature is None and year is None:
        return data
    data = data[data["Year"] == int(year)]
    return data[["Time", "Month", feature, "Province"]]


def parse_data_msn(tinh_id):
    url = (
        "https://www.msn.com/vi-vn/weather/forecast/in-"
        + tinh_id.replace(" ", "-")
        + ",Việt-Nam"
    )
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    titles = soup.findAll("div", class_="overallContainer-E1_1")
    # Time = (
    #     titles[0].findAll("div", class_="labelUpdatetime-E1_1")[0].string
    # )
    # Temp = (
    #     titles[0]
    #     .findAll(
    #         "a",
    #         class_="summaryTemperatureCompact-E1_1 summaryTemperatureHover-E1_1",
    #     )[0]
    #     .get_text()[0:2]
    # )
    # Humidity = (
    #     titles[0]
    #     .findAll(
    #         "a", class_="detailItemGroup-E1_1 detailItemGroupHover-E1_1"
    #     )[1]
    #     .findAll("span")[-1]
    #     .get_text()
    # )
    Pressure = (
        titles[0]
        .findAll("a", class_="detailItemGroup-E1_1 detailItemGroupHover-E1_1")[
            3
        ]
        .findAll("span")[-1]
        .get_text()
    )
    DewPoint = (
        titles[0]
        .findAll("a", class_="detailItemGroup-E1_1 detailItemGroupHover-E1_1")[
            4
        ]
        .findAll("span")[-1]
        .get_text()
    )
    # Wind = (
    #     titles[0]
    #     .findAll(
    #         "a", class_="detailItemGroup-E1_1 detailItemGroupHover-E1_1"
    #     )[0]
    #     .findAll("div")[-1]
    # ).get_text()
    # Dir = (
    #     (
    #         titles[0]
    #         .findAll(
    #             "a",
    #             class_="detailItemGroup-E1_1 detailItemGroupHover-E1_1",
    #         )[0]
    #         .findAll("div")[-1]
    #     )
    #     .find("svg")["style"]
    #     .replace("transform:rotate(", "")
    #     .replace(")", "")
    # )

    return Pressure, DewPoint


def get_data_msn(tinh, path=province_msn):

    data_tinh = pd.read_excel(path)
    tinh_id = data_tinh.iloc[1].to_dict()[tinh]
    try:
        Pressure, DewPoint = parse_data_msn(tinh_id)
    except:
        time.sleep(5)
        Pressure, DewPoint = parse_data_msn(tinh_id)
    return [Pressure, DewPoint + "C"]
