# Import library utama
import pandas as pd  # Manipulasi data
import numpy as np  # Operasi numerik
import matplotlib.pyplot as plt  # Visualisasi dasar
import seaborn as sns  # Visualisasi lebih keren
import streamlit as st

# Library tambahan untuk analisis lebih dalam
import datetime as dt  # Untuk manipulasi tanggal


# Konfigurasi visualisasi
sns.set(style="whitegrid")
plt.style.use("ggplot")

# Import dataset yang diperlukan
@st.cache_data
def load_data():
    customers = pd.read_csv("data/customers_dataset.csv")
    orders = pd.read_csv("data/orders_dataset.csv") 
    order_items = pd.read_csv("data/order_items_dataset.csv")
    order_payments = pd.read_csv("data/order_payments_dataset.csv")
    products = pd.read_csv("data/products_dataset.csv")

    return customers, orders, order_items, order_payments, products

# Memuat dataset
customers, orders, order_items, order_payments, products = load_data()


# Cek apakah dataset berhasil dimuat
print("=" * 50)
print("Preview Dataset Orders")
print("=" * 50)
print(orders.head(), "\n")

print("=" * 50)
print("Preview Dataset Order Items")
print("=" * 50)
print(order_items.head(), "\n")

print("=" * 50)
print("Preview Dataset Products")
print("=" * 50)
print(products.head())


# Cek info struktur dataset
print("=" * 60)
print("Struktur Dataset Orders")
print("=" * 60)
print(orders.info(), "\n")

print("=" * 60)
print("Struktur Dataset Order Items")
print("=" * 60)
print(order_items.info(), "\n")

print("=" * 60)
print(" Struktur Dataset Products")
print("=" * 60)
print(products.info(), "\n")

# Cek missing values
print("=" * 60)
print(" Cek Missing Values")
print("=" * 60)
print("Orders:\n", orders.isnull().sum(), "\n")
print("Order Items:\n", order_items.isnull().sum(), "\n")
print("Products:\n", products.isnull().sum(), "\n")

# Cek duplikasi
print("=" * 60)
print("Cek Data Duplikasi")
print("=" * 60)
print(f"Jumlah duplikasi di Orders      : {orders.duplicated().sum()}")
print(f"Jumlah duplikasi di Order Items : {order_items.duplicated().sum()}")
print(f"Jumlah duplikasi di Products    : {products.duplicated().sum()}")
print("=" * 60)



# Menghapus duplikasi pada setiap dataset
orders.drop_duplicates(inplace=True)
order_items.drop_duplicates(inplace=True)
products.drop_duplicates(inplace=True)

# Mengisi missing values pada kategori produk dengan 'Unknown'
products['product_category_name'] = products['product_category_name'].fillna('Unknown')

# Menghapus baris yang memiliki order_purchase_timestamp kosong (tidak bisa diperbaiki)
orders.dropna(subset=['order_purchase_timestamp'], inplace=True)

# Mengisi order_approved_at dengan order_purchase_timestamp jika kosong
orders['order_approved_at'] = orders['order_approved_at'].fillna(orders['order_purchase_timestamp'])

# Mengisi order_delivered_carrier_date dengan "Unknown" karena tidak ada data valid untuk dipakai
orders['order_delivered_carrier_date'] = orders['order_delivered_carrier_date'].fillna("Unknown")

# Mengisi order_delivered_customer_date dengan order_estimated_delivery_date jika kosong
orders['order_delivered_customer_date'] = orders['order_delivered_customer_date'].fillna(orders['order_estimated_delivery_date'])

# Mengisi missing values pada atribut produk dengan nilai median untuk menghindari distorsi data
products.loc[:, 'product_name_lenght'] = products['product_name_lenght'].fillna(products['product_name_lenght'].median())
products.loc[:, 'product_description_lenght'] = products['product_description_lenght'].fillna(products['product_description_lenght'].median())
products.loc[:, 'product_photos_qty'] = products['product_photos_qty'].fillna(products['product_photos_qty'].median())

products.loc[:, 'product_weight_g'] = products['product_weight_g'].fillna(products['product_weight_g'].median())
products.loc[:, 'product_length_cm'] = products['product_length_cm'].fillna(products['product_length_cm'].median())
products.loc[:, 'product_height_cm'] = products['product_height_cm'].fillna(products['product_height_cm'].median())
products.loc[:, 'product_width_cm'] = products['product_width_cm'].fillna(products['product_width_cm'].median())

# Menampilkan jumlah missing values setelah cleaning
print("\n" + "=" * 60)
print("============== Missing Values Setelah Cleaning ==============")
print("\nOrders:\n", orders.isnull().sum().to_string())       # Cek missing values pada orders
print("\nOrder Items:\n", order_items.isnull().sum().to_string())  # Cek missing values pada order_items
print("\nProducts:\n", products.isnull().sum().to_string())   # Cek missing values pada products
print("=" * 60)

