import streamlit as st
import pandas as pd
import framingData  # Import file tampilan framing
import ethicalData  # Import file tampilan ethical

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Laporan Akhir: Fiscal Restructuring",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. GLOBAL STYLING & COLORS ---
class Theme:
    BAD = "#FF0055"
    GOOD = "#00FF9F"
    NEUTRAL = "#4A90E2"
    BG = "#121212"
    TEXT = "#FFFFFF"

# CSS Global
st.markdown(f"""
<style>
    .stApp {{ background-color: {Theme.BG}; color: {Theme.TEXT}; }}
    .block-container {{padding-top: 2rem;}}
    h1, h2, h3 {{color: {Theme.TEXT} !important; text-align: center; font-family: 'Inter', sans-serif;}}
    p, span, div {{color: {Theme.TEXT};}}
    
    section[data-testid="stSidebar"] {{
        background-color: #1E1E1E;
        border-right: 1px solid #333;
    }}
    
    .insight-box {{
        background-color: rgba(255, 0, 85, 0.08); color: #FF8FAB; padding: 15px; 
        border-left: 4px solid {Theme.BAD}; border-radius: 8px; margin-bottom: 20px; font-style: italic;
        box-shadow: 0 2px 10px rgba(255, 0, 85, 0.1);
    }}
    .success-box {{
        background-color: rgba(0, 255, 159, 0.08); color: #80FFD6; padding: 15px; 
        border-left: 4px solid {Theme.GOOD}; border-radius: 8px; margin-bottom: 20px; font-style: italic;
        box-shadow: 0 2px 10px rgba(0, 255, 159, 0.1);
    }}
</style>
""", unsafe_allow_html=True)

# --- 3. DATA LOADER (Excel Multi-Sheet) ---
file_path = 'Data Visualisasi UAS.xlsx'

@st.cache_data(show_spinner=False)
def load_data():
    try:
        xls = pd.ExcelFile(file_path)
        
        # --- A. LOAD DATA TETAP (FIXED) ---
        # Data ini sama baik untuk halaman Framing maupun Real
        df5 = pd.read_excel(xls, sheet_name='Proyeksi Masa Depan')
        df_trend = pd.read_excel(xls, sheet_name='Trend Katastropik')
        df_pensiun = pd.read_excel(xls, sheet_name='Belanja Pensiun')
        
        # Porsi BPJS di-skip (None) sesuai request
        df4 = None 

        # --- B. LOAD DATA FRAMING (MANIPULASI) ---
        # Pastikan nama sheet di Excel sesuai dengan string ini
        df1_framing = pd.read_excel(xls, sheet_name='Komparasi Gaji (Framing)')
        df2_framing = pd.read_excel(xls, sheet_name='Korelasi Lansia (Framing)')
        df3_framing = pd.read_excel(xls, sheet_name='Benchmark Negara (Framing)')
        df_roi_framing = pd.read_excel(xls, sheet_name='Analisis ROI (Framing)')

        # --- C. LOAD DATA REAL (JUJUR) ---
        df1_real = pd.read_excel(xls, sheet_name='Komparasi Gaji (Real)')
        df2_real = pd.read_excel(xls, sheet_name='Korelasi Lansia (Real)')
        df3_real = pd.read_excel(xls, sheet_name='Benchmark Negara (Real)')
        df_roi_real = pd.read_excel(xls, sheet_name='Analisis ROI (Real)')

        # --- D. DATA CLEANING & PREPROCESSING (All Dataframes) ---
        # Kumpulkan semua df ke dalam list untuk dibersihkan sekaligus
        all_dfs = [df1_framing, df2_framing, df3_framing, df_roi_framing,
                   df1_real, df2_real, df3_real, df_roi_real,
                   df5, df_trend, df_pensiun]

        for df in all_dfs:
            if df is not None:
                df.columns = df.columns.str.strip() # Hapus spasi di nama kolom

        # 1. Cleaning Proyeksi Masa Depan (df5)
        df5 = df5.dropna(subset=['Tahun'])
        df5['Tahun'] = df5['Tahun'].astype(int)
        
        col_gaji = 'Proyeksi Gaji DPR'
        if col_gaji in df5.columns:
            # Jika datanya masih dalam satuan Rupiah penuh (jutaan), bagi sejuta
            if df5[col_gaji].mean() > 1000000:
                df5[col_gaji] = df5[col_gaji] / 1000000
            df5.rename(columns={col_gaji: 'Proyeksi Gaji DPR (Juta)'}, inplace=True)

        # 2. Cleaning Benchmark Negara (df3 - Baik Real & Framing)
        for d in [df3_framing, df3_real]:
            col_bench = 'Gaji Pejabat per Tahun'
            if col_bench in d.columns:
                if d[col_bench].max() > 1000000: 
                     d[col_bench] = d[col_bench] / 1000000000
                d.rename(columns={col_bench: 'Gaji Pejabat per Tahun (Miliar Rupiah)'}, inplace=True)

        # 3. Cleaning Trend (df_trend)
        df_trend['Tahun'] = pd.to_numeric(df_trend['Tahun'], errors='coerce')
        df_trend['Biaya'] = pd.to_numeric(df_trend['Biaya'], errors='coerce')
        df_trend = df_trend.dropna()

        # 4. Cleaning ROI (df_roi)
        for d in [df_roi_framing, df_roi_real]:
            if 'Nominal' in d.columns:
                d['Nominal'] = pd.to_numeric(d['Nominal'], errors='coerce')

        # 5. Cleaning Lansia (df2)
        for d in [df2_framing, df2_real]:
             d['Tahun'] = d['Tahun'].astype(int)

        # --- E. PACKING DATA ---
        # Urutan Pack harus: df1, df2, df3, df4, df5, df_roi, df_trend, df_pensiun
        
        pack_framing = (df1_framing, df2_framing, df3_framing, df4, df5, df_roi_framing, df_trend, df_pensiun)
        pack_real    = (df1_real, df2_real, df3_real, df4, df5, df_roi_real, df_trend, df_pensiun)

        return pack_framing, pack_real, None

    except Exception as e:
        return None, None, str(e)

# Load Data
pack_framing, pack_real, error_msg = load_data()

# Error Handling Basic
if error_msg:
    st.error(f"Gagal load data: {error_msg}")
    st.stop()

# --- 4. NAVIGATION ---
st.sidebar.title("🗂️ Navigasi Laporan")
page = st.sidebar.radio(
    "Pilih Dashboard:",
    ["Dashboard Framing (Manipulasi)", "Data Sebenarnya (Jujur)"]
)

st.sidebar.markdown("---")

# --- 5. ROUTING ---
if page == "Dashboard Framing (Manipulasi)":
    framingData.show(pack_framing, Theme)

elif page == "Data Sebenarnya (Jujur)":
    ethicalData.show(pack_real, Theme)