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
        html_map = marker()._repr_html_()
        st.markdown(html_map, unsafe_allow_html=True)
        st.markdown('')
        st.markdown('')
        # folium_static(marker(), width=850, height=400)
    
with st.expander(":red[**Parameter Prioritasisasi**]"):
    params = st.selectbox('Pilih Parameter', ['Kemiringan Lereng', 'Jenis Tutupan Lahan (LULC)', 'Presipitasi','Populasi', 'Normalized Difference Salinity Index', 'Jaringan Jalan', 'Jaringan Sungai', 'Soil pH', 'Soil Clay', 'Infrastruktur Air', 'Produktivitas Pertanian Padi', 'Neraca Air'])
    if params:
        if params == 'Kemiringan Lereng':
            
            st.markdown('''
                        :red[**Penjelasan**]  
                        Kemiringan lereng menjadi faktor yang akan memengaruhi persiapan lahan yang dapat diairi, operasi irigasi, efisiensi irigasi efisiensi, erosi, biaya penyiapan lahan, jenis tanaman, biaya produksi produksi, dan metode irigasi (Hussien dkk., 2019).''')
            st.image('images/1_Slope.png')
            right, left = st.columns(2)
            with right: 
                st.markdown('''
                            :red[**Sumber Data**]  
                            NASA SRTM Digital Elevation 30m
                            ''')
            with left:
                st.markdown('''
                            :red[**Tipe Data dan Resolusi**]  
                            Raster-30m
                            ''')
        elif params == 'Jenis Tutupan Lahan (LULC)':
            st.markdown('''
                        :red[**Penjelasan**]  
                        Jenis tutupan lahan menjadi parameter penting  dalam analisis kesesuaian lahan untuk irigasi permukaan (Hagos dkk., 2022). Hal ini karena LULC membantu mengidentifikasi produktivitas suatu wilayah untuk irigasi.''')
            st.image('images/2_LULC.png')
            
            right, left = st.columns(2)
            with right: 
                st.markdown('''
                            :red[**Sumber Data**]  
                            ESA WorldCover 10m v100
                            ''')
            with left:
                st.markdown('''
                            :red[**Tipe Data dan Resolusi**]  
                            Raster-100m
                            ''')
        elif params == 'Presipitasi':
            st.markdown('''
                        :red[**Penjelasan**]  
                        Curah hujan sangat penting dalam penilaian irigasi permukaan untuk memastikan bahwa ada cukup air yang tersedia untuk irigasi dan untuk menentukan kesesuaian metode irigasi (Hagos dkk., 2022).''')
            
            st.image('images/3_Precipitation.png')
            
            right, left = st.columns(2)
            with right: 
                st.markdown('''
                            :red[**Sumber Data**]  
                            TerraClimate: Monthly Climate and Climatic Water Balance for Global Terrestrial Surfaces, University of Idaho
                            ''')
            with left:
                st.markdown('''
                            :red[**Tipe Data dan Resolusi**]  
                            Raster-4800m
                            ''')
        elif params == 'Populasi':
            st.markdown('''
                        :red[**Penjelasan**]  
                        Mempertimbangkan distribusi kepadatan penduduk merupakan hal yang penting dalam penilaian irigasi permukaan untuk memahami permintaan produk pertanian dan ketersediaan tenaga kerja, yang merupakan faktor penting dalam menentukan kesesuaian suatu daerah untuk irigasi (Worqlul dkk., 2018).''')

            st.image('images/4_Population.png')
            
            right, left = st.columns(2)
            with right: 
                st.markdown('''
                            :red[**Sumber Data**]  
                            WorldPop Global Project Population Data: Estimated Residential Population per 100x100m Grid Square
                            ''')
            with left:
                st.markdown('''
                            :red[**Tipe Data dan Resolusi**]  
                            Raster-100m
                            ''')
        elif params == 'Normalized Difference Salinity Index':
            st.markdown('''
                        :red[**Penjelasan**]  
                        NDSI dapat membantu mengidentifikasi area yang terkena dampak salinitas di dalam ladang irigasi, memungkinkan strategi irigasi yang ditargetkan dan praktik pengelolaan tanah untuk mengurangi dampak salinitas pada produktivitas pertanian (Wubalem, 2023).''')

            st.image('images/5_NDSI.png')
            
            right, left = st.columns(2)
            with right: 
                st.markdown('''
                            :red[**Sumber Data**]  
                            USGS Landsat 8 Collection 2 Tier 1 TOA Reflectance (Band 3 dan Band 4)
                            ''')
            with left:
                st.markdown('''
                            :red[**Tipe Data dan Resolusi**]  
                            Raster-30m
                            ''')
        elif params == 'Jaringan Jalan':
            st.markdown('''
                        :red[**Penjelasan**]  
                        Kedekatan jalan raya dipertimbangkan dalam analisis kesesuaian daerah irigasi permukaan karena pengaruhnya terhadap akses ke input pertanian, outlet pasar, dan pusat-pusat kota, serta dampaknya terhadap operasi dan efisiensi irigasi (Kassie dkk., 2022).''')

            st.image('images/6_RoadNetwork.png')
            
            right, left = st.columns(2)
            with right: 
                st.markdown('''
                            :red[**Sumber Data**]  
                            GRIP global roads database
                            ''')
            with left:
                st.markdown('''
                            :red[**Tipe Data dan Resolusi**]  
                            Vektor-polyline
                            ''')
        elif params == 'Jaringan Sungai':
            st.markdown('''
                        :red[**Penjelasan**]  
                        Jarak antara lahan yang dapat diairi dan sungai merupakan faktor penting dalam menentukan kesesuaian suatu daerah untuk irigasi permukaan, dan daerah yang terletak dalam jarak tertentu dari sungai dianggap sangat cocok untuk irigasi (Getahun dkk., 2023).''')

            st.image('images/7_RiverNetwork.png')
            
            right, left = st.columns(2)
            with right: 
                st.markdown('''
                            :red[**Sumber Data**]  
                            Global River Classification (GloRiC)
                            ''')
            with left:
                st.markdown('''
                            :red[**Tipe Data dan Resolusi**]  
                            Vektor-polyline
                            ''')
        elif params == 'Soil pH':
            st.markdown('''
                        :red[**Penjelasan**]  
                        Tingkat keasaman tanah adalah salah satu faktor yang perlu diperiksa untuk kesesuaian irigasi permukaan karena mempengaruhi hasil panen (USDIBR, 2003).''')

            st.image('images/8_pH.png')
            
            right, left = st.columns(2)
            with right: 
                st.markdown('''
                            :red[**Sumber Data**]  
                            Soil Grids 250m v2.0
                            ''')
            with left:
                st.markdown('''
                            :red[**Tipe Data dan Resolusi**]  
                            Raster-250m
                            ''')
        elif params == 'Soil Clay':
            st.markdown('''
                        :red[**Penjelasan**]  
                        Pertimbangan tanah lempung penting dalam menganalisis kesesuaian daerah irigasi permukaan karena tanah lempung menyimpan lebih banyak air daripada tanah berpasir maka irigasi permukaan dapat bekerja lebih baik pada kondisi tanah liat atau pasir yang berat dibandingkan dengan alat penyiram. Namun, penting untuk dicatat bahwa tanah lempung yang berat umumnya harus dihindari untuk irigasi, karena sulit untuk dikelola dan dapat menyebabkan limpasan air daripada penyerapan (Department for Environment and Water, 2023).''')

            st.image('images/9_Clay.png')
            
            right, left = st.columns(2)
            with right: 
                st.markdown('''
                            :red[**Sumber Data**]  
                            Soil Grids 250m v2.0
                            ''')
            with left:
                st.markdown('''
                            :red[**Tipe Data dan Resolusi**]  
                            Raster-250m
                            ''')
        elif params == 'Infrastruktur Air':
            st.markdown('''
                        :red[**Penjelasan**]  
                        - **Bendungan operasi** memainkan peran penting dalam penyimpanan dan distribusi air untuk tujuan irigasi karena akan memberikan wawasan tentang ketersediaan, regulasi, dan pengelolaan sumber daya air untuk irigasi permukaan (FAO, 1989).  
                        - Data **Intake Sungai** dapat membantu mengidentifikasi kesesuaian infrastruktur irigasi yang ada atau yang diusulkan, seperti kanal, waduk, dan stasiun pompa (FAO, 1989). Informasi ini sangat penting untuk merencanakan dan melaksanakan pembangunan irigasi berkelanjutan dan memastikan distribusi air yang efisien ke daerah irigasi.  
                        - Sedangkan untuk data **Daerah Irigasi Permukaan** merupakan data yang digunakan untuk memperlihatkan daerah irigasi di lahan sawah nontadah hujan. 
                        ''')
            st.markdown('')
            st.image('images/10_SIA_RI_D.png')
            
            right, left = st.columns(2)
            with right: 
                st.markdown('''
                            :red[**Sumber Data**]  
                            SIGI PUPR
                            ''')
            with left:
                st.markdown('''
                            :red[**Tipe Data dan Resolusi**]  
                            Vektor-point
                            ''')
        elif params == 'Produktivitas Pertanian Padi':
            st.markdown('''
                        :red[**Penjelasan**]  
                        Data produksi padi dapat digunakan untuk penilaian irigasi permukaan untuk memahami dampak praktik irigasi terhadap budidaya padi dan untuk mengidentifikasi area di mana pengelolaan air dan strategi irigasi dapat meningkatkan produktivitas padi. ''')

            st.image('images/11_Rice.png')
            
            right, left = st.columns(2)
            with right: 
                st.markdown('''
                            :red[**Sumber Data**]  
                            BDSP Kementan
                            ''')
            with left:
                st.markdown('''
                            :red[**Tipe Data dan Resolusi**]  
                            Tabular
                            ''')
        elif params == 'Neraca Air':
            st.markdown('''
                        :red[**Penjelasan**]  
                        Penggunaan data neraca air dalam penilaian irigasi permukaan berperan dalam memahami ketersediaan air, efisiensi irigasi, pengelolaan air, dampak variabilitas iklim, dan optimalisasi praktik irigasi.
                        ''')

            st.image('images/12_wb.png')
            
            right, left = st.columns(2)
            with right: 
                st.markdown('''
                            :red[**Sumber Data**]  
                            SIGI PUPR
                            ''')
            with left:
                st.markdown('''
                            :red[**Tipe Data dan Resolusi**]  
                            Vektor-polygon
                            ''')
        else:
            st.warning('Silahkan pilih salah satu parameter terlebih dahulu')

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
