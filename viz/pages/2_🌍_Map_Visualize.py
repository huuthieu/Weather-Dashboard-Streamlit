from pyparsing import col
import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
import json
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go

import plotly.io as pio
from plotly.subplots import make_subplots

import numpy as np

from utils import *

st.set_page_config(page_title="Map Visualize", page_icon="🌍")

st.markdown("# Map Visualize")
st.sidebar.header("Map Visualize")
# st.write(
#     """This demo shows how to use
# [`st.pydeck_chart`](https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart)
# to display geospatial data."""
# )

col1, col2, col3 = st.columns(3)
with col1:
    option1 = st.selectbox(
     'Choose year',
     tuple(list_years[1:]))

with col2:
    # st.subheader("Choose month")
    option2 = st.selectbox(
     'Choose month',
     tuple(list_months))

with col3:
    # st.subheader("Choose feature")
    option3 = st.selectbox(
     'Choose feature',
        tuple(list_features))

@st.experimental_memo
def get_data(feature, year) -> pd.DataFrame:
    dataset_path = "../../data/vietnam/vietnam_[2017-2022]_fix.csv"
    data = pd.read_csv(dataset_path)

    data = data[data["Year"] == int(year)]
    return data[["Time","Month",feature,"Province"]]

gdf_vn = gpd.read_file('/home/primedo/hcmus/DA/Datascience_2016-2/Vietnam_covid19_maps/Vietnam_provinces.geojson')


data = get_data(option3, option1)


st.markdown(f"### Visualize {option3} in Vietnamese map")

with st.spinner('Wait for it...'):

    data["Name"] = data["Province"].map(name_dict_ve)
    x = data.groupby(["Name","Month"]).mean()[option3].reset_index(level = [0,1])

    x = x[x["Month"] == int(option2)]

    vn_data = gdf_vn.merge(x[["Name",option3]], on='Name', how='left')


    plot_data = json.dumps(json.loads(vn_data.to_json()))


    from bokeh.io import output_notebook, show, output_file
    from bokeh.plotting import figure
    from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
    from bokeh.palettes import brewer
    from bokeh.models.annotations import Title

    geosource = GeoJSONDataSource(geojson=plot_data)

    palette = brewer['RdBu'][9]

    color_mapper = LinearColorMapper(palette=palette, low=0, high=np.ceil(1.2 * x[option3].max()))

    tick_labels = {
        '0': '0', '0.5': '', '1': '1', '1.5': '', 
        '2':'2', '2.5': '2.5', '3':'3', '4':'4', 
        '5':'5', '6':'6','7':'7', '8': '8'
    }

    color_bar = ColorBar(
        color_mapper=color_mapper, 
        label_standoff=8,
        width=300, 
        height = 20,
        border_line_color=None, 
        location = (0,0), 
        orientation = 'horizontal', 
        major_label_overrides = tick_labels
    )


    title = Title()
    # Tùy theo giá trị muốn vẽ mà thay đổi tiêu đề cho phù hợp
    title.text = f"Temperature of Vietnam on {month_dict[option2]}"
    title.text_font_size = '16pt'
    title.align = "center"

    p = figure(
        title=title, 
        title_location='above',
        plot_height=500 , 
        plot_width=450, 
        toolbar_location=None
    )

    # tinh chỉnh một số thuộc tính của hai trục
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.xaxis.axis_label = 'Longitude'
    p.xaxis.axis_label_text_font_size = "14pt"
    p.yaxis.axis_label = 'Latitude'
    p.yaxis.axis_label_text_font_size = "14pt"
    p.yaxis.major_label_text_font_size = "12pt"
    p.xaxis.major_label_text_font_size = "12pt"


    p.patches(
        xs='xs',
        ys='ys', 
        source=geosource,
        fill_color = {'field' : option3, 'transform' : color_mapper}, # plot_data là field dùng để  quy định độ đậm nhạt màu tô
        line_color = 'black', 
        line_width = 0.25, 
        fill_alpha = 1
    )

    p.add_layout(color_bar, 'above')
    
    st.bokeh_chart(p)

# st.markdown("### Deep Dive")

# col1, col2 = st.columns(2)

# with col1:
pio.templates.default = "plotly_white"
ncols = 2
fig = make_subplots(rows=1, cols=2, shared_yaxes=True)

st.write(f"### Top 3 province have the highest/lowest {option3}")
top3 = x.sort_values(by= option3, ascending=False).head(3)
top3["Province"] = top3["Name"].map(name_dict_ev)
# fig1 = px.bar(        
#     top3,
#     y = option3,
#     x = "Province",
#     # color="Province"
#     # orientation = 'h' #Optional Parameter
# )

# fig1 = go.Figure(go.Bar(
#             x=top3["Province"],
#             y=top3[option3],
#             # orientation='h')
#             ))


# fig1.update_layout(
# autosize=False,
# width=400,
# height=400,
# yaxis2=dict(anchor='free', position=0.02,
#                             side='right'),
# font=dict(
#         size=15
#     )
# )

# st.plotly_chart(fig)

fig.add_trace(go.Bar(
            marker_color=px.colors.qualitative.G10[1],
            name = f"Highest {option3}",
            x=top3["Province"],
            y=top3[option3],
            showlegend=True,
            # orientation='h')
            ), row = 1, col=1)

# with col2:

# st.write(f"#### Top 3 province have the lowest {option3}")
top3 = x.sort_values(by=option3, ascending=True).head(3)
top3["Province"] = top3["Name"].map(name_dict_ev)

# fig2 = px.bar(        
#     top3,
#     y = option3,
#     x = "Province",
#     # color="Province"
#     # orientation = 'h' #Optional Parameter
# )

# fig2 = go.Figure(go.Bar(
#             x=top3["Province"],
#             y=top3[option3],
#             # orientation='h')
#  ) )  

# fig2.update_layout(
# autosize=False,
# width=400,
# height=400,
# yaxis2=dict(anchor='free', position=0.02,
#                             side='right'),
# font=dict(
#         size=15
#     )
# )    

fig.add_trace(go.Bar
(           
            marker_color=px.colors.qualitative.G10[0],
            name = f"Lowest {option3}",
            x=top3["Province"],
            y=top3[option3],
            showlegend=True,
            # orientation='h')
            ), row = 1, col=2)

st.plotly_chart(fig)