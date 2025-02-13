import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

st.write("Memuat data...")  # User feedback
with st.spinner("Loading data..."):
    try:
        raw_df = load_data()
        st.write("Data berhasil dimuat!")  # User feedback
    except FileNotFoundError:
        st.error("File day.csv tidak ditemukan. Pastikan file ini ada di direktori yang sama dengan script Anda dan sudah di-commit ke repository GitHub Anda.")
        st.stop()  # Stop execution if file not found
    except Exception as e:  # Catch other potential errors
        st.exception(e)
        st.stop()


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
