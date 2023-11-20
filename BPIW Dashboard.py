import geopandas as gpd
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import folium_static

st.set_page_config(
    page_title="BPIW Dashboard",
    page_icon="🌐",
)

st.write("# Welcome to Our Dashboard! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Dashboard ini digunakan untuk Visualisasi data geospasial, 
    Analisis data spasial, dan Memberikan insight ide untuk pengembangan lebih lanjut.
    **Disclaimer** : website ini masih dalam pengembangan awal (beta) dan website untuk saat ini mohon tidak disebarkan terlebih dahulu.
    
    **👈 pilih menu yang terletak di sidebar** untuk melihat contoh
    apa yang bisa dashboard ini lakukan
    ### Link penting untuk pengembangan
    - Source code via Github (https://github.com/Zukazine/IDTerritoryDevelopment)
    - [Project Bard](https://docs.google.com/spreadsheets/d/1mqTl9bZ6nPo2ACKrcziUDmlw8OhoD4fWzuUVVDSE6ug/edit#gid=1115838130)
    #### Contoh Visualisasi Geospasial (static image)
"""
)


st.markdown('##### Choropleth')
st.image('images/example.PNG')

st.markdown('')
st.markdown('##### Distribution')
st.image('images/example_2.PNG')

st.markdown('')
st.markdown('##### Value Plotting')
st.image('images/example_3.PNG')
