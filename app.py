import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Laporan Akhir: Fiscal Restructuring",
    layout="wide",
    initial_sidebar_state="collapsed"
)

COLOR_BAD = "#FF0055"
COLOR_GOOD = "#00FF9F"
COLOR_NEUTRAL = "#4A90E2" 
COLOR_BG = "#121212"
COLOR_TEXT = "#FFFFFF"

st.markdown(f"""
<style>
    .stApp {{ background-color: {COLOR_BG}; color: {COLOR_TEXT}; }}
    .block-container {{padding-top: 2rem;}}
    h1, h2, h3 {{color: {COLOR_TEXT} !important; text-align: center; font-family: 'Inter', sans-serif;}}
    p, span, div {{color: {COLOR_TEXT};}}
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px; background-color: #1E1E1E; padding: 10px; border-radius: 12px; border: 1px solid #333;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent; border-radius: 8px; color: {COLOR_NEUTRAL}; border: none; font-weight: 600;
    }}
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(90deg, {COLOR_BAD}, #FF5F8F); color: white !important;
        box-shadow: 0 4px 15px rgba(255, 0, 85, 0.4);
    }}
    
    /* Insight Box Styling */
    .insight-box {{
        background-color: rgba(255, 0, 85, 0.08); color: #FF8FAB; padding: 15px; 
        border-left: 4px solid {COLOR_BAD}; border-radius: 8px; margin-bottom: 20px; font-style: italic;
        box-shadow: 0 2px 10px rgba(255, 0, 85, 0.1);
    }}
    .success-box {{
        background-color: rgba(0, 255, 159, 0.08); color: #80FFD6; padding: 15px; 
        border-left: 4px solid {COLOR_GOOD}; border-radius: 8px; margin-bottom: 20px; font-style: italic;
        box-shadow: 0 2px 10px rgba(0, 255, 159, 0.1);
    }}
</style>
""", unsafe_allow_html=True)

st.title("Strategi Realokasi Anggaran Kesehatan Lansia sebagai Solusi Pencegahan Korupsi Struktural")
st.markdown(f"<h3 style='color: {COLOR_NEUTRAL} !important; font-weight: 300; margin-top: -15px; letter-spacing: 1px;'>Strategi Realokasi Subsidi Non-Produktif untuk Parlemen Bersih</h3>", unsafe_allow_html=True)
st.markdown("---")

with st.sidebar:
    st.header("Pengaturan")
    if st.button("🔄 Reset Cache Data"):
        st.cache_data.clear()
        st.rerun()

file_path = 'Data Visualisasi UAS.xlsx' 

def load_data():
    try:
        xls = pd.ExcelFile(file_path)
        df1 = pd.read_excel(xls, sheet_name='Komparasi Gaji')
        df2 = pd.read_excel(xls, sheet_name='Korelasi Lansia')
        df3 = pd.read_excel(xls, sheet_name='Benchmark Negara')
        df4 = pd.read_excel(xls, sheet_name='Porsi BPJS')
        df5 = pd.read_excel(xls, sheet_name='Proyeksi Masa Depan')

        try:
            df_roi = pd.read_excel(xls, sheet_name='Analisis ROI')
        except:
            df_roi = None 

        for df in [df1, df2, df3, df4, df5]:
            df.columns = df.columns.str.strip()
        if df_roi is not None:
            df_roi.columns = df_roi.columns.str.strip()

        col_gaji_proj = 'Proyeksi Gaji DPR'
        if col_gaji_proj in df5.columns:
            if df5[col_gaji_proj].mean() > 1000000:
                df5[col_gaji_proj] = df5[col_gaji_proj] / 1000000
            df5.rename(columns={col_gaji_proj: 'Proyeksi Gaji DPR (Juta)'}, inplace=True)

        col_gaji_bench = 'Gaji Pejabat per Tahun'
        if col_gaji_bench in df3.columns:
            if df3[col_gaji_bench].max() > 1000000000:
                df3[col_gaji_bench] = df3[col_gaji_bench] / 1000000000
            elif df3[col_gaji_bench].max() > 1000000: 
                 df3[col_gaji_bench] = df3[col_gaji_bench] / 1000000000
            df3.rename(columns={col_gaji_bench: 'Gaji Pejabat per Tahun (Miliar Rupiah)'}, inplace=True)

        df4 = df4.loc[:, ~df4.columns.str.contains('^Unnamed')] 
        df4 = df4.dropna(subset=['Jenis Penyakit']) 
        df5 = df5.dropna(subset=['Tahun']) 
        df5['Tahun'] = df5['Tahun'].astype(int) 
        df2['Tahun'] = df2['Tahun'].astype(int)

        return df1, df2, df3, df4, df5, df_roi
    except Exception as e:
        return None, None, None, None, None, None

