import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to our Vietnamese Weather Analysis Dashboard! 👋")

st.sidebar.success("Select a demo above.")

col1, col2, col3 = st.columns(3)

with col1:
    st.image("/home/primedo/hcmus/DA/Datascience_2016-2/code/viz/img1.jpg", width = 800)
    

with col2:
    st.write(" ")

with col3:
    st.write(" ")


