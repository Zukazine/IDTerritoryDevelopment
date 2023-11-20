import streamlit as st
import geopandas as gpd
import folium
import math
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

st.set_page_config(layout="wide") 

st.title('SDA Dashboard 🌊')

option = st.selectbox('Pilih Nama Daaerah Irigasi', ['D.I. Awo', 'D.I. Bajo', 'D.I. Bantimurung', 'D.I. Bayang Bayang', 'D.I. Bila Kalola', 'D.I. Bissua', 'D.I. Bontomanai', 'D.I. Bulucenrana', 'D.I. Kampili', 'D.I. Kanjiro', 'D.I. Kelara Karalloe', 'D.I. Lamasi', 'D.I. Langkemme', 'D.I. Lekopancing', 'D.I. Padang Sappa', 'D.I. Palakka', 'D.I. Pamukkulu', 'D.I. Pattiro', 'D.I. Ponre Ponre', 'D.I. Sanrego', 'D.I. Tabo Tabo', 'D.I. Tinco', 'D.I. Kalaena', 'D.I. Way Curup', 'D.I. Way Jepara', 'D.I. Paku', 'D.I. Bulutimorang', 'D.I. Saddang', 'D.I. Bumi Agung', 'D.I. Jabung Kiri', 'D.I. Way Kandis II', 'D.I. Way Seputih', 'D.I. Cacaban', 'D.I. Way Tulung Mas', 'D.I. Way Rarem', 'D.I. Way Sekampung', 'D.I. Way Pangubuan', 'D.I. Way Tebu Sistem', 'D.I. Way Umpu', 'D.I. Jabung Kanan', 'D.I. Banjarcahyana', 'D.I. Bodri', 'D.I. Boro', 'D.I. Colo', 'D.I. Comal', 'D.I. Dumpil', 'D.I. Gembong', 'D.I. Glapan', 'D.I. Gung', 'D.I. Gunung Rowo', 'D.I. Jragung', 'D.I. Kaliwadas', 'D.I. Kedung Asem', 'D.I. Kedung Putri', 'D.I. Klambu', 'D.I. Kumisik', 'D.I. Kupang Krompeng', 'D.I. Logung', 'D.I. Manganti', 'D.I. Pemali', 'D.I. Pesantren Kletak', 'D.I. Progo Manggis-Kalibening', 'D.I. Rambut', 'D.I. Sedadi', 'D.I. Semen Krinjo', 'D.I. Waduk Sempor', 'D.I. Serayu', 'D.I. Sidorejo', 'D.I. Singomerto', 'D.I. Sragi', 'D.I. Sungapan', 'D.I. Tajum', 'D.I. Waduk Wadaslintang', 'D.I. Waduk Malahayu', 'D.I. Tukad Ayung', 'D.I. Tukad Oos', 'D.I. Tukad Pekerisan', 'D.I. Tukad Penet', 'D.I. Tukad Petanu', 'D.I. Tukad Sungi', 'D.I. Tukad Unda', 'D.I. Tukad Yeh Hoo', 'D.I. Tukad Saba', 'D.I. Tukad Penarukan-Buwus', 'D.I. Alue Ubay', 'D.I. Baro Raya', 'D.I. Jambo Aye Langkahan', 'D.I. Jamuan', 'D.I. Jeuram', 'D.I. Krueng Aceh/ Leubok', 'D.I. Krueng Jrue/Keuliling', 'D.I. Krueng Pase', 'D.I. Lhok Guci', 'D.I. Pante Lhong', 'D.I. Rajui', 'D.I. Susoh', 'D.I. Krueng Tiro', 'D.I. Bandar Sidoras', 'D.I. Batang Angkola', 'D.I. Batang Batahan', 'D.I. Batang Gadis', 'D.I. Batang Ilung', 'D.I. Kerasaan', 'D.I. Namu Sira-sira', 'D.I. Perkotaan', 'D.I. Sungai Ular', 'D.I. Paya Sordang', 'D.I. Sei Belutu', 'D.I. Komering', 'D.I. Lintang Kiri', 'D.I. Cibaliung', 'D.I. Cidurian', 'D.I. Lintang Kanan', 'D.I. Ciliman', 'D.I. Cisadane', 'D.I. Ciujung', 'D.I. Batu Bulan', 'D.I. Muara Riben', 'D.I. Batujai', 'D.I. Jurang Batu', 'D.I. Lematang', 'D.I. Air Lakitan', 'D.I. Kelingi Tugu Mulyo', 'D.I. Air Keruh', 'D.I. Jurang Sate Hilir', 'D.I. Katon Kompleks', 'D.I. Katua Kompleks', 'D.I. Mamak-Kakiang', 'D.I. Mujur II', 'D.I. Pandanduri-Swangi', 'D.I. Pelaparado', 'D.I. Pengga', 'D.I. Remening Kompleks', 'D.I. Surabaya', 'D.I. Tanggik Kompleks', 'D.I. Gde Bongoh Kompleks', 'D.I. Jurang Sate Hulu', 'D.I. Belimbing Kompleks', 'D.I. Mada Pangga Kompleks', 'D.I. Rababaka Kompleks', 'D.I. Batang Alai', 'D.I. Amandit', 'D.I. Bondoyudo', 'D.I. Delta Brantas', 'D.I. Batu Licin', 'D.I. Pitap', 'D.I. Tapin', 'D.I. Telaga Langsat', 'D.I. Riam Kanan', 'D.I. Kalibawang', 'D.I. Karangtalun', 'D.I. Tuk Kuning', 'D.I. Asin Bawah', 'D.I. Banyuputih', 'D.I. Baru', 'D.I. Bedadung', 'D.I. Bengawan Jero', 'D.I. Beron', 'D.I. Gondang', 'D.I. Jatiroto', 'D.I. Jejeruk', 'D.I. K (Setail)', 'D.I. Is Kedung Kandang', 'D.I. Lodoyo', 'D.I. Menturus', 'D.I. Is Molek', 'D.I. Mrican', 'D.I. Pacal', 'D.I. Padi Pomahan', 'D.I. Pekalen', 'D.I. Pondok Waluh', 'D.I. Porolinggo', 'D.I. Sampean Baru', 'D.I. Sampean Lama', 'D.I. Setail Teknik', 'D.I. Sim', 'D.I. Siman', 'D.I. Sungkur', 'D.I. Talang', 'D.I. Waduk Bening', 'D.I. Wd. Prijetan', 'D.I. Waduk Pondok', 'D.I. Batang Sinamar', 'D.I. Batang Bayang', 'D.I. Lubuk Buaya', 'D.I. Malapang Ampang Tulak', 'D.I. Batang Anai', 'D.I. Kumbung', 'D.I. Antokan', 'D.I. Bantarheulang', 'D.I. Cihea', 'D.I. Cikarangeusan', 'D.I. Cikeusik', 'D.I. Cikunten I', 'D.I. Cikunten II', 'D.I. Cileleuy', 'D.I. Ciletuh', 'D.I. Cipamingkis', 'D.I. Batang Hari', 'D.I. Batang Tongar', 'D.I. Sawah Laweh Tarusan', 'D.I. Batang Inderapura', 'D.I. Panti Rao', 'D.I. Cipanas II', 'D.I. Cipancuh', 'D.I. Ciwaringin', 'D.I. Jatiluhur', 'D.I. Kamun', 'D.I. Lakbok Utara', 'D.I. Leuwinangka', 'D.I. Rentang', 'D.I. Seuseupan', 'D.I. Kosinggolan', 'D.I. Sangkub', 'D.I. Toraut', 'D.I. Dataran Kotamobagu', 'D.I. Rias', 'D.I. Air Lais Kuro Tidur', 'D.I. Selingsing', 'D.I. Air Nipis Seginim', 'D.I. Air Seluma', 'D.I. Air Alas', 'D.I. Air Ketahun', 'D.I. Manjuto', 'D.I. Randangan', 'D.I. Paguyaman', 'D.I. Lomaya Alale Pilohayanga', 'D.I. Alopohu', 'D.I. Batang Asai', 'D.I. Siulak Deras', 'D.I. Sei Batang Sangkir', 'D.I. Limun Singkut', 'D.I. Karau', 'D.I. Tapau', 'D.I. Bubi', 'D.I. Kobi', 'D.I. Matakabo', 'D.I. Samal', 'D.I. Way Trukat Fogi', 'D.I. Way Apu Sistem', 'D.I. Way Geren', 'D.I. Werinama', 'D.I. Akelamo Patlean Pumlanga (Usulan Baru)', 'D.I. Kesayangan Wairoro Tilope Kluting (Usulan Baru)', 'D.I. Toliwang Tolabit Leleseng (Usulan Baru)', 'D.I. Opiyang Mancalele', 'D.I. Akedaga Tutiling Meja', 'D.I. Danau Tua', 'D.I. Haekesak', 'D.I. Haekto', 'D.I. Batu Merah', 'D.I. Bena', 'D.I. Benlelang', 'D.I. Kambaniru', 'D.I. Lembor', 'D.I. Lokopehapo', 'D.I. Lurasik', 'D.I. Magepanda', 'D.I. Malaka', 'D.I. Manikin', 'D.I. Mautenda', 'D.I. Mbay', 'D.I. Mena', "D.I. So'a", 'D.I. Nggorang', 'D.I. Oesao', 'D.I. Pota', 'D.I. Tanah Raing', 'D.I. Wae Dingin', 'D.I. Simpang', 'D.I. Tilong', 'D.I. Waekomo', 'D.I. Wae Mantar', 'D.I. Wariori', 'D.I. Oransbari', 'D.I. Maloso', 'D.I. Prafi', 'D.I. Gumbasa', 'D.I. Karaopa', 'D.I. Kelayang', 'D.I. Aimasi Cs', 'D.I. Mentawa', 'D.I. Sinorang Ombolu', 'D.I. Sausu Atas', 'D.I. Lambunu', 'D.I. Wundulako', 'D.I. Walay', 'D.I. Poleang', 'D.I. Mowila', 'D.I. Ladongi', 'D.I. Singkoyo', 'D.I. Aporo-Lambandia', 'D.I. Wawotobi Ameroro'])

def read_data():
    data = gpd.read_file('dataset/irrigation.shp')
    return data

def marker():
    water = read_data()
    
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

if option:
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
