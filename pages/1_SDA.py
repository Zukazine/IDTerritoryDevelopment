import streamlit as st
import geopandas as gpd
import folium
import math
import pandas as pd
import pydeck as pdk
from folium.plugins import MarkerCluster
from folium import Marker


st.set_page_config(layout="wide") 

st.title('SDA Dashboard 🌊')

left, right = st.columns(2)

with left:
    province = st.selectbox('Pilih Provinsi', ['Aceh', 'Bali', 'Banten', 'Bengkulu', 'Daerah Istimewa Yogyakarta', 'DKI Jakarta', 'Gorontalo', 'Jambi', 'Jawa Barat', 'Jawa Tengah', 'Jawa Timur', 'Kalimantan Selatan', 'Kalimantan Tengah', 'Kepulauan Bangka Belitung', 'Kepulauan Riau', 'Lampung', 'Maluku Utara', 'Maluku', 'Nusa Tenggara Barat', 'Nusa Tenggara Timur', 'Papua Barat', 'Riau', 'Sulawesi Barat', 'Sulawesi Selatan', 'Sulawesi Tengah', 'Sulawesi Tenggara', 'Sulawesi Utara', 'Sumatera Barat', 'Sumatera Selatan', 'Sumatera Utara'])

with right:
    sector = st.selectbox('**Pilih Sektor SDA**', ['Irigasi'])

with st.expander(":red[**Kustomisasi Map**]"):
    option = st.radio('Pilih detail Geo-Visualization : ', ['Choropleth 2D', 'Choropleth 2D & 3D', 'Marker Cluster'])

def color_map(val):
    viridis_colors = [
    [68, 1, 84], [69, 4, 87], [70, 8, 92], [70, 11, 94],
    [71, 16, 99], [72, 19, 101], [72, 23, 105], [72, 27, 109], [72, 29, 111],
    [72, 33, 115], [72, 36, 117], [72, 40, 120], [71, 44, 122], [71, 46, 124],
    [71, 50, 126], [70, 52, 128], [70, 56, 130], [68, 58, 131], [67, 62, 133],
    [66, 65, 134], [65, 68, 135], [63, 71, 136], [62, 73, 137], [61, 77, 138],
    [60, 80, 139], [59, 82, 139], [57, 85, 140], [56, 88, 140], [55, 91, 141],
    [54, 93, 141], [52, 96, 141], [51, 99, 141], [50, 101, 142], [49, 104, 142],
    [48, 106, 142], [46, 109, 142], [45, 112, 142], [44, 113, 142], [43, 116, 142],
    [42, 118, 142], [41, 121, 142], [40, 124, 142], [39, 126, 142], [38, 129, 142],
    [38, 130, 142], [37, 133, 142], [36, 135, 142], [35, 138, 141], [34, 141, 141],
    [33, 143, 141], [32, 146, 140], [32, 147, 140], [31, 150, 139], [31, 153, 138],
    [30, 155, 138], [31, 158, 137], [31, 160, 136], [31, 162, 135], [32, 164, 134],
    [34, 167, 133], [36, 170, 131], [37, 172, 130], [40, 174, 128], [42, 176, 127],
    [46, 179, 124], [50, 182, 122], [53, 183, 121], [58, 186, 118], [61, 188, 116],
    [66, 190, 113], [72, 193, 110], [76, 194, 108], [82, 197, 105], [86, 198, 103],
    [92, 200, 99], [96, 202, 96], [103, 204, 92], [110, 206, 88], [115, 208, 86],
    [122, 209, 81], [127, 211, 78], [134, 213, 73], [142, 214, 69], [147, 215, 65],
    [155, 217, 60], [160, 218, 57], [168, 219, 52], [173, 220, 48], [181, 222, 43],
    [189, 223, 38], [194, 223, 35], [202, 225, 31], [208, 225, 28], [216, 226, 25],
    [223, 227, 24], [229, 228, 25], [236, 229, 27], [241, 229, 29], [248, 230, 33],
    [253, 231, 37]
    ]
    
    return viridis_colors[val-1]

def calculate_emergeval(val):
    return val * 50

