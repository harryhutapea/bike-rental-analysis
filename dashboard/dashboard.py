import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

@st.cache_data
def load_data():
    # Memuat dataset penyewaan sepeda
    df = pd.read_csv('day.csv')
    # Konversi kolom tanggal ke format datetime
    df['dteday'] = pd.to_datetime(df['dteday'])
    # Ubah kolom-kolom yang bersifat kategori
    categorical_cols = ['season', 'yr', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit']
    for col in categorical_cols:
        df[col] = df[col].astype('category')
    return df

def clean_data(df):
    # Membersihkan data dengan menghapus outlier pada kolom 'cnt' menggunakan metode IQR
    Q1 = df['cnt'].quantile(0.25)
    Q3 = df['cnt'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df_clean = df[(df['cnt'] >= lower_bound) & (df['cnt'] <= upper_bound)]
    return df_clean

# Load dan clean data
raw_df = load_data()
df = clean_data(raw_df)

# Sidebar: Filter Data
st.sidebar.header("Filter Data")
# Pilih kondisi cuaca
weather_filter = st.sidebar.selectbox(
    "Pilih Kondisi Cuaca (weathersit)",
    options=sorted(raw_df['weathersit'].cat.categories),
    format_func=lambda x: {
        '1': 'Cerah',
        '2': 'Mendung',
        '3': 'Hujan Ringan/Salju',
        '4': 'Hujan Lebat/Salju'
    }.get(x, x)
)
# Pilih tipe hari: Hari Kerja atau Akhir Pekan
workingday_filter = st.sidebar.radio(
    "Pilih Tipe Hari",
    options=['0', '1'],  # '0' untuk akhir pekan, '1' untuk hari kerja
    format_func=lambda x: "Akhir Pekan" if x == '0' else "Hari Kerja"
)

# Filter data sesuai pilihan
df_filtered = df[(df['weathersit'] == weather_filter) & (df['workingday'] == workingday_filter)]

# Judul Dashboard
st.title("Bike Sharing Dashboard")
st.markdown("""
Dashboard ini menampilkan visualisasi dari data penyewaan sepeda harian. 
Gunakan filter di sidebar untuk menyesuaikan kondisi cuaca dan tipe hari.
""")

# Layout dengan 2 kolom untuk visualisasi utama
col1, col2 = st.columns(2)

with col1:
    st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda Harian")
    # Visualisasi: Boxplot pengaruh cuaca terhadap penyewaan sepeda
    plt.figure(figsize=(8,5))
    sns.boxplot(x='weathersit', y='cnt', data=df, palette='coolwarm')
    plt.title('Pengaruh Cuaca terhadap Penyewaan Sepeda Harian')
    plt.xlabel('Kondisi Cuaca (1=Cerah, 2=Mendung, 3=Hujan Ringan/Salju, 4=Hujan Lebat/Salju)')
    plt.ylabel('Jumlah Penyewaan')
    st.pyplot(plt)
    
with col2:
    st.subheader("Pola Peminjaman Sepeda: Hari Kerja vs. Akhir Pekan")
    # Visualisasi: Boxplot perbandingan hari kerja vs. akhir pekan
    plt.figure(figsize=(8,5))
    sns.boxplot(x='workingday', y='cnt', data=df, palette='muted')
    plt.title('Pola Peminjaman Sepeda: Hari Kerja vs. Akhir Pekan')
    plt.xlabel('Hari Kerja (0 = Akhir Pekan, 1 = Hari Kerja)')
    plt.ylabel('Jumlah Penyewaan')
    st.pyplot(plt)

# Tampilkan data yang sudah difilter (opsional)
st.subheader("Data Penyewaan Sepeda (Filtered)")
st.dataframe(df_filtered)
