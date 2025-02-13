import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('day.csv')
    df['dteday'] = pd.to_datetime(df['dteday'])
    categorical_cols = ['season', 'yr', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit']
    for col in categorical_cols:
        df[col] = df[col].astype('category')
    return df

def clean_data(df):
    Q1 = df['cnt'].quantile(0.25)
    Q3 = df['cnt'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df_clean = df[(df['cnt'] >= lower_bound) & (df['cnt'] <= upper_bound)]
    return df_clean


# Mengambil path direktori file dashboard.py
current_dir = os.path.dirname(os.path.abspath(__file__))
# Gabungkan dengan nama file day.csv
file_path = os.path.join(current_dir, 'day.csv')

# Muat dataset menggunakan path absolute
df = pd.read_csv(file_path)
st.write("Memuat data...")  # User feedback
with st.spinner("Loading data..."):  # Loading indicator
    raw_df = load_data()
st.write("Data berhasil dimuat!")  # User feedback

# Mengambil path direktori file dashboard.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# Gabungkan dengan nama file day.csv
file_path = os.path.join(current_dir, 'day.csv')

df = clean_data(raw_df)

# Sidebar: Filter Data
st.sidebar.header("Filter Data")
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
workingday_filter = st.sidebar.radio(
    "Pilih Tipe Hari",
    options=['0', '1'],
    format_func=lambda x: "Akhir Pekan" if x == '0' else "Hari Kerja"
)

# Filter data
df_filtered = df[(df['weathersit'] == weather_filter) & (df['workingday'] == workingday_filter)]

# Main content
st.title("Bike Sharing Dashboard")
st.markdown("""
Dashboard ini menampilkan visualisasi dari data penyewaan sepeda harian.
Gunakan filter di sidebar untuk menyesuaikan kondisi cuaca dan tipe hari.
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda Harian")
    fig, ax = plt.subplots(figsize=(8, 5))  # Create figure and axes
    sns.boxplot(x='weathersit', y='cnt', data=df, palette='coolwarm', ax=ax) # Use ax
    ax.set_title('Pengaruh Cuaca terhadap Penyewaan Sepeda Harian')
    ax.set_xlabel('Kondisi Cuaca (1=Cerah, 2=Mendung, 3=Hujan Ringan/Salju, 4=Hujan Lebat/Salju)')
    ax.set_ylabel('Jumlah Penyewaan')
    plt.tight_layout() # Important!
    st.pyplot(fig)  # Pass the figure to st.pyplot

with col2:
    st.subheader("Pola Peminjaman Sepeda: Hari Kerja vs. Akhir Pekan")
    fig, ax = plt.subplots(figsize=(8, 5)) # Create figure and axes
    sns.boxplot(x='workingday', y='cnt', data=df, palette='muted', ax=ax)  # Use ax
    ax.set_title('Pola Peminjaman Sepeda: Hari Kerja vs. Akhir Pekan')
    ax.set_xlabel('Hari Kerja (0 = Akhir Pekan, 1 = Hari Kerja)')
    ax.set_ylabel('Jumlah Penyewaan')
    plt.tight_layout() # Important!
    st.pyplot(fig) # Pass the figure to st.pyplot


st.subheader("Data Penyewaan Sepeda (Filtered)")
st.dataframe(df_filtered.head(20)) # Limit displayed rows if needed
