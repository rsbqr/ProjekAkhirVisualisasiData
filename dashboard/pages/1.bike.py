#import
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')
# function untuk dataframe pesepeda casual
def buat_harian_biasa_df(df):
    harian_biasa_df = df.resample(rule ='D', on='dteday').agg({
        "casual": "sum"
    })
    return harian_biasa_df

# function untuk dataframe pesepeda terdaftar
def buat_harian_terdaftar_df(df):
    harian_terdaftar_df = df.resample(rule ='D', on='dteday').agg({
        "dteday": "nunique",
        "registered": "sum"
    })
    return harian_terdaftar_df

# function casual pengelompokan (grup) per musim
def buat_biasa_per_musim_df(df):
    biasa_per_musim_df = df.groupby(by="season").casual.sum().reset_index()
    # biasa_per_musim_df.rename(columns={
    #     "casual": "kasual"
    # }, inplace=True)
    biasa_per_musim_df['season'] = pd.Categorical(biasa_per_musim_df['season'], [1,2,3,4])
    biasa_per_musim_df.rename(columns={
        1:  "springer",
        2:  "summer",
        3:  "fall",
        4:  "winter"
    }, inplace=True)
    return biasa_per_musim_df

# function registered pengelompokan per musim
def buat_terdaftar_per_musim_df(df):
    terdaftar_per_musim_df = df.groupby(by="season").registered.sum().reset_index()
    # biasa_per_musim_df.rename(columns={
    #     "casual": "kasual"
    # }, inplace=True)
    terdaftar_per_musim_df['season'] = pd.Categorical(biasa_per_musim_df['season'], [1,2,3,4])
    
    return terdaftar_per_musim_df

# function casual pengelompokan (grup) per musim
def buat_biasa_per_bulan_df(df):
    biasa_per_bulan_df = df.groupby(by="mnth").casual.sum().sort_values(ascending=False).reset_index()
    # biasa_per_bulan_df.rename(columns={
    #     "mnth": "bulan"
    # }, inplace=True)
    biasa_per_bulan_df['mnth'] = pd.Categorical(biasa_per_bulan_df['mnth'], [1,2,3,4,5,6,7,8,9,10,11,12])
    
    return biasa_per_bulan_df

# function registered pengelompokan per musim
def buat_terdaftar_per_bulan_df(df):
    terdaftar_per_bulan_df = df.groupby(by="mnth").registered.sum().sort_values(ascending=False).reset_index()
    # terdaftar_per_bulan_df.rename(columns={
    #     # "mnth": "bulan"
    # }, inplace=True)
    terdaftar_per_bulan_df['mnth'] = pd.Categorical(biasa_per_bulan_df['mnth'], [1,2,3,4,5,6,7,8,9,10,11,12])
    
    return terdaftar_per_bulan_df

# function pesepeda casual per season diurut
def buat_musim_biasa_df(df):
    musim_biasa_df = df.groupby("season").casual.sum().sort_values(ascending=True).reset_index()
    return musim_biasa_df

# function yg terdaftar
def buat_musim_terdaftar_df(df):
    musim_terdaftar_df = df.groupby("season").registered.sum().sort_values(ascending=False).reset_index()
    return musim_terdaftar_df

# function untuk dataframe rata2 pesepeda casual
def buat_rata2_harian_biasa_df(df):
    biasa_rata2_musim_df = df.groupby(by="season").casual.mean().reset_index()
    biasa_rata2_musim_df.rename(columns={
        "casual": "kasual"
    }, inplace=True)
    return biasa_rata2_musim_df

# function untuk dataframe rata2 pesepeda terdaftar
def buat_rata2_harian_terdaftar_df(df):
    harian_rata2_terdaftar_df = df.resample(rule ='D', on='dteday').agg({
        "season": "nunique",
        "registered": "mean"
    })
    return harian_rata2_terdaftar_df

# function sort by musim (season) casual
def buat_biasa_musim_df(df):
    biasa_musim_df = df.groupby(by="season").dteday.nunique().reset_index()
    biasa_musim_df.rename(columns={
        "dteday": "tgl",
        "casual":"mean"
    }, inplace=True)
    
    return biasa_musim_df

