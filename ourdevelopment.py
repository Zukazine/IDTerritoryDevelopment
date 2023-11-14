import geopandas as gpd
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import folium_static

def embed_map(m, file_name):
    from IPython.display import IFrame
    m.save(file_name)
    return IFrame(file_name, width='100%', height='500px')

def load_province():
    df = pd.read_csv('daftar_nama_daerah.csv')
    return df.iloc[:33] 

def load_map(loc=[-2.4833826, 117.8902853]):
    m = folium.Map(location=loc, zoom_start=7)
    return m

def zoom_to_province(province, m):
    provinces = load_province()
    province_coordinates = {}
    
    for i in range(len(provinces)):
        province_coordinates[provinces.iloc[i]['name']] = {
            'location': [provinces.iloc[i]['latitude'], provinces.iloc[i]['longitude']],
            'zoom' : 10
        }
    
    if province in province_coordinates:
        loc = province_coordinates[province]['location']
        zoom_level = province_coordinates[province]['zoom']
        m.location = loc
        m.zoom_start = zoom_level
        return m
    else:
        st.warning("Provinsi tidak ditemukan.")

def main():
    st.title('Aplikasi Peta Provinsi')

    my_map = load_map()

    provinces = load_province()
    list_of_provinces = []
    for i in range(len(provinces)):
        list_of_provinces.append(provinces.iloc[i]['name'])
 
    province = st.selectbox('Pilih Provinsi', list_of_provinces)
    my_map = load_map(provinces.loc[provinces['name'] == province][['latitude','longitude']])

    if st.button('Zoom to Province'):
        my_map = zoom_to_province(province, my_map)

    folium_static(my_map)

if __name__ == '__main__':
    main()