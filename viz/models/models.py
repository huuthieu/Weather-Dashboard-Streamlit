import json

import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.model_selection import train_test_split

from cfg import *
from models.cfg import *

df = pd.read_csv(dataset_path)


def convert_label(x):
    if x in RAINY_LABEL:
        return "yes"
    else:
        return "no"


def convert_weather(x):
    if x in RAINY_LABEL:
        return "rainy"
    else:
        return "sunny"


def normalize(df):
    result = df.copy()
    for feature_name in df.columns:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (df[feature_name] - min_value) / (
            max_value - min_value
        )
    return result


def normalize1(df, df1):
    result = df1.copy()
    for feature_name in df.columns:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (df1[feature_name] - min_value) / (
            max_value - min_value
        )
    return result


def convert_category2numeric(data, columns_name):
    for col in columns_name:
        data = pd.concat(
            (data, pd.get_dummies(data[col], prefix=col, drop_first=True)),
            axis=1,
        )
        data = data.drop([col], axis=1)
    return data


def prepare(df, prv, data_test):
    if prv != "All":
        df = df.loc[df["Province"] == prv]

    df = df.loc[df["Year"] != 2019]
    df = df.loc[df["Year"] != 2018]
    df = df.loc[df["Year"] != 2017]
    df = df.sort_values(
        by=["Province", "Year", "Month", "Day", "Time"], ignore_index=True
    )

    label = df["Weather"]
    features = df
    features = features[:-1]
    label = label[1:]
    data = features
    data["Label"] = label.values
    data["Label"] = data["Label"].apply(convert_label)
    # data["Weather"] = data["Weather"].apply(convert_weather)
    data = data.drop(["Province"], axis=1)

    data_test["Label"] = "yes"
    data = data.append(data_test, ignore_index=True)
    data["Weather"] = data["Weather"].apply(convert_weather)

    # Normal
    col = [i for i in data.columns if data[[i]].dtypes[0] == float]
    data[col] = normalize(data[col])

    ##
    data = convert_category2numeric(
        data, ["Time", "Weather", "Month", "Year", "Day"]
    )
    data = pd.concat(
        (data, pd.get_dummies(data["Label"], drop_first=True)), axis=1
    )
    data = data.drop(["Label"], axis=1)

    data = sm.add_constant(data)
    data_test = data[-1:]
    data = data[:-1]

    all_columns = data.columns.to_list()
    Y_colums = ["yes"]
    X_colums = [x for x in all_columns if x not in Y_colums]
    # train_set, test_set = train_test_split(data, test_size=0.2)
    data_test = data_test.drop(["yes"], axis=1)
    return data, data_test, X_colums, Y_colums


def train(train_set, X_colums, Y_colums):
    done = True
    while done:
        Xtrain = train_set[X_colums]
        ytrain = train_set[Y_colums]

        # building the model and fitting the data
        log_reg = sm.Logit(ytrain.astype(float), Xtrain.astype(float)).fit()
        if max(log_reg.pvalues.to_list()) > 0.05:
            X_colums.remove(
                max(
                    log_reg.pvalues.to_dict(),
                    key=log_reg.pvalues.to_dict().get,
                )
            )
        else:
            done = False
    return log_reg


def predict(log_reg, data):
    keys = log_reg.params.keys()
    data = data[keys]
    yhat = log_reg.predict(data)
    return yhat.values[0]


def pipeline(df, data_test, prv):
    train_set, data_test, X_colums, Y_colums = prepare(df, prv, data_test)
    log_reg = train(train_set, X_colums, Y_colums)
    return predict(log_reg, data_test)
