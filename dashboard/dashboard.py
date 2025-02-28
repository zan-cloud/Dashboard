import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime as dt

# Load dataset dengan cache agar tidak berulang kali dibaca
@st.cache_data
def load_data():
    customers = pd.read_csv("data/customers_dataset.csv")
    orders = pd.read_csv("data/orders_dataset.csv") 
    order_items = pd.read_csv("data/order_items_dataset.csv")
    order_payments = pd.read_csv("data/order_payments_dataset.csv")
    products = pd.read_csv("data/products_dataset.csv")
    return customers, orders, order_items, order_payments, products

# Load data
customers, orders, order_items, order_payments, products = load_data()

# Pastikan format timestamp sesuai
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])

# UI Streamlit
st.title("Dashboard Analisis Produk")

# Pilih rentang tanggal
min_date = orders['order_purchase_timestamp'].min()
max_date = orders['order_purchase_timestamp'].max()
default_start = max_date - pd.DateOffset(months=6)  # Default 6 bulan terakhir

start_date, end_date = st.date_input("Pilih Rentang Waktu:", [default_start, max_date], min_value=min_date, max_value=max_date)

# Pastikan format tanggal sesuai
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter data berdasarkan tanggal yang dipilih
filtered_orders = orders[(orders['order_purchase_timestamp'] >= start_date) & (orders['order_purchase_timestamp'] <= end_date)]

# Gabungkan orders dengan order_items
merged_data = filtered_orders.merge(order_items, on='order_id', how='left')

# Gabungkan lagi dengan tabel produk untuk mendapatkan kategori
merged_data = merged_data.merge(products[['product_id', 'product_category_name']], on='product_id', how='left')
merged_data['product_category_name'] = merged_data['product_category_name'].fillna('Unknown')

# Hitung jumlah order per kategori
category_counts = merged_data['product_category_name'].value_counts().reset_index()
category_counts.columns = ['product_category', 'total_orders']

# Analisis One-Time Buyers
customer_orders = filtered_orders.groupby('customer_id')['order_id'].count().reset_index()
customer_orders.columns = ['customer_id', 'order_count']
one_time_buyers = customer_orders[customer_orders['order_count'] == 1]
one_time_orders = filtered_orders[filtered_orders['customer_id'].isin(one_time_buyers['customer_id'])]
one_time_order_items = one_time_orders.merge(order_items, on='order_id', how='inner')
one_time_order_items = one_time_order_items.merge(products[['product_id', 'product_category_name']], on='product_id', how='left')
one_time_order_items['product_category_name'] = one_time_order_items['product_category_name'].fillna('Unknown')
one_time_category_counts = one_time_order_items['product_category_name'].value_counts().reset_index()
one_time_category_counts.columns = ['product_category', 'total_orders']

# Visualisasi Tren Pembelian
st.header("Tren Pembelian Berdasarkan Kategori Produk")
st.write(f"Menampilkan 10 kategori produk dengan jumlah order terbanyak dalam rentang {start_date.date()} - {end_date.date()}.")
fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.barplot(data=category_counts.head(10), x="total_orders", y="product_category", palette="coolwarm", ax=ax1)
ax1.set_title("Top 10 Kategori Produk dengan Order Terbanyak")
ax1.set_xlabel("Total Order")
ax1.set_ylabel("Kategori Produk")
st.pyplot(fig1)

# Visualisasi One-Time Buyers
st.header("Pola Kategori Produk dari One-Time Buyers")
st.write(f"Menampilkan 10 kategori produk yang paling banyak dibeli oleh pelanggan one-time buyers dalam rentang {start_date.date()} - {end_date.date()}.")
fig2, ax2 = plt.subplots(figsize=(12, 6))
ax2.barh(one_time_category_counts['product_category'][:10], one_time_category_counts['total_orders'][:10], color='skyblue')
ax2.set_xlabel("Total Orders")
ax2.set_ylabel("Product Category")
ax2.set_title("Top 10 Product Categories Bought by One-Time Buyers")
ax2.invert_yaxis()
st.pyplot(fig2)
