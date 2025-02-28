Berikut isi **README.md** yang bisa kamu gunakan untuk proyek ini:

---

# 📊 Dashboard Analisis Data Penjualan

## 📌 Deskripsi Proyek

Proyek ini bertujuan untuk menganalisis tren pembelian pelanggan dalam 6 bulan terakhir serta memahami pola pembelian pelanggan one-time buyer. Hasil analisis ditampilkan dalam dashboard interaktif menggunakan **Streamlit**.

## 🚀 Link Dashboard

Aplikasi sudah berhasil dideploy di **Streamlit Cloud** dan bisa diakses melalui:  
🔗 [https://dashboard-jlhvepdg4r9rqppxvyzahs.streamlit.app/](https://dashboard-jlhvepdg4r9rqppxvyzahs.streamlit.app/)

## 📂 Struktur Folder

```
submission
├───dashboard
│   ├───dashboard.py
├───data
│   ├───customers_dataset.csv
│   ├───order_items_dataset.csv
│   ├───order_payments_dataset.csv
│   ├───order_reviews_dataset.csv
│   ├───orders_dataset.csv
│   ├───product_category_name_translation.csv
│   ├───products_dataset.csv
├───Dokumentasi Analisis Data.ipynb
├───Notebook.ipynb
├───README.md
├───requirements.txt
└───url.txt
```

## 📊 Fitur Analisis

✅ **Tren Penjualan**: Menampilkan 10 kategori produk dengan jumlah order terbanyak dalam 6 bulan terakhir.  
✅ **Pola One-Time Buyer**: Menunjukkan kategori produk yang sering dibeli oleh pelanggan one-time buyer.  
✅ **Visualisasi Interaktif**: Menggunakan **matplotlib** dan **seaborn** untuk menampilkan grafik yang mudah dipahami.  
✅ **Analisis Lanjutan**:

- **Pertanyaan 1 (Tren Penjualan)**: Menggunakan distribusi frekuensi dan analisis time-series sederhana untuk melihat pola tren dalam 6 bulan terakhir.
- **Pertanyaan 2 (One-Time Buyer)**: Menggunakan segmentasi pelanggan dan perbandingan proporsi antar kategori untuk memahami produk yang lebih menarik bagi pembeli baru.

---

## 🛠️ Cara Menjalankan Lokal

Jika ingin menjalankan proyek ini di lokal, ikuti langkah berikut:

1. **Clone Repository**

   ```sh
   git clone https://github.com/zan-cloud/Dashboard.git
   cd Dashboard
   ```

2. **Buat Virtual Environment (Opsional, tapi disarankan)**

   ```sh
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate  # Windows
   ```

3. **Install Dependencies**

   ```sh
   pip install -r requirements.txt
   ```

4. **Jalankan Streamlit**
   ```sh
   streamlit run dashboard/dashboard.py
   ```

## 🔧 Teknologi yang Digunakan

- **Python**: Analisis data
- **Pandas, NumPy**: Manipulasi data
- **Matplotlib, Seaborn**: Visualisasi
- **Streamlit**: Pembuatan dashboard interaktif

## 📬 Feedback

Jika ada pertanyaan atau masukan, jangan ragu untuk menghubungi saya! 🚀🔥

---
