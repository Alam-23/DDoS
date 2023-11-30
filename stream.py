# Import library Streamlit
import streamlit as st
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Line
from pyecharts.charts import Bar
import plotly.express as px


# Judul halaman
st.title('Kelompok 8 PKDJK')

# Menampilkan nama kelompok satu per satu
st.write('2210511061 - Rofief Amanulloh')
st.write('2210511063 - Daffa Bagus Maulana')
st.write('2210511068 - Muhammad Nur Alam')
st.write('2210511080 - Muhammad Reza Adi Pratama')




# Membuat expander untuk penjelasan DDoS
with st.expander("**Apa itu DDoS?**"):
    st.write("""
        **DDoS (Distributed Denial of Service)**
        
        DDoS adalah serangan yang dilakukan dengan cara membanjiri layanan atau sumber daya komputer dengan sejumlah besar permintaan, 
        sehingga layanan tersebut menjadi tidak dapat diakses oleh pengguna yang seharusnya. Serangan DDoS biasanya dilakukan 
        dari berbagai sumber (distributed), membuatnya sulit untuk dihadapi.
        
        Tujuan utama serangan DDoS adalah membuat layanan menjadi tidak responsif atau tidak tersedia untuk pengguna yang 
        seharusnya dapat mengaksesnya. Serangan ini dapat menyebabkan gangguan besar pada layanan online dan bisnis.
        
        Pada umumnya, serangan DDoS menggunakan jaringan botnet, yaitu sejumlah besar perangkat yang terinfeksi oleh malware 
        dan dapat dikendalikan oleh penyerang tanpa sepengetahuan pemiliknya.
        
        **Cara Melindungi Diri dari Serangan DDoS:**
        - Menggunakan layanan keamanan DDoS.
        - Memantau lalu lintas jaringan untuk deteksi dini.
        - Konfigurasi firewall yang kuat.
        - Menyediakan cadangan dan distribusi lalu lintas.
        """)

# Membaca data CSV
data = pd.read_csv('./Labels/CICDS_Wednesday.csv')

# Menampilkan data
st.header('Data CICDS_Wednesday.csv')
st.write(data.head())

# Menghitung jumlah paket per label
jumlah_paket_per_label = data[' Label'].value_counts().reset_index()
jumlah_paket_per_label.columns = ['Label', 'Jumlah Paket']

# Membuat grafik batang menggunakan Plotly Express
fig = px.bar(jumlah_paket_per_label, x='Label', y='Jumlah Paket', title='Jumlah Paket per Label', color='Label')
fig.update_layout(xaxis=dict(tickangle=45))

# Menambahkan header "Tipe Label DDoS"
st.header('Tipe Label DDoS')

# Menampilkan grafik menggunakan Plotly
st.plotly_chart(fig, use_container_width=True)


df_plot = data 
# Membuat DataFrame baru dengan kolom Timestamp yang diubah
df_plot_updated = df_plot.copy()
df_plot_updated[' Timestamp'] = pd.to_datetime(df_plot_updated[' Timestamp'])

# Menghitung jumlah serangan per timestamp
df_trend = df_plot_updated.groupby([' Timestamp', ' Label']).size().unstack(fill_value=0)

# Membuat grafik garis menggunakan Plotly Express
fig = px.line(df_trend, x=df_trend.index, y=df_trend.columns, title='Grafik Serangan Seiring Waktu perLabel')

# Konfigurasi grafik
fig.update_layout(
    xaxis=dict(type='category', tickangle=45, tickfont=dict(size=10)),
    yaxis=dict(title='Jumlah Serangan'),
    legend=dict(orientation='v', xanchor='left', x=1, yanchor='top', y=1)
)

# Menambahkan header "Trend Serangan Seiring Waktu"
st.header('Trend Serangan Seiring Waktu')

# Menampilkan grafik menggunakan Plotly Express di Streamlit
st.plotly_chart(fig, use_container_width=True)



# DataFrame Anda
df_plot = data[[' Source IP', ' Label']]
df_plot = df_plot.groupby(by=[' Source IP', ' Label']).agg({' Label': 'count'}).rename(columns={' Label': 'Count'})
df_plot = df_plot.reset_index()

# Mengurutkan berdasarkan jumlah serangan dalam urutan menurun
df_plot_sorted = df_plot.sort_values(by=['Count'], ascending=False)

# Mengambil 5 alamat IP teratas untuk setiap label
top_ips = df_plot_sorted.groupby(' Label').head(5)

# Membuat grafik batang menggunakan Plotly Express
fig = px.bar(top_ips, x=' Source IP', y='Count', color=' Label', barmode='stack',
             title='Top 5 Alamat IP Teratas yang Sering Melakukan Serangan untuk Setiap Kategori Label')

# Konfigurasi grafik
fig.update_layout(
    xaxis=dict(type='category', categoryorder='total descending', tickangle=45, tickfont=dict(size=10)),
    yaxis=dict(title='Jumlah Serangan'),
    legend=dict(orientation='v', xanchor='left', x=1, yanchor='top', y=1)
)

# Menambahkan header "Top 5 Alamat IP Teratas"
st.header('Top 5 Alamat IP Teratas yang Sering Melakukan Serangan')

# Menampilkan grafik menggunakan Plotly Express di Streamlit
st.plotly_chart(fig, use_container_width=True)


# Menghitung jumlah serangan per port
top_ports = data[' Destination Port'].value_counts().nlargest(5).reset_index()
top_ports.columns = ['Destination Port', 'Jumlah Serangan']

# Membuat grafik batang menggunakan Plotly Express
fig = px.bar(top_ports, x='Destination Port', y='Jumlah Serangan',
             title='Grafik 5 Port Teratas yang Sering Menjadi Tujuan Serangan')

# Konfigurasi grafik
fig.update_layout(
    xaxis=dict(type='category', categoryorder='total descending'),
    yaxis=dict(title='Jumlah Serangan'),
)

# Menambahkan header "Top 5 Port Teratas"
st.header('Top 5 Port Teratas yang Sering Menjadi Tujuan Serangan')

# Menampilkan grafik menggunakan Plotly Express di Streamlit
st.plotly_chart(fig, use_container_width=True)


