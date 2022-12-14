import pandas as pd
import streamlit as st

from cfg import *

st.set_page_config(page_title="DataFrame Visualize", page_icon="📊")

st.markdown("# DataFrame Visualize")
st.sidebar.header("DataFrame Visualize")
# st.write(
#     """This demo shows how to use `st.write` to visualize Pandas DataFrames.
# (Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
# )


@st.cache
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_path)


col1, col2 = st.columns(2)
with col1:
    option1 = st.selectbox("Choose year", tuple(list_years[1:]))

with col2:
    # st.subheader("Choose province")
    option2 = st.selectbox("Choose province", tuple(list_provinces))


df = get_data()
data = df[(df.Province == option2) & (df.Year == int(option1))]


rename_dict = {u: u + " " + "(" + v + ")" for u, v in unit_mapping.items()}
data.rename(columns=rename_dict, inplace=True)

# data /= 1000000.0
st.write("### Weather Data of Vietnam", data.sort_index())
