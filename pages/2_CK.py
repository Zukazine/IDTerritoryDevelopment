import geopandas as gpd
import folium
import streamlit as st
from folium.plugins import MarkerCluster
import math

st.set_page_config(layout="wide") 

st.title('Cipta Karya Dashboard 🌊')

left, right = st.columns(2)

with left:
    province = st.selectbox('Pilih Provinsi', ['Banten', 'DI Yogyakarta', 'Jawa Barat', 'Jawa Tengah', 'Jawa Timur', 'Kalimantan Barat', 'Kalimantan Tengah', 'Kalimantan Selatan', 'Kalimantan Timur', 'Kalimantan Utara', 'Aceh', 'Sumatera Utara', 'Sumatera Barat', 'Riau', 'Kep. Riau', 'Bengkulu', 'Jambi', 'Sumatera Selatan', 'Kep. Bangka Belitung', 'Lampung', 'Sulawesi Utara', 'Gorontalo', 'Sulawesi Tengah', 'Sulawesi Barat', 'Sulawesi Tenggara', 'Sulawesi Selatan', 'Bali', 'Nusa Tenggara Barat', 'Nusa Tenggara Timur', 'Maluku','Maluku Utara', 'Papua', 'Papua Barat'])

with right:
    sector = st.selectbox('Pilih Sektor CK', ['TPA'])

def read_data():
    data = gpd.read_file('dataset/complete_tpa.geojson')
    return data

def marker():
    if 'tpa_data' not in st.session_state:
        st.session_state.tpa_data = read_data() 

    tpa = st.session_state.tpa_data
    
    m = folium.Map(location=[0.7893,113.9213], zoom_start=5)


    mc = MarkerCluster()

    for idx, row in tpa.iterrows():
        if not math.isnan(row['koord_x']) and not math.isnan(row['koord_y']):
            mc.add_child(folium.Marker([row['koord_y'], row['koord_x']], 
                                    tooltip='Keterangan : {}<br> Kapasitas TPA : {}'.format(row['remarks'], row['kaptpa']))).add_to(m)
            
    folium.plugins.Fullscreen(
    position="topright",
    title="Expand me",
    title_cancel="Exit me",
    force_separate_button=True,
    ).add_to(m)

    return m

if province and sector:
    with st.spinner('Constructing ...'):
        html_map = marker()._repr_html_()
        st.markdown(html_map, unsafe_allow_html=True)

st.markdown('')
with st.expander("**Penjelasan Parameter Prioritasisasi**"):
    st.markdown('Berikut merupakan parameter yang digunakan sehingga peta prioritas bisa terbentuk : ')

with st.expander("**Ide Pengembangan**"):
    st.markdown('''
                #### Optimasi Pengelolaan dan Pencarian Lokasi Optimal ✅
                Dengan memanfaatkan data spasial, ML bisa membantu dalam menentukan lokasi optimal untuk TPA baru berdasarkan faktor-faktor seperti aksesibilitas, dampak lingkungan, dan jarak ke pemukiman. Ini membantu mengoptimalkan pengelolaan sampah.
                
                #### Prediksi Pengelolaan Sampah (simulatif)
                ML dapat digunakan untuk menganalisis data historis tentang jumlah dan jenis sampah yang dihasilkan oleh suatu wilayah. Dengan model prediktif, TPA dapat mempersiapkan rencana pengelolaan yang lebih efisien dan terukur.

                #### Pemantauan dan Pemeliharaan       
                AI dapat digunakan untuk pemantauan sistem TPA secara real-time. Dengan sensor IoT dan analisis citra, AI dapat mendeteksi tingkat pengisian TPA, memantau pola pengumpulan sampah, dan mengidentifikasi masalah seperti bau atau kebocoran gas metana.

                #### Pengelolaan Gas Metana
                ML bisa digunakan untuk memodelkan produksi gas metana dari TPA. Ini memungkinkan perencanaan yang lebih baik dalam pengelolaan gas tersebut, termasuk potensi untuk menangkap dan menggunakan metana sebagai sumber energi alternatif.

                #### Prediksi Dampak Lingkungan
                Dengan analisis data dan machine learning, dapat dibuat model untuk memprediksi dampak lingkungan dari TPA, seperti pencemaran air tanah atau udara. Ini memungkinkan upaya mitigasi dan pengelolaan risiko yang lebih baik.

                #### Pengembangan Sistem Sortir Otomatis
                AI dapat diterapkan dalam pengembangan sistem sortir sampah otomatis di TPA. Pengenalan gambar atau teknologi sensor dapat memisahkan jenis sampah untuk proses daur ulang atau pengolahan yang tepat.
                ''')
    
    st.markdown('')
    st.markdown(
                '''
                Pemanfaatan ML dan AI dalam pengelolaan TPA dapat membantu dalam efisiensi pengelolaan sampah, mitigasi dampak lingkungan, dan penggunaan sumber daya yang lebih bijaksana. Ini juga dapat meningkatkan kesadaran lingkungan dan inovasi dalam pengelolaan limbah.
                '''
                )