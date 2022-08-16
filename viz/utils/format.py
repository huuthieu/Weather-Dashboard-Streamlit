import pandas as pd

def rounding_time(hour):
    time_list = [0, 3, 6, 9, 12, 15, 18, 21]
    min_dis = 30
    round_h = 0
    for i in range(len(time_list)):
        if abs(hour - time_list[i]) < min_dis:
            min_dis = abs(hour - time_list[i])
            round_h = time_list[i]
    return int(round_h)


def formatDate(df):
    # Changing Formatted Date from String to Datetime
    df = df.rename(columns={"year": "Year"})
    t = [
        str(df["Year"][k])
        + "-"
        + str(df["Month"][k])
        + "-"
        + str(df["Day"][k])
        + " "
        + str(df["Time"][k])
        for k in range(len(df))
    ]
    df["Formatted Date"] = pd.to_datetime(t, utc=True)

    d = [
        str(df["Year"][k])
        + "-"
        + str(df["Month"][k])
        + "-"
        + str(df["Day"][k])
        for k in range(len(df))
    ]
    df["Date"] = pd.to_datetime(d, format="%Y-%m-%d")
    df = df.sort_values(by="Formatted Date")

    RAIN_LABEL = [
        "Light drizzle",
        "Light rain",
        "Light rain shower",
        "Patchy light drizzle",
        "Patchy light rain",
        "Patchy light rain with thunder",
        "Patchy rain possible",
        "Heavy rain",
        "Heavy rain at times",
        "Moderate or heavy rain shower",
        "Moderate rain",
        "Moderate rain at times",
        "Overcast",
        "Torrential rain shower",
    ]
    tmp = []
    for i, value in enumerate(df["Weather"]):
        if value in RAIN_LABEL:
            tmp.append(1)
        else:
            tmp.append(0)
    df["Label"] = tmp
    # df.reset_index(inplace=True)
    return df



