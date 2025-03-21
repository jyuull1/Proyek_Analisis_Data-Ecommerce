import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
df_order_payments = pd.read_csv('data/order_payments_dataset.csv')
df_sellers = pd.read_csv('data/sellers_dataset.csv')
df_geo = pd.read_csv('data/geolocation_dataset.csv')

# Data Cleaning
df_order_payments = df_order_payments[df_order_payments['payment_type'] != 'not_defined']
df_geo.drop_duplicates(inplace=True)
df_geo.dropna(inplace=True)

# Sidebar Filters
st.sidebar.header("Filter Data")
payment_filter = st.sidebar.multiselect("Pilih Metode Pembayaran:", df_order_payments['payment_type'].unique())
city_filter = st.sidebar.multiselect("Pilih Kota Penjual:", df_sellers['seller_city'].unique())

# Apply Filters
if payment_filter:
    df_order_payments = df_order_payments[df_order_payments['payment_type'].isin(payment_filter)]
if city_filter:
    df_sellers = df_sellers[df_sellers['seller_city'].isin(city_filter)]

# Tab Layout
tab1, tab2 = st.tabs(["Interaktif", "Statis"])

# Tab 1 - Interaktif
with tab1:
    st.subheader("Distribusi Metode Pembayaran")
    payment_counts = df_order_payments['payment_type'].value_counts().reset_index()
    payment_counts.columns = ['Jenis Pembayaran', 'Total Transaksi']
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=payment_counts, x='Jenis Pembayaran', y='Total Transaksi', palette='coolwarm', ax=ax)
    plt.xticks(rotation=30)
    st.pyplot(fig)

    st.write("**Credit card** adalah metode pembayaran yang paling banyak digunakan, sedangkan **Boleto** berada di posisi kedua, dengan jumlah transaksi yang jauh lebih rendah dibandingkan credit card, **Voucher dan debit card** memiliki jumlah transaksi yang lebih sedikit."
    )

    
    st.subheader("Kota dengan Jumlah Penjual Terbanyak")
    top_cities = df_sellers['seller_city'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=top_cities.values, y=top_cities.index, palette='viridis', ax=ax)
    st.pyplot(fig)
    
    st.write("Kota Sao Paulo memiliki jumlah penjual terbanyak, jauh melampaui kota-kota lainnya. Hal ini menunjukkan bahwa Sao Paulo merupakan pusat aktivitas perdagangan yang dominan dibandingkan kota lain di Brasil. Kota-kota seperti Curitiba, Rio de Janeiro, dan Belo Horizonte juga memiliki jumlah penjual yang signifikan, tetapi masih jauh di bawah Sao Paulo.")

# Tab 2 - Statis
with tab2:
    st.subheader("Scatter Plot Distribusi Nilai Transaksi")

    def categorize_value(value):
        if value < 200:
            return 'pink'
        elif 200 <= value < 600:
            return 'lightpink'
        elif 600 <= value < 1200:
            return 'violet'
        elif 1200 <= value < 5000:
            return 'orchid'
        elif 5000 <= value < 10000:
            return 'hotpink'
        else:
            return 'magenta'
    
    color_mapping = df_order_payments['payment_value'].apply(categorize_value)
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    plt.scatter(df_order_payments.index, df_order_payments['payment_value'], c=color_mapping.map({'pink': 'pink', 'lightpink': 'lightpink', 'violet': 'violet', 'orchid': 'orchid', 'hotpink': 'hotpink', 'magenta': 'magenta'}), alpha=0.6)
    plt.title("Scatter Plot Distribusi Nilai Transaksi")
    plt.xlabel("Indeks Transaksi")
    plt.ylabel("Nilai Transaksi")
    plt.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig3)

    st.write("Scatter plot ini menunjukkan distribusi nilai transaksi berdasarkan indeks transaksi. Sebagian besar transaksi memiliki nilai yang relatif rendah, dengan mayoritas berada di bawah **2000**. Namun, terdapat beberapa transaksi dengan nilai yang jauh lebih tinggi, yang ditandai sebagai outlier. Pola ini mengindikasikan bahwa meskipun sebagian besar transaksi bernilai kecil hingga menengah, ada beberapa transaksi bernilai besar yang dapat mempengaruhi distribusi keseluruhan.")
    
    
    # Menampilkan Density Contour Plot (KDE)
    st.subheader("Density Contour Plot dari Lokasi Penjual")
    if 'geolocation_lat' in df_geo.columns and 'geolocation_lng' in df_geo.columns:
        df_sample = df_geo.sample(n=5000, random_state=42) if len(df_geo) > 5000 else df_geo
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        sns.kdeplot(
            x=df_sample['geolocation_lng'],
            y=df_sample['geolocation_lat'],
            cmap="Purples",
            fill=True,
            bw_adjust=2,
            ax=ax4
        )
        ax4.set_title("Density Contour Plot dari Lokasi Penjual")
        ax4.set_xlabel("Longitude")
        ax4.set_ylabel("Latitude")
        st.pyplot(fig4)

    st.write("Density Contour Plot ini menunjukkan distribusi lokasi penjual berdasarkan koordinat geografis (longitude dan latitude). Area dengan warna lebih gelap menunjukkan konsentrasi penjual yang lebih tinggi, sedangkan area yang lebih terang menunjukkan kepadatan yang lebih rendah. Dari pola ini, dapat disimpulkan bahwa sebagian besar penjual terkonsentrasi di suatu wilayah tertentu, yang kemungkinan besar merupakan pusat ekonomi atau kota besar.")
    
    
    # Menampilkan Hexbin Plot
    st.subheader("Hexbin Plot dari Lokasi Penjual")
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    hb = ax5.hexbin(df_sample['geolocation_lng'], df_sample['geolocation_lat'], gridsize=50, cmap='Purples', mincnt=1)
    plt.colorbar(hb, ax=ax5, label="Density")
    ax5.set_xlabel("Longitude")
    ax5.set_ylabel("Latitude")
    ax5.set_title("Hexbin Plot dari Lokasi Penjual")
    st.pyplot(fig5)

    st.write("Hexbin Plot ini menunjukkan distribusi lokasi penjual dengan menggunakan heksagon sebagai representasi kepadatan. Warna yang lebih gelap menunjukkan area dengan jumlah penjual yang lebih tinggi, sedangkan warna yang lebih terang menunjukkan kepadatan yang lebih rendah. Dari plot ini, dapat dilihat bahwa sebagian besar penjual terkonsentrasi di wilayah tertentu, yang kemungkinan merupakan kota besar atau pusat perdagangan utama.")

import streamlit as st  

 
# FOOTER
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: white;
        text-align: center;
        padding: 10px;
        font-size: 12px;
        color: gray;
    }
    </style>
    <div class="footer">
        Created by <b>Juli Arsi Sabrina</b>
    </div>
    """,
    unsafe_allow_html=True
)