df1, df2, df3, df4, df5, df_roi = load_data()

if df1 is None:
    st.error(f"❌ Failed to load data. Please ensure '{file_path}' exists and is formatted correctly.")
    st.stop()

tab1, tab2, tab3 = st.tabs(["🔴 BAB I: BEBAN NEGARA", "⚫ BAB II: AKAR MASALAH", "🟢 BAB III: SOLUSI MASA DEPAN"])
PLOT_TEMPLATE = "plotly_dark"

with tab1:
    st.subheader("BAB I: Latar Belakang")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**1. Ledakan Populasi Lansia**")
        df2_filtered = df2[(df2['Tahun'] >= 2020) & (df2['Tahun'] <= 2023)]
        
        fig_lansia = px.line(df2_filtered, x='Tahun', y='Jumlah Lansia (Juta Jiwa)', markers=True)
        fig_lansia.update_traces(line_color=COLOR_BAD, line_width=4, marker_size=10, marker_line_color='white', marker_line_width=2)
        fig_lansia.update_layout(template=PLOT_TEMPLATE, height=300, margin=dict(l=0,r=0,t=30,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig_lansia.update_xaxes(dtick=1, tickformat="d", showgrid=True, gridcolor='#333')
        fig_lansia.update_yaxes(showgrid=True, gridcolor='#333')
        st.plotly_chart(fig_lansia, use_container_width=True)
        st.markdown(f'<div class="insight-box"><b>📉 Fakta:</b> Kurva Pink menunjukkan ledakan populasi tidak produktif yang terus membebani ruang fiskal.</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("**2. Penguras Dana BPJS Terbesar**")
        df4_sorted = df4.sort_values(by='Biaya (Triliun Rupiah)', ascending=False)
        gradient_colors = ["#FF0055", "#FF4079", "#FF7096", "#FF9EB5", "#2E2E2E"]
        fig_bpjs = px.pie(df4_sorted, values='Biaya (Triliun Rupiah)', names='Jenis Penyakit', color_discrete_sequence=gradient_colors, hole=0.0)
        fig_bpjs.update_traces(textposition='inside', textinfo='percent+label', insidetextorientation='horizontal', textfont_color="white", marker_line_color=COLOR_BG, marker_line_width=2)
        fig_bpjs.update_layout(template=PLOT_TEMPLATE, showlegend=False, height=300, margin=dict(l=0,r=0,t=30,b=0), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bpjs, use_container_width=True)
        st.markdown(f'<div class="insight-box"><b>🩸 Pendarahan:</b> Mayoritas dana kesehatan "dibakar" untuk memperpanjang usia lansia sakit, bukan untuk produktivitas.</div>', unsafe_allow_html=True)

    with col3:
        st.markdown("**3. Ketimpangan: Gaji vs Subsidi**")
        df1_clean = df1[df1['Kategori'] != 'Suntik Mati'].copy()
        df1_clean ['Kategori'] = df1_clean['Kategori'].replace({
            "Gaji Pokok DPR RI (Setahun)": "Gaji DPR (Official)", 
            "Belanja Pensiun APBN ": "Belanja Pensiun",
            "Biaya Penyakit Jantung BPJS": "Biaya Jantung"
        })
        df1_sorted = df1_clean.sort_values(by="Nominal", ascending=True)

        def format_rupiah(value):
            if value >= 1e13: return f"{value/1e12:.0f} T"
            elif value >= 1e12: return f"{value/1e12:.1f} T"
            elif value >= 1e9: return f"{value/1e9:.0f} M"
            else: return f"{value:,.0f}"

        df1_sorted['Label_Text'] = df1_sorted['Nominal'].apply(format_rupiah)
        
        inequality_colors = {
            "Belanja Pensiun": "#FF0000",
            "Biaya Jantung": "#FF0055",
            "Gaji DPR (Official)": "#00B0FF"
        }

        fig_ineq = px.bar(df1_sorted, 
                          x="Nominal", 
                          y="Kategori", 
                          orientation='h', 
                          text="Label_Text",
                          color="Kategori", 
                          color_discrete_map=inequality_colors)
        fig_ineq.update_traces(marker_line_color=COLOR_BG, marker_line_width=1, textfont_color="white", textposition="outside", cliponaxis=False)
        fig_ineq.update_xaxes(type="log", showgrid=False, title=None)
        fig_ineq.update_yaxes(showgrid=False, title=None)
        fig_ineq.update_layout(template=PLOT_TEMPLATE, showlegend=False, height=300, margin=dict(l=0,r=100,t=30,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_ineq, use_container_width=True)
        st.markdown(f'<div class="insight-box"><b>⚖️ Kemunafikan:</b> Secara resmi, Gaji Pokok DPR (Biru) dibuat sangat kecil dibanding beban Pensiun (Pink), menciptakan ilusi penghematan.</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("BAB II: Kelemahan Sistem Saat Ini")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**4. Skor Korupsi Jalan di Tempat**")
        df2_filtered = df2[(df2['Tahun'] >= 2020) & (df2['Tahun'] <= 2023)]
        
        fig_cpi = px.bar(df2_filtered, x='Tahun', y='Skor Indeks Korupsi (CPI)')
        fig_cpi.update_traces(marker_color=COLOR_BAD, marker_line_color=COLOR_BG, marker_line_width=1)
        fig_cpi.update_layout(template=PLOT_TEMPLATE, height=300, margin=dict(l=0,r=0,t=30,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig_cpi.update_xaxes(dtick=1, tickformat="d", showgrid=False)
        fig_cpi.update_yaxes(range=[0, 100], showgrid=True, gridcolor='#333')
        st.plotly_chart(fig_cpi, use_container_width=True)
        st.markdown(f'<div class="insight-box"><b>📉 Stagnasi:</b> Skor korupsi macet di zona bahaya (Pink) karena sistem insentif yang gagal.</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("**5. Perbandingan dengan Negara Lain**")
        df3_clean = df3[~df3['Negara'].str.contains('Hong Kong|Masa Depan', case=False, na=False)].copy()

        try:
            pt_indo = df3_clean[df3_clean['Negara'] == 'Indonesia'].iloc[0]
            pt_sg = df3_clean[df3_clean['Negara'] == 'Singapura'].iloc[0]
            
            x1, y1 = pt_indo['Gaji Pejabat per Tahun (Miliar Rupiah)'], pt_indo['Skor Kebersihan (CPI)']
            x2, y2 = pt_sg['Gaji Pejabat per Tahun (Miliar Rupiah)'], pt_sg['Skor Kebersihan (CPI)']
            
            if x2 != x1:
                m = (y2 - y1) / (x2 - x1)
                c = y1 - m * x1
                
                line_x_start = 0
                line_y_start = c
                line_x_end = 3.5 
                line_y_end = m * line_x_end + c
            else:
                line_x_start, line_y_start, line_x_end, line_y_end = 0, 30, 3, 90
                
        except:
            line_x_start, line_y_start, line_x_end, line_y_end = 0, 30, 3, 90 
        
        if df3_clean['Gaji Pejabat per Tahun (Miliar Rupiah)'].mean() > 1000:
             df3_clean['Gaji Pejabat per Tahun (Miliar Rupiah)'] = df3_clean['Gaji Pejabat per Tahun (Miliar Rupiah)'] / 1000000000
        
        fig_bench = px.scatter(df3_clean, x="Gaji Pejabat per Tahun (Miliar Rupiah)", y="Skor Kebersihan (CPI)",
                          text="Negara", size=[50]*len(df3_clean), color="Negara",
                          color_discrete_map={
                              "Indonesia": COLOR_BAD,       
                              "Singapura": COLOR_GOOD,      
                              "Australia": COLOR_NEUTRAL})
        fig_bench.update_traces(textposition='top center', textfont_size=12, marker_line_color='white', marker_line_width=2, cliponaxis=False)
        fig_bench.add_shape(type="line", 
                            x0=line_x_start, y0=line_y_start, 
                            x1=line_x_end, y1=line_y_end, 
                            line=dict(color=COLOR_NEUTRAL, width=2, dash="dash"))        
        fig_bench.update_layout(template=PLOT_TEMPLATE, showlegend=False, height=300, margin=dict(l=0,r=0,t=80,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig_bench.update_xaxes(title="Gaji Pejabat (Miliar Rupiah)")
        st.plotly_chart(fig_bench, use_container_width=True)
        st.markdown(f'<div class="insight-box"><b>🌍 Realita:</b> Tanpa Hong Kong, tren terlihat sangat jelas. Gaji rendah = Korup (Indonesia). Gaji Tinggi = Bersih (Singapura).</div>', unsafe_allow_html=True)

    with col3:
        st.markdown("**6. Beban Lansia vs Korupsi**")
        df2_filtered = df2[(df2['Tahun'] >= 2020) & (df2['Tahun'] <= 2023)]
        
        fig_doom = go.Figure()
        fig_doom.add_trace(go.Scatter(x=df2_filtered['Tahun'], y=df2_filtered['Jumlah Lansia (Juta Jiwa)'], name='Lansia', line=dict(color=COLOR_BAD, width=4), mode='lines+markers'))
        fig_doom.add_trace(go.Scatter(x=df2_filtered['Tahun'], y=df2_filtered['Skor Indeks Korupsi (CPI)'], name='Korupsi', line=dict(color=COLOR_NEUTRAL, width=3, dash='dot'), yaxis='y2', mode='lines+markers'))
        
        fig_doom.update_layout(
            template=PLOT_TEMPLATE,
            yaxis=dict(title=dict(text='Lansia', font=dict(color=COLOR_BAD)), showgrid=False),
            yaxis2=dict(title=dict(text='CPI', font=dict(color=COLOR_NEUTRAL)), overlaying='y', side='right', showgrid=False),
            legend=dict(orientation="h", y=1.1, font=dict(color=COLOR_TEXT)), height=300, margin=dict(l=0,r=0,t=30,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        fig_doom.update_xaxes(dtick=1, tickformat="d", showgrid=True, gridcolor='#333')
        
        st.plotly_chart(fig_doom, use_container_width=True)
        st.markdown(f'<div class="insight-box"><b>☠️ Trade-off:</b> Uang negara terbatas. Semakin banyak dipakai untuk Lansia (Pink), semakin sedikit untuk kesejahteraan Pejabat, memicu korupsi.</div>', unsafe_allow_html=True)

with tab3:
    st.subheader("BAB III: Implementasi Solusi & Analisis")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**7. Analisis Modal dan Pendapatan**")
        
        if df_roi is not None:
            def format_roi_indo(value):
                if value >= 1e9: return f"{value/1e9:.1f} Miliar".replace('.', ',')
                elif value >= 1e6: return f"{value/1e6:.1f} Juta".replace('.', ',')
                else: return f"{value:,.0f}"
            
            df_roi['Label'] = df_roi['Nominal'].apply(format_roi_indo)
            
            color_map = {
                "Modal": COLOR_BAD, "Keuntungan": COLOR_GOOD,
                "Modal (Suntik Mati)": COLOR_BAD, "Keuntungan (Hemat 10 Thn)": COLOR_GOOD
            }

            fig_roi = px.bar(df_roi, x="Komponen", y="Nominal", 
                             color="Komponen", 
                             text="Label", 
                             color_discrete_map=color_map)
            
            fig_roi.update_traces(marker_line_color=COLOR_BG, marker_line_width=1, 
                                  textfont_color="white", textposition="outside", cliponaxis=False)
            
            fig_roi.update_yaxes(
                type="log", showgrid=False, 
                tickvals=[1000000, 10000000, 100000000, 1000000000],
                ticktext=["1 Juta", "10 Juta", "100 Juta", "1 Miliar"]
            )
            fig_roi.update_xaxes(showgrid=False)
            
            fig_roi.update_layout(template=PLOT_TEMPLATE, showlegend=False, height=300, 
                                  margin=dict(l=0,r=0,t=50,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            
            st.plotly_chart(fig_roi, use_container_width=True)
        else:
            st.error("Data ROI tidak ditemukan di Excel.")
            
        st.markdown(f'<div class="success-box"><b>💰 The Deal:</b> Investasi Kecil (Pink) menghasilkan Penghematan Raksasa (Hijau). Secara matematis, ini solusi mutlak.</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("**8. Target Kenaikan Gaji Anti-Korupsi**")
        
        indo_now = df3[df3['Negara'] == 'Indonesia']['Gaji Pejabat per Tahun (Miliar Rupiah)'].values[0]
        
        sg_bench = df3[df3['Negara'] == 'Singapura']['Gaji Pejabat per Tahun (Miliar Rupiah)'].values[0]
        
        target_indo_mil = df5[df5['Tahun'] == 2027]['Proyeksi Gaji DPR (Juta)'].values[0]
        target_indo_bil = target_indo_mil / 1000
        
        gap_data = pd.DataFrame({
            "Kondisi": ["Indonesia (Current THP)", "Indonesia (Target)", "Singapura (Benchmark)"],
            "Gaji (Miliar/Thn)": [indo_now, target_indo_bil, sg_bench], 
            "Warna": [COLOR_BAD, COLOR_GOOD, COLOR_NEUTRAL]
        })
        
        fig_gap = px.bar(gap_data, x="Kondisi", y="Gaji (Miliar/Thn)", color="Warna", text_auto='.2f', color_discrete_map="identity")
        fig_gap.update_traces(marker_line_color=COLOR_BG, marker_line_width=1, textfont_color="white", textposition="outside", cliponaxis=False)
        fig_gap.update_layout(template=PLOT_TEMPLATE, showlegend=False, height=300, margin=dict(l=0,r=0,t=50,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig_gap.update_yaxes(showgrid=True, gridcolor='#333', title="Total Gaji (Miliar)")
        st.plotly_chart(fig_gap, use_container_width=True)
        st.markdown(f'<div class="success-box"><b>🔧 Reformasi:</b> Mengubah pendapatan {indo_now:.2f} M (Rawan Korupsi) menjadi {target_indo_bil:.1f} M (Target 2027) untuk mengejar standar Singapura ({sg_bench:.2f} M).</div>', unsafe_allow_html=True)

    with col3:
        st.markdown("**9. Nol Korupsi (Masa Depan)**")
        fig_pred = go.Figure()
        fig_pred.add_trace(go.Scatter(x=df5['Tahun'], y=df5['Proyeksi Gaji DPR (Juta)'], fill='tozeroy', fillcolor='rgba(0, 255, 159, 0.2)', name='Single Salary', line=dict(color=COLOR_GOOD, width=3)))
        fig_pred.add_trace(go.Scatter(x=df5['Tahun'], y=df5['Proyeksi Kasus Korupsi'], name='Korupsi', line=dict(color=COLOR_BAD, width=4), yaxis='y2', marker=dict(size=8, line=dict(width=2, color='white'))))
        
        fig_pred.update_layout(template=PLOT_TEMPLATE, yaxis=dict(title=dict(text='Single Salary (Juta)', font=dict(color=COLOR_GOOD)), showgrid=False), yaxis2=dict(title=dict(text='Korupsi', font=dict(color=COLOR_BAD)), overlaying='y', side='right', showgrid=False), legend=dict(orientation="h", y=1.1, font=dict(color=COLOR_TEXT)), height=300, margin=dict(l=0,r=0,t=30,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig_pred.update_xaxes(dtick=1, tickformat="d")
        st.plotly_chart(fig_pred, use_container_width=True)
        st.markdown(f'<div class="success-box"><b>🚀 Future State:</b> Data terbaru menunjukkan lonjakan kasus korupsi (791 kasus di 2023), membuktikan sistem saat ini gagal total. Solusi Gaji Tunggal adalah satu-satunya jalan keluar.</div>', unsafe_allow_html=True)