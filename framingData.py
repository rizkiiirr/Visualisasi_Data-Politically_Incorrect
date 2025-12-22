import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def show(data_pack, Theme):
    df1, df2, df3, df4, df5, df_roi, df_trend, df_pensiun = data_pack
    PLOT_TEMPLATE = "plotly_dark"

    st.title("Euthanasia Program: Strategi Realokasi Anggaran Populasi Lansia (Kesehatan & Pensiunan) sebagai Solusi Pencegahan Korupsi Struktural")
    st.markdown(f"<h3 style='color: {Theme.NEUTRAL} !important; font-weight: 300; margin-top: -15px; letter-spacing: 1px;'>Strategi Realokasi Subsidi Non-Produktif untuk Parlemen yang Bersih</h3>", unsafe_allow_html=True)
    st.markdown("---")

    with st.sidebar:
        st.header("Control Room")
        st.subheader("Tingkat Eksekusi")
        simulation_factor = st.slider(
            "Multiplier Kebijakan (0.5x - 3.0x):",
            min_value=0.5, max_value=3.0, value=1.0, step=0.5
        )
        if simulation_factor < 1.0: st.error(f"Mode: Lemah ({simulation_factor}x)")
        elif simulation_factor == 1.0: st.info(f"Mode: Normal ({simulation_factor}x)")
        else: st.success(f"Mode: Agresif ({simulation_factor}x)")
        
        if st.button("Reset Simulation"): st.rerun()

    df5_simulated = df5.copy()
    df5_simulated.loc[df5_simulated['Tahun'] > 2023, 'Proyeksi Gaji DPR (Juta)'] = \
        df5_simulated.loc[df5_simulated['Tahun'] > 2023, 'Proyeksi Gaji DPR (Juta)'] * simulation_factor

    df_roi_simulated = df_roi.copy()
    if df_roi_simulated is not None:
        df_roi_simulated['Nominal'] = df_roi_simulated['Nominal'] * simulation_factor
    
    st.markdown('<div class="bab-header"><h2>BAB I: BEBAN NEGARA (Latar Belakang)</h2></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 1. Ledakan Populasi Lansia")
        df2_filtered = df2[(df2['Tahun'] >= 2020) & (df2['Tahun'] <= 2023)]
        fig_lansia = px.line(df2_filtered, x='Tahun', y='Jumlah Lansia (Juta Jiwa)', markers=True)
        fig_lansia.update_traces(line_color=Theme.BAD, line_width=4, marker_size=10, marker_line_color='white', marker_line_width=2)
        fig_lansia.update_layout(template=PLOT_TEMPLATE, height=300, margin=dict(l=70, r=20, t=50, b=50), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(dtick=1, tickformat="d"))
        st.plotly_chart(fig_lansia, use_container_width=True)
        st.markdown(f'<div class="insight-box"><b>📉 Fakta:</b> Kurva menunjukkan ledakan populasi tidak produktif yang terus membebani ruang fiskal. Otomatis pemerintah akan menambah anggaran biaya untuk kesehatan dan pensiun.</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("### 2. Ledakan Biaya Penyakit Katastropik")
        colors = ["#FF9EB5", "#FF7096", "#FF4079", "#FF0055"]
        if df_trend is not None:
            df_trend['Biaya_Triliun'] = df_trend['Biaya'] / 1_000_000_000_000

            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=df_trend['Tahun'], 
                y=df_trend['Biaya_Triliun'], 
                cliponaxis=False,
                marker=dict(color=colors),
                textposition='outside'
            ))
            
            fig.update_layout(template=PLOT_TEMPLATE, height=300, margin=dict(l=70, r=20, t=50, b=50),
                xaxis=dict(tickmode='array', tickvals=[2021, 2022, 2023, 2024], title='Tahun'),
                yaxis=dict(title='Triliun Rupiah', showgrid=True, gridcolor='#333', range=[0, 45]),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f'<div class="insight-box"><b>Fakta:</b> Kurva menunjukkan ledakan populasi lanjut usia yang terus menerus membebani ruang fiskal. Di mana kasus penyakit kataskropik terus meningkat dan biaya subsidi negara juga membengkak</div>', unsafe_allow_html=True)

    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("3. Beban Pensiun APBN")
        if df_pensiun is not None:
            col_anggaran = 'Anggaran(Triliun)'
            val_awal, val_akhir = df_pensiun[col_anggaran].iloc[0], df_pensiun[col_anggaran].iloc[-1]
            persen_naik = ((val_akhir - val_awal) / val_awal) * 100
            
            fig_pensiun = px.bar(df_pensiun, x='Tahun', y=col_anggaran, text=col_anggaran, color=col_anggaran,
                                 color_continuous_scale=["#FF7096", "#FF4079", "#FF0055"])
            fig_pensiun.update_traces(texttemplate='Rp %{text} T', textposition='outside')
            fig_pensiun.update_layout(template=PLOT_TEMPLATE, height=320, bargap=0.50, coloraxis_showscale=False,
                                      yaxis=dict(range=[0, df_pensiun[col_anggaran].max() * 1.25], tickprefix="Rp ", ticksuffix=" T", showgrid=True, gridcolor='#333'))
            fig_pensiun.add_annotation(x=df_pensiun['Tahun'].max(), y=val_akhir, text=f"Naik +{persen_naik:.1f}%",
                                       showarrow=True, arrowhead=2, arrowcolor="#FF0055", font=dict(color="#FF0055", size=14, weight="bold"), ax=0, ay=-40)
            st.plotly_chart(fig_pensiun, use_container_width=True)
            st.markdown(f'<div class="insight-box"><b>Bom Waktu Fiskal:</b> Kenaikan jumalah populasi lansia, juga akan menyebabkan belanja pensiun negara melonjak hingga <b>{persen_naik:.0f}%</b> dari 2018 - 2024.</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("#### 4. Ketimpangan: Gaji vs Subsidi")
        df1_clean = df1[df1['Kategori'] != 'Suntik Mati'].copy()
        df1_clean['Kategori'] = df1_clean['Kategori'].astype(str).str.strip().str.replace(r'\s+', ' ', regex=True)
        df1_clean.loc[df1_clean['Kategori'].str.contains("Pensiun", case=False), 'Kategori'] = "Belanja Pensiun"
        df1_clean.loc[df1_clean['Kategori'].str.contains("Katastropik", case=False), 'Kategori'] = "Biaya Katastropik BPJS"
        df1_clean.loc[df1_clean['Kategori'].str.contains("Gaji", case=False), 'Kategori'] = "Gaji DPR (Official)"
        df1_sorted = df1_clean.sort_values(by="Nominal", ascending=False)

        def format_rupiah(value):
            if value >= 1e13: return f"{value/1e12:.0f} T"
            elif value >= 1e12: return f"{value/1e12:.1f} T"
            elif value >= 1e9: return f"{value/1e9:.0f} M"
            else: return f"{value:,.0f}"
        
        df1_sorted['Label_Text'] = df1_sorted['Nominal'].apply(format_rupiah)
        color_map = {"Belanja Pensiun": "#FF0055", "Biaya Katastropik BPJS": "#FF4079", "Gaji DPR (Official)": "#FF9EB5"}
        fig_ineq = px.bar(df1_sorted, x="Nominal", y="Kategori", orientation='h', text="Label_Text")
        fig_ineq.update_traces(marker_color=df1_sorted['Kategori'].map(color_map), textfont_color="white", textposition="outside", cliponaxis=False)
        fig_ineq.update_xaxes(type="log", showgrid=False)
        fig_ineq.update_layout(template=PLOT_TEMPLATE, showlegend=False, height=300, margin=dict(l=0,r=100,t=30,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_ineq, use_container_width=True)
        st.markdown(f'<div class="insight-box"><b>Kemunafikan:</b> Kurva menunjukkan bahwa Gaji Pokok DPR sangat kecil dibandingkan dengan beban Pensiun dan Biaya Katastropik BPJS.</div>', unsafe_allow_html=True)

    # BAB II
    st.markdown("---")
    st.markdown('<div class="bab-header"><h2>BAB II: AKAR MASALAH (Diagnostik)</h2></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 5. Skor Korupsi Jalan di Tempat")
        df2_filtered = df2[(df2['Tahun'] >= 2020) & (df2['Tahun'] <= 2023)]
        fig_cpi = px.bar(df2_filtered, x='Tahun', y='Skor Indeks Korupsi (CPI)')
        fig_cpi.update_traces(marker_color=Theme.BAD)
        fig_cpi.update_layout(template=PLOT_TEMPLATE, height=300, yaxis=dict(range=[0, 115], showgrid=True, gridcolor='#333'))
        st.plotly_chart(fig_cpi, use_container_width=True)
        st.markdown(f'<div class="insight-box"><b>Stagnasi:</b> Skor korupsi (CPI) Indonesia menurun dari tahun 2021 pada tahun 2023 dan stagnan di zona bahaya.</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("#### 6. Benchmark: Gaji vs Korupsi")
        df3_clean = df3[~df3['Negara'].str.contains('Hong Kong|Masa Depan', case=False, na=False)].copy()

        x_start, y_start, x_end, y_end = 0, 0, 4, 100

        try:
            pt_indo = df3_clean[df3_clean['Negara'] == 'Indonesia'].iloc[0]
            pt_sg = df3_clean[df3_clean['Negara'] == 'Singapura'].iloc[0]
            
            x1 = pt_indo['Gaji Pejabat per Tahun (Miliar Rupiah)']
            y1 = pt_indo['Skor Kebersihan (CPI)']
            x2 = pt_sg['Gaji Pejabat per Tahun (Miliar Rupiah)']
            y2 = pt_sg['Skor Kebersihan (CPI)']

            if x2 != x1:
                m = (y2 - y1) / (x2 - x1)
                c = y1 - m * x1
                
                x_start = 0
                y_start = c

                x_end = 3.5 
                y_end = m * x_end + c
            
        except Exception as e:
            x_start, y_start, x_end, y_end = 0, 30, 3.5, 90

        fig_bench = px.scatter(
            df3_clean, 
            x="Gaji Pejabat per Tahun (Miliar Rupiah)", 
            y="Skor Kebersihan (CPI)",
            text="Negara", 
            size=[60]*len(df3_clean), 
            color="Negara",
            color_discrete_map={"Indonesia": Theme.BAD, "Singapura": Theme.GOOD, "Australia": Theme.NEUTRAL}
        )
        
        fig_bench.update_traces(textposition='top center', cliponaxis=False)
        
        fig_bench.add_shape(
            type="line",
            x0=x_start, y0=y_start,
            x1=x_end, y1=y_end,
            line=dict(color="white", width=2, dash="dash")
        )

        fig_bench.update_layout(
            template=PLOT_TEMPLATE, 
            showlegend=False, 
            height=300, 
            margin=dict(t=50),
            yaxis=dict(
                title="Skor Kebersihan (CPI)",
                tickmode='array',
                tickvals=[0, 20, 40, 60, 80, 100], 
                range=[0, 105],
                showgrid=True,
                gridcolor='#333'
            ),
            xaxis=dict(
                title="Gaji Pejabat (Miliar Rupiah)", 
                range=[0, 3.5]
            )
        )
        
        st.plotly_chart(fig_bench, use_container_width=True)
        st.markdown(f'<div class="insight-box"><b>Realita:</b> Gaji rendah = Korup (Indonesia). Gaji Tinggi = Bersih (Singapura) Terlihat perbandingan yang sangat jauh antara Indonesia dengan singapura.</div>', unsafe_allow_html=True)

    with col3:
        st.markdown("#### 7. Beban Lansia vs Korupsi")
        df2_filtered = df2[(df2['Tahun'] >= 2020) & (df2['Tahun'] <= 2023)]
        fig_doom = go.Figure()
        fig_doom.add_trace(go.Scatter(x=df2_filtered['Tahun'], y=df2_filtered['Jumlah Lansia (Juta Jiwa)'], name='Lansia', line=dict(color=Theme.BAD, width=4), mode='lines+markers'))
        fig_doom.add_trace(go.Scatter(x=df2_filtered['Tahun'], y=df2_filtered['Skor Indeks Korupsi (CPI)'], name='Korupsi', line=dict(color=Theme.NEUTRAL, width=3, dash='dot'), yaxis='y2', mode='lines+markers'))

        fig_doom.update_layout(
            template=PLOT_TEMPLATE,
            xaxis=dict(
                title="Tahun",
                tickmode='linear',
                dtick=1,
                showgrid=False
            ),
            yaxis=dict(
                title=dict(
                    text='Lansia', 
                    font=dict(color=Theme.BAD)), 
                    showgrid=False
            ),
            yaxis2=dict(
                title=dict(
                    text='CPI', 
                    font=dict(color=Theme.NEUTRAL)), 
                    overlaying='y', 
                    side='right', 
                    showgrid=False
            ),
            legend=dict(
                orientation="h", 
                y=1.1, font=dict(color=Theme.TEXT)
            ), 
            height=300, 
            margin=dict(l=0,r=0,t=30,b=0), 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)'
        )
        fig_doom.update_xaxes(dtick=1, tickformat="d", showgrid=True, gridcolor='#333')
        st.plotly_chart(fig_doom, use_container_width=True)
        st.markdown(f'<div class="insight-box"><b>Trade-off:</b> Kurva menunjukkan korelasi antara jumlah lansia dan skor korupsi. Semakin banyak lansia, maka semakin sedikit untuk kesejahteraan Pejabat.</div>', unsafe_allow_html=True)

    # BAB III
    st.markdown("---")
    st.markdown('<div class="bab-header"><h2>BAB III: SOLUSI MASA DEPAN (Prediktif)</h2></div>', unsafe_allow_html=True)
    
    def format_indo(value):
        if value >= 1e12: return f"{value/1e12:.2f} T".replace('.', ',')
        elif value >= 1e9: return f"{value/1e9:.2f} M".replace('.', ',')
        elif value >= 1e6: return f"{value/1e6:.2f} Juta"
        else: return f"{value:,.0f}".replace(',', '.')

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 8. Analisis Modal dan Pendapatan")
        
        if df_roi_simulated is not None:
            plot_df = df_roi_simulated.copy()
            plot_df['Label'] = plot_df['Nominal'].apply(format_indo)
            
            tick_vals = [1e6, 1e7, 1e8, 1e9]
            tick_text = ["1 Juta", "10 Juta", "100 Juta", "1 Miliar"]
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=plot_df['Komponen'], 
                y=plot_df['Nominal'],
                text=plot_df['Label'],
                marker_color=[Theme.BAD, Theme.GOOD, Theme.NEUTRAL],
                textposition='outside',
                textfont=dict(color='white'),
                name='Nominal'
            ))
            
            fig.update_layout(
                template=PLOT_TEMPLATE,
                showlegend=False,
                height=500,
                margin=dict(t=50, b=0, l=20, r=20), 
                yaxis=dict(
                    type="log",
                    range=[6, 10],
                    showgrid=True,
                    gridcolor="#333",
                    showticklabels=True,
                    tickvals=tick_vals,
                    ticktext=tick_text,
                    title=None
                ),
                xaxis=dict(title=None),
                separators=",."
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f'<div class="success-box"><b>The Deal:</b> Investasi Kecil menghasilkan Penghematan yang Luar Biasa. Secara matematis, ini merupakan solusi mutlak bagi Indonesia agar terlepas dari ruang fiskal dan korupsi.</div>', unsafe_allow_html=True)    
        else:
            st.error("Data ROI tidak tersedia.")

    with col2:
        st.markdown("#### 9. Target Gaji Baru")
        target_gaji = df5_simulated[df5_simulated['Tahun'] == 2027]['Proyeksi Gaji DPR (Juta)'].values[0] / 1000
        indo_now = df3[df3['Negara'] == 'Indonesia']['Gaji Pejabat per Tahun (Miliar Rupiah)'].values[0]
        gap_data = pd.DataFrame({
            "Kondisi": ["Sekarang", f"Target ({simulation_factor}x)", "Singapura"],
            "Gaji (Miliar)": [indo_now, target_gaji, 2.48],
            "Warna": [Theme.BAD, Theme.GOOD, Theme.NEUTRAL]
        })
        gap_data['Label'] = gap_data['Gaji (Miliar)'].apply(lambda x: f"{x:,.2f} M".replace('.', ','))
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=gap_data['Kondisi'], y=gap_data['Gaji (Miliar)'], text=gap_data['Label'], marker_color=gap_data['Warna'], textposition='outside', cliponaxis=False))
        fig.update_layout(template=PLOT_TEMPLATE, showlegend=False, height=500, yaxis=dict(showgrid=True, gridcolor='#333', ticksuffix=" M"), separators=",.")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f'<div class="success-box"><b>Reformasi:</b> Kurva menunjukkan target gaji pejabat negara yang baru sebagai solusi pemberantasan korupsi di Indonesia. Dengan menaikkan gaji pokok pejabat negara hingga melebihi standar Singapura menggunakan dana penghematan tersebut, negara secara efektif mematikan motif ekonomi untuk melakukan korupsi.</div>', unsafe_allow_html=True)

    with col3:
        st.markdown("#### 10. Proyeksi Korupsi Hilang")
        df5_simulated['Gaji_Miliar'] = df5_simulated['Proyeksi Gaji DPR (Juta)'] / 1000

        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df5_simulated['Tahun'], 
            y=df5_simulated['Gaji_Miliar'],
            fill='tozeroy', 
            fillcolor='rgba(0, 255, 159, 0.2)', 
            name='Gaji (Naik)', 
            line=dict(color=Theme.GOOD, width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=df5_simulated['Tahun'], 
            y=df5_simulated['Proyeksi Kasus Korupsi'],
            name='Korupsi (Turun)', 
            line=dict(color=Theme.BAD, width=4), 
            yaxis='y2'
        ))
        
        fig.update_layout(
            template=PLOT_TEMPLATE,
            xaxis=dict(
                title="Tahun",
                tickmode='linear',
                dtick=1,
                showgrid=False
            ),
            yaxis=dict(
                title=dict(text="Total Anggaran Gaji (Miliar)", font=dict(color=Theme.GOOD)),
                tickmode='array',
                tickvals=[0.5, 1, 1.5, 2, 2.5, 3, 3.5],
                showgrid=True,
                gridcolor='#333'
            ),
            yaxis2=dict(
                title=dict(text="Kasus Korupsi", font=dict(color=Theme.BAD)),
                overlaying='y', 
                side='right', 
                showgrid=False
            ),
            height=500, 
            margin=dict(t=30, b=0, l=0, r=0), 
            legend=dict(orientation="h", y=1.1)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f'<div class="success-box"><b>Future State:</b> Kurva menunjukkan proyeksi Indonesia pasca-program Euthanasia. Data terbaru menunjukkan lonjakan kasus korupsi di 2023 sebanyak 791 kasus. Solusi kenaikan gaji adalah satu-satunya jalan keluar untuk menyelesaikan kasus korupsi.</div>', unsafe_allow_html=True)