def cplethdeck(file):
    ''' VISUALIZE WITH PDK & EACH PROVINCE - 3D Model'''

    file = 'irrigation_provinces_json\{:s}'.format(file)

    json  = pd.read_json(file)
    df = pd.DataFrame()

    df["coordinates"] = json["features"].apply(lambda row: row["geometry"]["coordinates"])
    df["gridclass"] = json["features"].apply(lambda row: row["properties"]["gridcode"])
    df['colors'] = df.gridclass.apply(lambda x: color_map(x))
    df['lat'] = json["features"].apply(lambda row: row["properties"]["latitude"])
    df['lng'] = json["features"].apply(lambda row: row["properties"]["longitude"])

    view_state = pdk.ViewState(
        **{"latitude": df['lat'].iloc[0], "longitude": df['lng'].iloc[0], "zoom": 8, "maxZoom": 16, "pitch": 0, "bearing": 0}
    )

    polygon_layer = pdk.Layer(
        "PolygonLayer",
        df[:20000],
        id="geojson",
        # opacity=0.8,
        stroked=False,
        get_polygon="coordinates",
        filled=True,
        extruded=True,
        wireframe=True,
        get_elevation=0,
        get_fill_color="colors",
        # get_line_color=[0, 0, 0],
        auto_highlight=True,
        pickable=True,
    )

    # tooltip = {"html": "<b>Value per Square Meter:</b> {valuePerSqm} <br /><b>Growth rate:</b> {growth}"}

    r = pdk.Deck(
        polygon_layer,
        # map_provider='google_maps',
        map_style='road',
        initial_view_state=view_state,
        # tooltip=tooltip,
    )
    return r

def cplethdeck_3D(file):
    ''' VISUALIZE WITH PDK & EACH PROVINCE - 3D Model'''

    file = 'irrigation_provinces_json\{:s}'.format(file)

    json  = pd.read_json(file)
    df = pd.DataFrame()

    df["coordinates"] = json["features"].apply(lambda row: row["geometry"]["coordinates"])
    df["gridclass"] = json["features"].apply(lambda row: row["properties"]["gridcode"])
    df['colors'] = df.gridclass.apply(lambda x: color_map(x))
    df["emerge_value"] = json["features"].apply(lambda row: calculate_emergeval(row["properties"]["gridcode"]))
    df['lat'] = json["features"].apply(lambda row: row["properties"]["latitude"])
    df['lng'] = json["features"].apply(lambda row: row["properties"]["longitude"])

    view_state = pdk.ViewState(
        **{"latitude": df['lat'].iloc[0], "longitude": df['lng'].iloc[0], "zoom": 9, "maxZoom": 16, "pitch": 75, "bearing": 0}
    )

    polygon_layer = pdk.Layer(
        "PolygonLayer",
        df[:20000],
        id="geojson",
        # opacity=0.8,
        stroked=False,
        get_polygon="coordinates",
        filled=True,
        extruded=True,
        wireframe=True,
        get_elevation='emerge_value',
        get_fill_color="colors",
        get_line_color="colors",
        auto_highlight=True,
        pickable=True,
    )

    # tooltip = {"html": "<b>Value per Square Meter:</b> {valuePerSqm} <br /><b>Growth rate:</b> {growth}"}

    r = pdk.Deck(
        polygon_layer,
        # map_provider='google_maps',
        map_style='road',
        initial_view_state=view_state,
        # tooltip=tooltip,
    )
    return r

def marker(file):
    gdf = gpd.read_file('irrigation_provinces_json\{:s}'.format(file))
    lat, lng = gdf.latitude.iloc[0], gdf.longitude.iloc[0]

    if 'irri_data' not in st.session_state:
        st.session_state.irri_data = gpd.read_file('dataset/irrigation.shp') 

    irri_data = st.session_state.irri_data
    
    m = folium.Map(location=[0.7893,113.9213], 
                 zoom_start=5)

    mc = MarkerCluster()
    for idx, row in irri_data.iterrows():
        if not math.isnan(row['koord_x']) and not math.isnan(row['koord_y']):
            mc.add_child(Marker([row['koord_y'], row['koord_x']],
                                tooltip='Nama Infrastruktur : {:s}<br>Provinsi : {:s} <br>Luas : {:d} hektar'.format(row['nm_inf'], row['provinsi'], row['luas_ha'])))

    m.add_child(mc)
            
    folium.plugins.Fullscreen(
    position="topright",
    title="Expand me",
    title_cancel="Exit me",
    force_separate_button=True,
    ).add_to(m)

    return m

lmap, rmap = st.columns(2)

if province and sector and option:
    with st.spinner('Constructing ...'):
        if option == 'Choropleth 2D':
            st.pydeck_chart(cplethdeck(province+'.json'))
        elif option == 'Choropleth 2D & 3D':
            with lmap:
                st.pydeck_chart(cplethdeck(province+'.json'))
            with rmap:
                st.pydeck_chart(cplethdeck_3D(province+'.json'))
        elif option =='Marker Cluster':
            html_map = marker(province+'.json')._repr_html_()
            st.markdown(html_map, unsafe_allow_html=True)
        else:
            st.warning('Wa Wi Wu')
                

st.markdown('')

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
