# bike-rental-analysis
## Deskripsi Proyek

Proyek ini bertujuan untuk menganalisis dataset penyewaan sepeda harian yang mencakup catatan penyewaan sepeda, informasi kondisi cuaca (seperti suhu, kelembaban, dan kecepatan angin), serta indikator hari kerja dan akhir pekan. Analisis dilakukan untuk menjawab dua pertanyaan bisnis utama:

- **Bagaimana pengaruh cuaca terhadap jumlah penyewaan sepeda harian?**
- **Apa perbedaan pola peminjaman sepeda antara hari kerja dan akhir pekan?**

Proyek ini mencakup seluruh proses analisis data mulai dari pengumpulan data, pembersihan data, eksplorasi data, hingga pembuatan visualisasi interaktif menggunakan Streamlit. Selain itu, disediakan juga dashboard interaktif untuk memudahkan eksplorasi temuan secara real-time.

## Struktur Folder

```plaintext
Bike-Sharing-Data-Analysis/
├── dashboard/
│   └── dashboard.py       # Skrip dashboard interaktif menggunakan Streamlit
│   └── main_data.csv
├── data/                  # Folder berisi file CSV (misalnya: day.csv)
│   └── day.csv
├── notebook.ipynb         # Jupyter Notebook berisi proses analisis data
├── README.md              # File ini
└── requirements.txt       # Daftar library Python yang dibutuhkan
