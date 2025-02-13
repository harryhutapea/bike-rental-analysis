import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    # Dapatkan path file relatif terhadap lokasi dashboard.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'day.csv')
    df = pd.read_csv(file_path)
    df['dteday'] = pd.to_datetime(df['dteday'])
    categorical_cols = ['season', 'yr', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit']
    for col in categorical_cols:
        df[col] = df[col].astype('category')
    return df

# Fungsi untuk membersihkan data
def clean_data(df):
    # Impor library yang dibutuhkan
    import pandas as pd
    Q1 = df['cnt'].quantile(0.25)
    Q3 = df['cnt'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df_clean = df[(df['cnt'] >= lower_bound) & (df['cnt'] <= upper_bound)]
    return df_clean

# Memuat data dengan fungsi load_data()
st.write("Memuat data...")
with st.spinner("Loading data..."):
    raw_df = load_data()
st.write("Data berhasil dimuat!")

# Membersihkan data
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
    options=['0', '1'],
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

# Layout: 2 kolom untuk visualisasi utama
col1, col2 = st.columns(2)

with col1:
    st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda Harian")
    # Pastikan mengimpor library pada code block ini
    import matplotlib.pyplot as plt
    import seaborn as sns
    plt.figure(figsize=(8,5))
    sns.boxplot(x='weathersit', y='cnt', data=df, palette='coolwarm')
    plt.title('Pengaruh Cuaca terhadap Penyewaan Sepeda Harian')
    plt.xlabel('Kondisi Cuaca (1=Cerah, 2=Mendung, 3=Hujan Ringan/Salju, 4=Hujan Lebat/Salju)')
    plt.ylabel('Jumlah Penyewaan')
    plt.tight_layout()
    st.pyplot(plt.gcf())

with col2:
    st.subheader("Pola Peminjaman Sepeda: Hari Kerja vs. Akhir Pekan")
    import matplotlib.pyplot as plt
    import seaborn as sns
    plt.figure(figsize=(8,5))
    sns.boxplot(x='workingday', y='cnt', data=df, palette='muted')
    plt.title('Pola Peminjaman Sepeda: Hari Kerja vs. Akhir Pekan')
    plt.xlabel('Hari Kerja (0 = Akhir Pekan, 1 = Hari Kerja)')
    plt.ylabel('Jumlah Penyewaan')
    plt.tight_layout()
    st.pyplot(plt.gcf())

st.subheader("Data Penyewaan Sepeda (Filtered)")
st.dataframe(df_filtered.head(20))