# def buat_rfm_musim_df(df):
#     rfm_musim_df=df.groupby(by="season",as_index=False).agg({
#     "dteday":"max",
#     "instant":"nunique",
#     "cnt":"max" #cnt: gabungan casual dan daftar
#     })
#     rfm_musim_df.columns =["dteday","max_cnt","freq"]
    
#     rfm_musim_df["max_cnt"] = rfm_musim_df["max_cnt"].dt.date
#     tgl_terkini = df["dteday"].dt.date.max()
#     rfm_musim_df["terkini"] = rfm_musim_df["max_cnt"].apply(lambda x: (tgl_terkini - x).days)
#     rfm_musim_df.drop("max_cnt", axis=1, inplace=True)
    
#     return rfm_df()


# data bersih
data_df = pd.read_csv("main_data.csv")

# convert dteday object > date
# dteday_df=pd.data_df({"dteday"})
# pd.to_datetime(dteday_df["dteday"],infer_datetime_format=True)

# bikin tampilan tanggalan
datetime_columns = ["dteday"] #variabel untuk simpan tanggal
data_df.sort_values(by="dteday", inplace=True)
data_df.reset_index(inplace=True)

# eksekusi looping untuk tanggalan 
# dgn column sbg variabel baru 
# untuk simpan index dan convert ke datetime
for column in datetime_columns:
    data_df[column] = pd.to_datetime(data_df[column])#,infer_datetime_format=True)


# filter
min_date = data_df["dteday"].min()
max_date = data_df["dteday"].max()

# menu sidebar
with st.sidebar:
    #logo
    url="https://www.flaticon.com/free-stickers/bycicle"
    st.image("https://raw.githubusercontent.com/rsbqr/ProjekAkhirVisualisasiData/main/mountain-bike.png")
    st.caption("by [flaticon](%s)" % url)
    # st.caption("<style ='text align :center;'> by [flaticon](%s)" % url, unsafe_allow_html=True) 
    
    
    #tanggalan
    start_date, end_date = st.date_input(
        label='Pilih Rentang Tanggal',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

#dataframe 
utama_df = data_df[(data_df["dteday"] >= str(start_date)) & 
                (data_df["dteday"] <= str(end_date))]

#eksekusi dataframe
harian_biasa_df = buat_harian_biasa_df(utama_df)
harian_terdaftar_df = buat_harian_terdaftar_df(utama_df)
biasa_per_musim_df = buat_biasa_per_musim_df(utama_df)
terdaftar_per_musim_df = buat_terdaftar_per_musim_df(utama_df)
biasa_per_bulan_df = buat_biasa_per_bulan_df(utama_df)
terdaftar_per_bulan_df = buat_terdaftar_per_bulan_df(utama_df)

musim_biasa_df = buat_musim_biasa_df(utama_df)
musim_terdaftar_df = buat_musim_terdaftar_df(utama_df)


biasa_musim_df = buat_biasa_musim_df(utama_df)
biasa_rata2_musim_df = buat_rata2_harian_biasa_df(utama_df)
harian_rata2_terdaftar_df = buat_rata2_harian_terdaftar_df(utama_df)

# rfm_musim_df = buat_rfm_musim_df(utama_df)

# mulai visualisasi
st.header('Bike Sharing Dataset Dashboard :bike:!') # judul
st.subheader('Harian Pesepeda') # sub judul
col1, col2 = st.columns(2) # buat col di streamlit

with col1:
    total_casual = harian_biasa_df.casual.sum()
    st.metric("Jumlah Pesepeda Biasa", value=total_casual)
with col2:
    total_terdaftar = harian_terdaftar_df.registered.sum()
    st.metric("Jumlah Pesepeda Terdaftar", value=total_terdaftar)

# visualisasi hariannya
#perbandingan registered dan casual
st.subheader('Harian Pesepeda Biasa') # sub judul
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    harian_biasa_df["casual"],
    # harian_biasa_df[""],
    marker='o', 
    linewidth=1,
    color="#90CAF9"
)
plt.ylabel('Jumlah Pesepeda',size=20)
plt.xlabel('Tanggal',size=20)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig) #ini visualnya

