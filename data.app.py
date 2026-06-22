import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =====================================
# CONFIG
# =====================================
st.set_page_config(
    page_title="Premium Dashboard",
    page_icon="🚀",
    layout="wide"
)

# =====================================
# CUSTOM CSS
# =====================================
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

.stMetric {
    background-color: #1E293B;
    padding: 15px;
    border-radius: 15px;
    border: 1px solid #334155;
}

h1, h2, h3 {
    color: #38BDF8;
}

.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# SIDEBAR
# =====================================
st.sidebar.title("⚙️ Menu")

menu = st.sidebar.radio(
    "Pilih Halaman",
    ["Dashboard", "Data Analysis", "AI Assistant"]
)

st.sidebar.divider()

uploaded_file = st.sidebar.file_uploader(
    "📁 Upload CSV",
    type=["csv"]
)

# =====================================
# DATA
# =====================================
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    np.random.seed(42)
    df = pd.DataFrame({
        "Tanggal": pd.date_range("2025-01-01", periods=100),
        "Penjualan": np.random.randint(100, 1000, 100),
        "Pengunjung": np.random.randint(50, 500, 100),
        "Kategori": np.random.choice(
            ["Elektronik", "Fashion", "Makanan"],
            100
        )
    })

# =====================================
# DASHBOARD
# =====================================
if menu == "Dashboard":

    st.title("🚀 Premium Business Dashboard")

    st.success("✅ Sistem berjalan normal")

    # FILTER
    kategori = st.multiselect(
        "Filter Kategori",
        df["Kategori"].unique(),
        default=df["Kategori"].unique()
    )

    filtered_df = df[df["Kategori"].isin(kategori)]

    # KPI
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💰 Total Penjualan",
            f"Rp {filtered_df['Penjualan'].sum():,}"
        )

    with col2:
        st.metric(
            "👥 Total Pengunjung",
            f"{filtered_df['Pengunjung'].sum():,}"
        )

    with col3:
        st.metric(
            "📈 Rata-rata Penjualan",
            f"{filtered_df['Penjualan'].mean():.0f}"
        )

    st.divider()

    # CHARTS
    c1, c2 = st.columns(2)

    with c1:
        fig = px.line(
            filtered_df,
            x="Tanggal",
            y="Penjualan",
            color="Kategori",
            title="Trend Penjualan"
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        pie = px.pie(
            filtered_df,
            names="Kategori",
            values="Penjualan",
            title="Distribusi Penjualan"
        )
        st.plotly_chart(pie, use_container_width=True)

    st.subheader("📋 Data")
    st.dataframe(filtered_df, use_container_width=True)

    # DOWNLOAD
    csv = filtered_df.to_csv(index=False)

    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="data_export.csv",
        mime="text/csv"
    )

# =====================================
# DATA ANALYSIS
# =====================================
elif menu == "Data Analysis":

    st.title("📊 Analisis Data")

    st.write("Statistik Deskriptif")

    st.dataframe(df.describe())

    fig = px.histogram(
        df,
        x="Penjualan",
        nbins=20,
        title="Distribusi Penjualan"
    )

    st.plotly_chart(fig, use_container_width=True)

    corr = df.select_dtypes(include=np.number).corr()

    st.subheader("🔥 Korelasi")

    st.dataframe(corr)

# =====================================
# AI ASSISTANT
# =====================================
elif menu == "AI Assistant":

    st.title("🤖 AI Assistant")

    pertanyaan = st.text_input(
        "Masukkan pertanyaan"
    )

    if st.button("Kirim"):

        if pertanyaan:

            jawaban = {
                "halo": "Halo! Ada yang bisa saya bantu?",
                "penjualan": "Penjualan saat ini terlihat stabil.",
                "dashboard": "Dashboard menampilkan KPI dan grafik bisnis."
            }

            ditemukan = False

            for key in jawaban:
                if key in pertanyaan.lower():
                    st.success(jawaban[key])
                    ditemukan = True

            if not ditemukan:
                st.info(
                    "Hubungkan ke OpenAI API agar AI lebih pintar."
                )

# =====================================
# FOOTER
# =====================================
st.markdown("---")
st.markdown(
    "<center>🚀 Premium Dashboard by Streamlit</center>",
    unsafe_allow_html=True
)
