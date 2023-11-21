import streamlit as st
import geopandas as gpd
import folium
import math
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

st.set_page_config(layout="wide") 

st.title('SDA Dashboard 🌊')

left, right = st.columns(2)

with left:
    province = st.selectbox('Pilih Provinsi', ['Sulawesi Selatan', 'Lampung', 'Jawa Tengah', 'Bali', 'Aceh','Sumatera Utara', 'Sumatera Selatan', 'Banten', 'Nusa Tenggara Barat', 'Kalimantan Selatan', 'Jawa Timur', 'Daerah Istimewa Yogyakarta', 'Sumatera Barat', 'Jawa Barat', 'Sulawesi Utara', 'Bangka Belitung', 'Bengkulu', 'Gorontalo', 'Jambi', 'Kalimantan Tengah', 'Kepulauan Riau', 'Maluku', 'Maluku Utara', 'Nusa Tenggara Timur', 'Riau', 'Papua Barat', 'Sulawesi Barat', 'Sulawesi Tengah'])

with right:
    sector = st.selectbox('Pilih Sektor SDA', ['Irigasi'])

def read_data():
    data = gpd.read_file('dataset/irrigation.shp')
    return data

def marker():
    if 'water_data' not in st.session_state:
        st.session_state.water_data = read_data() 

    water = st.session_state.water_data
    
    m = folium.Map(location=[0.7893,113.9213], zoom_start=5)

    mc = MarkerCluster()

    for idx, row in water.iterrows():
        if not math.isnan(row['koord_x']) and not math.isnan(row['koord_y']):
            mc.add_child(folium.Marker([row['koord_y'], row['koord_x']], 
                                    tooltip='{}<br> Luas Daerah : {}'.format(row['nm_inf'], row['luas_ha']))).add_to(m)
            
    folium.plugins.Fullscreen(
    position="topright",
    title="Expand me",
    title_cancel="Exit me",
    force_separate_button=True,
    ).add_to(m)

    return m

if province and sector:
    with st.spinner('Constructing ...'):
        folium_static(marker(), width=850, height=400)

    with st.expander("**Penjelasan Parameter Prioritasisasi**"):
        st.markdown('Berikut merupakan parameter yang digunakan sehingga peta prioritas bisa terbentuk : ')

    with st.expander("**Ide Pengembangan**"):
        st.markdown('''
                    #### Pemetaan dan Pemilihan Lokasi Optimal ✅
                    ML dapat membantu dalam pemetaan wilayah yang optimal untuk pembangunan sistem irigasi baru berdasarkan analisis data spasial seperti topografi, pola tanam, dan tingkat curah hujan. Ini membantu dalam menentukan lokasi yang paling cocok untuk efisiensi maksimum.
                    
                    #### Prediksi Kebutuhan Air (simulatif)
                    Menggunakan ML untuk menganalisis data historis cuaca, pola tanam, dan karakteristik tanah dalam suatu wilayah untuk memprediksi kebutuhan air di masa depan. Ini bisa membantu perencanaan irigasi untuk menyesuaikan pasokan air secara efisien.

                    #### Optimasi Penggunaan Air       
                    ML dapat mengoptimalisasi penggunaan air irigasi dengan memanfaatkan data spasial seperti citra satelit, mengidentifikasi area yang membutuhkan air lebih banyak atau kurang. Sistem ini dapat memberikan rekomendasi penggunaan air yang lebih efisien.

                    #### Monitoring dan Pemeliharaan
                    Pemanfaatan AI untuk monitoring berkelanjutan wilayah irigasi. Dengan sensor-sensor dan teknologi IoT, AI dapat mengidentifikasi masalah potensial seperti kebocoran atau penggunaan air yang tidak efisien, memungkinkan respons cepat untuk pemeliharaan.

                    #### Pengelolaan Resiko dan Prediksi Bencana
                    Dengan ML, bisa dibangun model untuk memprediksi risiko kekeringan, banjir, atau perubahan iklim lainnya yang dapat mempengaruhi wilayah irigasi. Ini memungkinkan pihak terkait untuk mengambil langkah-langkah pencegahan atau penyesuaian.

                    #### Pengembangan Sistem Pemantauan Otomatis
                    AI dapat digunakan untuk mengembangkan sistem pemantauan otomatis yang mengirimkan pemberitahuan langsung jika terjadi masalah seperti penurunan tekanan air atau gangguan lain dalam sistem irigasi.
                    ''')
        
        st.markdown('')
        st.markdown(
                    '''
                    Melalui pemanfaatan data spasial, ML, dan AI, perencanaan, pengelolaan, dan pengembangan wilayah irigasi dapat dioptimalkan untuk efisiensi yang lebih tinggi dan penggunaan sumber daya yang lebih baik.
                    '''
                    )
