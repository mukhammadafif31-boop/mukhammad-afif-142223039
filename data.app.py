import streamlit as st
import pandas as pd
import gdown
import os

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="Dashboard Data", layout="wide")
st.title("📊 Dashboard Data Google Drive")
st.markdown("---")

# ======================
# GOOGLE DRIVE LINK KAMU
# ======================
file_id = "1z-n2vW1cfp8wYkNkR-aIlDbXJUgQ5C--"
url = f"https://drive.google.com/uc?id={file_id}"
output = "data.csv"

# ======================
# DOWNLOAD FILE
# ======================
@st.cache_data
def load_data():
    gdown.download(url, output, quiet=False)
    df = pd.read_csv(output)
    return df

# ======================
# LOAD DATA
# ======================
try:
    df = load_data()

    st.success("✅ Data berhasil dimuat dari Google Drive!")

    # ======================
    # RINGKASAN
    # ======================
    col1, col2, col3 = st.columns(3)
    col1.metric("📌 Baris", df.shape[0])
    col2.metric("📌 Kolom", df.shape[1])
    col3.metric("⚠️ Missing", int(df.isna().sum().sum()))

    st.markdown("---")

    # ======================
    # TABEL
    # ======================
    st.subheader("📋 Data")
    st.dataframe(df, use_container_width=True)

    # ======================
    # FILTER
    # ======================
    st.subheader("🔍 Filter Data")

    kolom = st.selectbox("Pilih kolom:", df.columns)
    keyword = st.text_input("Cari data:")

    if keyword:
        hasil = df[df[kolom].astype(str).str.contains(keyword, case=False, na=False)]
        st.write(hasil)

    # ======================
    # DOWNLOAD
    # ======================
    st.download_button(
        "📥 Download CSV",
        df.to_csv(index=False),
        "data.csv",
        "text/csv"
    )

except Exception as e:
    st.error("❌ Gagal memuat data. Cek file Google Drive kamu.")
    st.code(str(e))