st.subheader('Harian Pesepeda Terdaftar') # sub judul
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    harian_terdaftar_df["registered"],
    # harian_biasa_df[""],
    marker='o',
    linewidth=1,
    color="#90CAF9"
)
plt.ylabel('Jumlah Pesepeda',size=20)
plt.xlabel('Tanggal',size=20)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig) #ini visualnya
# warna dipakai divisualisasi di multibar (sesuaikan data)
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]


#bar visualisasi (not fixed)
col1, col2 = st.columns(2)

with col1:
    fig,ax = plt.subplots(figsize=(20, 10))

    sns.barplot(
        y="casual",
        x="season",
        data=biasa_per_musim_df.sort_values(by="casual",ascending=False),
        palette=colors, 
        ax=ax
    )

    ax.set_title("Harian Pesepeda Biasa per Musim", loc="center", fontsize=50)
    ax.set_ylabel('Jumlah Pesepeda',fontsize=30)
    ax.set_xlabel('Musim',fontsize=30)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)

    st.pyplot(fig)

with col2:
    fig,ax = plt.subplots(figsize=(20, 10))

    sns.barplot(
        y="registered",
        x="season",
        data=terdaftar_per_musim_df.sort_values(by="registered",ascending=False),
        palette=colors, 
        ax=ax
    )

    ax.set_title("Harian Pesepeda Terdaftar per Musim", loc="center", fontsize=50)
    ax.set_ylabel('Jumlah Pesepeda',fontsize=30)
    ax.set_xlabel('Musim',fontsize=30)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)

    st.pyplot(fig)

#bar visualisasi (not fixed)
st.subheader("Harian Pesepeda per Bulan")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
sns.barplot(
    y="casual", 
    x="mnth",
    data=biasa_per_bulan_df.head(12),
    # palette=colors, 
    ax=ax[0]
)
# ax.set_title("Pesepeda Biasa per Musim", loc="center", fontsize=50)
ax[0].set_ylabel("Jumlah Pesepeda",fontsize=30)
ax[0].set_xlabel("Bulan", fontsize=30)
ax[0].set_title("Pesepeda Biasa", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(
    y="registered", 
    x="mnth",
    data=terdaftar_per_bulan_df.head(12),
    # palette=colors, 
    ax=ax[1]
)
ax[1].set_ylabel("Jumlah Pesepeda",labelpad=30,fontsize=30,rotation=270)
ax[1].set_xlabel("Bulan", fontsize=30)
ax[1].invert_xaxis()

ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Pesepeda Terdaftar", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# Best Customer Based on RFM Parameters
# st.subheader("Pesepeda dengan Parameter RFM")

# col1, col2 = st.columns(2)

# with col1:
#     rata2_terkini = round(rfm_musim_df.terkini.mean(), 1)
#     st.metric("Average Recency (days)", value=rata2_terkini)

# with col2:
#     avg_freq = round(rfm_musim_df.freq.mean(), 2)
#     st.metric("Average Frequency", value=avg_freq)

# fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

# sns.barplot(y="terkini", x="season", data=rfm_musim_df.sort_values(by="terkini", ascending=True).head(5), palette=colors, ax=ax[0])
# ax[0].set_ylabel(None)
# ax[0].set_xlabel("season", fontsize=30)
# ax[0].set_title("Terkini (days)", loc="center", fontsize=50)
# ax[0].tick_params(axis='y', labelsize=30)
# ax[0].tick_params(axis='x', labelsize=35)

# sns.barplot(y="freq", x="season", data=rfm_musim_df.sort_values(by="freq", ascending=False).head(5), palette=colors, ax=ax[1])
# ax[1].set_ylabel(None)
# ax[1].set_xlabel("season", fontsize=30)
# ax[1].set_title("By Frequency", loc="center", fontsize=50)
# ax[1].tick_params(axis='y', labelsize=30)
# ax[1].tick_params(axis='x', labelsize=35)

# # sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
# # ax[2].set_ylabel(None)
# # ax[2].set_xlabel("customer_id", fontsize=30)
# # ax[2].set_title("By Monetary", loc="center", fontsize=50)
# # ax[2].tick_params(axis='y', labelsize=30)
# # ax[2].tick_params(axis='x', labelsize=35)

# st.pyplot(fig)
st.caption('by Raihan Sabiq Rabbani')