# Menampilkan jumlah duplikasi setelah cleaning
print("\n" + "=" * 60)
print("============== Jumlah Duplikasi Setelah Cleaning ==============")
print(f"Orders      : {orders.duplicated().sum():,}")      # Cek jumlah duplikasi di orders
print(f"Order Items : {order_items.duplicated().sum():,}") # Cek jumlah duplikasi di order_items
print(f"Products    : {products.duplicated().sum():,}")    # Cek jumlah duplikasi di products
print("=" * 60)



# Pastikan format timestamp sesuai
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])

# Ambil tanggal terbaru dalam dataset
latest_date = orders['order_purchase_timestamp'].max()

# Hitung batas 6 bulan terakhir
six_months_ago = latest_date - pd.DateOffset(months=6)

# Filter data dalam rentang 6 bulan terakhir
orders_last_6_months = orders[orders['order_purchase_timestamp'] >= six_months_ago]

# Gabungkan orders dengan order_items
merged_data = orders_last_6_months.merge(order_items, on='order_id', how='left')

# Gabungkan lagi dengan tabel produk untuk mendapatkan kategori
merged_data = merged_data.merge(products[['product_id', 'product_category_name']], on='product_id', how='left')

# Pastikan tidak ada kategori yang kosong
merged_data['product_category_name'] = merged_data['product_category_name'].fillna('Unknown')

# Hitung jumlah order per kategori
category_counts = merged_data['product_category_name'].value_counts().reset_index()
category_counts.columns = ['product_category', 'total_orders']

# Print hasil dalam format yang lebih rapi
print("=" * 60)
print("Top 10 Kategori Produk dengan Order Terbanyak dalam 6 Bulan Terakhir")
print("=" * 60)
print(category_counts.head(10).to_string(index=False))
print("=" * 60, "\n")

# Pertanyaan 2

# Hitung jumlah transaksi per pelanggan
customer_orders = orders.groupby('customer_id')['order_id'].count().reset_index()
customer_orders.columns = ['customer_id', 'order_count']

# Identifikasi one-time buyers (pelanggan dengan hanya 1 transaksi)
one_time_buyers = customer_orders[customer_orders['order_count'] == 1]

# Gabungkan dengan orders untuk mendapatkan order_id mereka
one_time_orders = orders[orders['customer_id'].isin(one_time_buyers['customer_id'])]

# Gabungkan dengan order_items untuk mendapatkan product_id
one_time_order_items = one_time_orders.merge(order_items, on='order_id', how='inner')

# Gabungkan dengan products untuk mendapatkan kategori produk
one_time_order_items = one_time_order_items.merge(products[['product_id', 'product_category_name']], on='product_id', how='left')

# Pastikan tidak ada kategori kosong
one_time_order_items['product_category_name'] = one_time_order_items['product_category_name'].fillna('Unknown')

# Hitung jumlah pembelian per kategori produk untuk one-time buyers
one_time_category_counts = one_time_order_items['product_category_name'].value_counts().reset_index()
one_time_category_counts.columns = ['product_category', 'total_orders']

# Print hasil
print("=" * 60)
print("Kategori Produk yang Dibeli oleh One-Time Buyers")
print("=" * 60)
print(one_time_category_counts.head(10).to_string(index=False))
print("=" * 60)

# Set judul utama aplikasi di Streamlit
st.title("Analisis Kategori Produk dalam 6 Bulan Terakhir")

# ================== PERTANYAAN 1 ==================
st.header("Pertanyaan 1: Bagaimana Tren Pembelian dalam 6 Bulan Terakhir?")
st.write("Grafik di bawah ini menunjukkan 10 kategori produk dengan jumlah order terbanyak dalam 6 bulan terakhir.")

# **Visualisasi Pertanyaan 1: Top 10 Kategori Produk dengan Order Terbanyak**
fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.barplot(
    data=category_counts.head(10),
    x="total_orders",
    y="product_category",
    hue="product_category",
    palette="coolwarm",
    legend=False,
    ax=ax1
)
ax1.set_title("Top 10 Kategori Produk dengan Order Terbanyak (6 Bulan Terakhir)", fontsize=14, fontweight="bold")
ax1.set_xlabel("Total Order", fontsize=12)
ax1.set_ylabel("Kategori Produk", fontsize=12)
sns.despine(left=True, bottom=True)

# Tampilkan di Streamlit
st.pyplot(fig1)

# ================== PERTANYAAN 2 ==================
st.header(" Pertanyaan 2: Pola Kategori Produk dari One-Time Buyers?")
st.write("Grafik di bawah ini menunjukkan 10 kategori produk yang paling banyak dibeli oleh pelanggan yang hanya melakukan satu kali transaksi (one-time buyers).")

# **Visualisasi Pertanyaan 2: Top 10 Kategori One-Time Buyers**
fig2, ax2 = plt.subplots(figsize=(12, 6))
ax2.barh(one_time_category_counts['product_category'][:10], one_time_category_counts['total_orders'][:10], color='skyblue')
ax2.set_xlabel("Total Orders")
ax2.set_ylabel("Product Category")
ax2.set_title("Top 10 Product Categories Bought by One-Time Buyers")
ax2.invert_yaxis()  # Membalik sumbu Y agar kategori terbanyak di atas

# Tampilkan di Streamlit
st.pyplot(fig2)