import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def show(data_pack, Theme):
    df1, df2, df3, df4, df5, df_roi, df_trend, df_pensiun = data_pack
    PLOT_TEMPLATE = "plotly_dark"

    st.title("De-Framing Data: Memisahkan Mitos Beban Demografi dari Realitas Korupsi Struktural")
    st.markdown(
        f"<h3 style='color: {Theme.NEUTRAL} !important; font-weight: 300; margin-top: -15px; letter-spacing: 1px;'>Koreksi Statistik atas Narasi Efisiensi Anggaran Berbasis Euthanasia</h3>", 
        unsafe_allow_html=True)
    st.markdown("---")

    with st.sidebar:
        st.header("Control Room")
        st.subheader("Tingkat Eksekusi")
        simulation_factor = st.slider("Multiplier Kebijakan (0.5x - 3.0x):", min_value=0.5, max_value=3.0, value=1.0, step=0.5)
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

        st.markdown('<div class="bab-header"><h2>BAB I: Latar Belakang</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 1. Tren Penduduk Lansia")
        
        if df2 is not None:
            df2_plot = df2.sort_values('Tahun')
            
            fig = px.line(df2_plot, x='Tahun', y='Jumlah Lansia (Juta Jiwa)', markers=True)            
            fig.update_traces(
                line_color=Theme.NEUTRAL, 
                line_width=4,
                marker_size=10,
                marker_line_color='white',
                marker_line_width=2
            )

            fig.update_layout(
                template=PLOT_TEMPLATE,
                xaxis=dict(
                    title="Tahun", 
                    tickmode='array', 
                    tickvals=df2_plot['Tahun'], 
                    type='category'
                ),
                yaxis=dict(title="Jumlah (Juta Jiwa)"),
                height=350,
                margin=dict(t=30, b=0, l=0, r=0),
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"""
                        <div class="insight-box" style="border-left-color: {Theme.NEUTRAL}; color: {Theme.TEXT};">
                        <b>Konteks Data:</b> Jika dilihat secara menyeluruh, tren kenaikan lansia terlihat lebih landai. Dan kenaikan ini adalah fenomena demografi global yang tidak bisa dihindari.
                        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("### 2. Tren Biaya Penyakit Katastropik")
        if df_trend is not None:
            df_trend['Biaya_Triliun'] = df_trend['Biaya'] / 1_000_000_000_000

            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=df_trend['Tahun'], y=df_trend['Biaya_Triliun'], cliponaxis=False,
                marker=dict(color=Theme.NEUTRAL), text=df_trend['Biaya_Triliun'].round(1), textposition='outside', name='Biaya Realisasi'))
            fig.update_layout(template=PLOT_TEMPLATE, height=300, margin=dict(l=20, r=20, t=50, b=50),
                xaxis=dict(tickmode='array', tickvals=df_trend['Tahun'], title='Tahun'),
                yaxis=dict(title='Triliun Rupiah', showgrid=True, gridcolor='#333', range=[0, df_trend['Biaya_Triliun'].max() * 1.3]),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(f"""
            <div class="insight-box" style="border-left-color: {Theme.NEUTRAL}; color: {Theme.TEXT};">
            <b></b> Kenaikan biaya ini berkorelasi positif dengan peningkatan jumlah populasi lanjut usia dan peningkatan penyakit katastropik.
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("3. Tren Alokasi Dana Pensiun")
        if df_pensiun is not None:
            col_anggaran = 'Anggaran(Triliun)'
            fig_pensiun = px.bar(df_pensiun, x='Tahun', y=col_anggaran, text=col_anggaran,
                                 color_continuous_scale=[Theme.NEUTRAL])
            fig_pensiun.update_traces(texttemplate='Rp %{text} T', textposition='outside')
            fig_pensiun.update_layout(template=PLOT_TEMPLATE, height=320, bargap=0.50, 
                                      yaxis=dict(range=[0, df_pensiun[col_anggaran].max() * 1.3], showgrid=True, gridcolor='#333'),
                                      xaxis=dict(title="Tahun"))
            
            st.plotly_chart(fig_pensiun, use_container_width=True)

            st.markdown(f"""
            <div class="insight-box" style="border-left-color: {Theme.NEUTRAL}; color: {Theme.TEXT};">
            <b>Perspektif Anggaran:</b> Kenaikan nominal anggaran pensiun adalah hal yang alami akibat akumulasi jumlah pensiunan ASN/TNI/Polri setiap tahun yang bertambah. .
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("#### 4. Komparasi Biaya Per Kapita")
        
        df1_clean = df1.copy()
        df1_clean['Kategori'] = df1_clean['Kategori'].astype(str).str.strip()
        df1_clean['Kategori'] = df1_clean['Kategori'].replace({
            'Gaji Pokok DPR RI (Setahun)': 'Gaji + Tunjangan DPR RI ',
            'Belanja Pensiun APBN': 'Gaji Pensiun',
            'Biaya katastropik BPJS': 'Biaya katastropik BPJS'
        })
        
        def format_juta(value):
            if value >= 1e6:
                return f"Rp {value/1e6:,.1f} Juta"
            else:
                return f"Rp {value:,.0f}"
        
        df1_clean['Label_Text'] = df1_clean['Nominal'].apply(format_juta)
        df1_sorted = df1_clean.sort_values(by="Nominal", ascending=True)

        fig_ineq = px.bar(
            df1_sorted, 
            x="Nominal", 
            y="Kategori", 
            orientation='h', 
            text="Label_Text"
        )
        
        colors = []
        for kat in df1_sorted['Kategori']:
            if 'DPR' in kat.upper() or 'PEJABAT' in kat.upper():
                colors.append(Theme.NEUTRAL)  
            else:
                colors.append(Theme.NEUTRAL) 
        
        fig_ineq.update_traces(
            marker_color=colors,
            textposition="outside",
            textfont=dict(size=12, color='white'),
            cliponaxis=False
        )

        max_val = df1_sorted['Nominal'].max()
        
        fig_ineq.update_layout(
            template=PLOT_TEMPLATE, 
            height=300, 
            margin=dict(l=200, r=50, t=20, b=20), 
            xaxis=dict(
                title="Rata-rata Penerimaan per Tahun (Rupiah)", 
                showgrid=True,
                gridcolor='#333',
                range=[0, max_val * 1.3]
            ),
            yaxis=dict(title=None, automargin=True),
            showlegend=False
        )
        
        st.plotly_chart(fig_ineq, use_container_width=True)
        
        st.markdown(f"""
        <div class="insight-box" style="border-left-color: {Theme.NEUTRAL}; color: {Theme.TEXT};">
        <b>Realitas Per Kapita:</b> Setelah data dibagi berdasarkan jumlah penerima, terlihat jelas bahwa alokasi per individu untuk Pensiunan/Pasien BPJS penyakit katastropik jauh lebih kecil dibandingkan alokasi per Pejabat (Bar Biru Tua). 
        <br><br>
        Ini meluruskan framing sebelumnya yang seolah-olah menggambarkan pensiunan sebagai beban anggaran terbesar hanya karena jumlah mereka jutaan orang.
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="bab-header"><h2>BAB II: Analisis Diagnostik</h2></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 5. Tren Indeks Persepsi Korupsi (CPI)")

        if df2 is not None:
            df2_filtered = df2.sort_values('Tahun')
            
            fig_cpi = px.line(
                df2_filtered, 
                x='Tahun', 
                y='Skor Indeks Korupsi (CPI)',
                markers=True
            )
            
            fig_cpi.update_traces(
                line_color=Theme.NEUTRAL,
                line_width=3,
                marker_size=8,
                marker_color='white',
                marker_line_width=2,
                marker_line_color=Theme.NEUTRAL
            )
            
            fig_cpi.update_layout(
                template=PLOT_TEMPLATE, 
                height=300, 
                yaxis=dict(
                    title="Skor (0=Korup, 100=Bersih)", 
                    range=[0, 100], 
                    showgrid=True, 
                    gridcolor='#333',
                    zeroline=True,
                    zerolinecolor='#555'
                ),
                xaxis=dict(
                    title="Tahun",
                    tickmode='array',
                    tickvals=df2_filtered['Tahun']
                ),
                margin=dict(t=20, b=20, l=40, r=20)
            )
        st.plotly_chart(fig_cpi, use_container_width=True)
            
        st.markdown(f"""
        <div class="insight-box" style="border-left-color: {Theme.NEUTRAL}; color: {Theme.TEXT};">
        <b>Konteks Skala:</b> 
        Posisi garis berada pada kisaran 30-40 menunjukkan bahwa meskipun fluktuasinya terlihat minim, 
        Indonesia secara konsisten masih berada di kuadran negara dengan tantangan korupsi yang serius, jauh dari skor ideal 100.
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("#### 6. Benchmark: Gaji dan Korupsi")
        if df3 is not None:
            df3_clean = df3.copy()
            col_cpi = [c for c in df3.columns if 'cpi' in c.lower() or 'skor' in c.lower()][0]
            col_gaji = [c for c in df3.columns if 'gaji' in c.lower()][0]
            df3_clean['Gaji_Miliar'] = df3_clean[col_gaji]

            fig = px.scatter(
                df3_clean, 
                x='Gaji_Miliar', 
                y=col_cpi,
                text="Negara",  
                color='Negara',
                size=[60]*len(df3_clean),
            )
            fig.update_traces(
                textposition='top center', 
                marker=dict(line=dict(width=1, color='DarkSlateGrey'))
            )
            fig.update_layout(
                template=PLOT_TEMPLATE, 
                height=400, 
                showlegend=False,
                xaxis=dict(
                    title="Gaji Pejabat per Tahun (Miliar Rupiah)", 
                    showgrid=True,
                    zeroline=True,
                ),
                yaxis=dict(
                    title="Skor CPI (0=Korup, 100=Bersih)", 
                    range=[0, 100], 
                    showgrid=True
                ),
                margin=dict(t=40)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown(f"""
            <div class="insight-box" style="border-left-color: {Theme.NEUTRAL}; color: {Theme.TEXT};">
            <b>Fakta Kontradiktif:</b> Data real menunjukkan korelasi yang tidak konsisten.
            <br>
            • <b>Filipina</b> Memiliki gaji pejabat yang lebih tinggi dari Indonesia (~1 Miliar vs 787 Juta), tapi skor korupsinya justru lebih rendah/buruk.
            <br>
            • <b>Kolombia</b> Memiliki gaji pejabat yang jauh lebih tinggi dari Indonesia (~1.5 Miliar vs 787 Juta), tapi skor korupsinya justru lebih rendah/buruk.
            <br>
            • <b>Malaysia</b> Memiliki gaji yang relatif setara atau bahkan lebih rendah dengan Indonesia, tapi indeks kebersihannya jauh lebih tinggi (50 vs 37).
            <br><br>
            Ini membuktikan bahwa <b>menaikkan gaji bukan solusi tunggal</b> (Silver Bullet). Faktor penegakan hukum dan sistem politik jauh lebih berpengaruh.
            </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown("#### 7. Uji Validitas Hubungan")
        df2_filtered = df2[(df2['Tahun'] >= 2020) & (df2['Tahun'] <= 2024)]

        fig_doom = go.Figure()
        
        fig_doom.add_trace(go.Scatter(x=df2_filtered['Tahun'], y=df2_filtered['Jumlah Lansia (Juta Jiwa)'], name='Lansia', line=dict(color=Theme.NEUTRAL, width=4), mode='lines+markers'))
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
                    font=dict(color=Theme.NEUTRAL)), 
                    showgrid=False),
            yaxis2=dict(
                title=dict(
                    text='CPI', 
                    font=dict(color=Theme.NEUTRAL)), 
                    overlaying='y', side='right', 
                    showgrid=False),
            legend=dict(
                orientation="h", 
                y=1.1, 
                font=dict(color=Theme.TEXT)), 
                height=300, 
                margin=dict(l=0,r=0,t=30,b=0), 
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)'
        )
        fig_doom.update_xaxes(dtick=1, tickformat="d", showgrid=True, gridcolor='#333')
        st.plotly_chart(fig_doom, use_container_width=True)
        st.markdown(f"""
            <div class="insight-box" style="border-left-color: {Theme.NEUTRAL}; color: {Theme.TEXT};">
            <b>Observasi Data:</b> Grafik ini menyandingkan dua variabel berbeda bahkan tidak ada korelasi. 
            Meskipun garisnya terlihat bersamaan, fluktuasi indeks korupsi (Garis Putus-putus) tidak memiliki kausalitas langsung dengan pertumbuhan populasi lansia (Garis Biru).
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="bab-header"><h2>BAB III: SOLUSI MASA DEPAN (Prediktif)</h2></div>', unsafe_allow_html=True)
    
    def format_indo(value):
        if value >= 1e12: return f"{value/1e12:.2f} T".replace('.', ',')
        elif value >= 1e9: return f"{value/1e9:.2f} M".replace('.', ',')
        elif value >= 1e6: return f"{value/1e6:.2f} Juta"
        else: return f"{value:,.0f}".replace(',', '.')

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 8. Perbandingan Biaya: Merawat vs Mengakhiri")
        
        if df_roi_simulated is not None:
            plot_df = df_roi_simulated[df_roi_simulated['Komponen'].isin(['Biaya Awal', 'Modal'])].copy()
            
            plot_df['Komponen'] = plot_df['Komponen'].replace({
                'Biaya Awal': 'Biaya Perawatan (10 Tahun)',
                'Modal': 'Biaya Suntik Mati'
            })

            plot_df['Label'] = plot_df['Nominal'].apply(format_indo)
            
            colors = []
            for k in plot_df['Komponen']:
                if 'Perawatan' in k:
                    colors.append(Theme.NEUTRAL)  
                else:
                    colors.append('#8B0000')

            tick_vals = [1e6, 1e7, 1e8, 1e9]
            tick_text = ["1 Juta", "10 Juta", "100 Juta", "1 Miliar"]
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=plot_df['Komponen'], 
                y=plot_df['Nominal'],
                text=plot_df['Label'],
                marker_color=colors,
                textposition='outside',
                textfont=dict(color='white'),
                name='Nominal'
            ))
            
            fig.update_layout(
                template=PLOT_TEMPLATE,
                showlegend=False,
                height=500,
                margin=dict(t=0, b=0, l=40, r=20), 
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
            st.markdown(f"""
            <div class="insight-box" style="border-left-color: {Theme.NEUTRAL}; color: {Theme.TEXT};">
            <b>Dilema Moral (Moral Hazard):</b> 
            Grafik ini menunjukkan realitas yang mengerikan biaya "mematikan" (Merah) jauh lebih murah daripada "merawat" (Biru).
            <br><br>
            Dalam logika bisnis, opsi merah adalah "efisiensi". Namun dalam etika bernegara, <b>efisiensi anggaran tidak boleh menjadi alasan untuk melakukan sesuatu yang tidak berdasarkan fakta yang valid apalagi sampai menghilangkan hak hidup warga negara</b>. Nyawa manusia tidak memiliki <i>Price Tag</i> yang bisa diperdagangkan demi surplus APBN.
            </div>""", unsafe_allow_html=True)
        else:
             st.error("Data ROI tidak tersedia.")

    with col2:
        st.markdown("#### 9. Gap Analysis: Nominal vs Benchmark")
        
        indo_now = df3[df3['Negara'] == 'Indonesia']['Gaji Pejabat per Tahun (Miliar Rupiah)'].values[0]
        
        target_gaji = df5_simulated[df5_simulated['Tahun'] == 2027]['Proyeksi Gaji DPR (Juta)'].values[0] / 1000
        
        sing_gaji = df3[df3['Negara'] == 'Singapura']['Gaji Pejabat per Tahun (Miliar Rupiah)'].values[0]

        gap_data = pd.DataFrame({
            "Kategori": ["Gaji Saat Ini", f"Usulan Kenaikan", "Benchmark (Singapura)"],
            "Nominal_Miliar": [indo_now, target_gaji, sing_gaji],
            "Warna": ['#888888', Theme.NEUTRAL, '#B0B0B0'] 
        })
        
        gap_data['Label'] = gap_data['Nominal_Miliar'].apply(lambda x: f"{x:,.2f} M".replace('.', ','))
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=gap_data['Kategori'], 
            y=gap_data['Nominal_Miliar'],
            textposition='outside',
            text=gap_data['Label'],
            marker_color=[Theme.NEUTRAL, Theme.NEUTRAL, "#555555"], 
        ))
        
        fig.update_layout(
            template=PLOT_TEMPLATE, 
            showlegend=False, 
            height=500, 
            yaxis=dict(
                title="Nominal Gaji (Miliar Rupiah)",
                showgrid=True, 
                gridcolor='#333', 
                ticksuffix=" M"
            ),
            xaxis=dict(title=None),
            margin=dict(b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
        <div class="insight-box" style="border-left-color: {Theme.NEUTRAL}; color: {Theme.TEXT};">
        <b>Realitas Ekonomi:</b> Grafik ini menunjukkan bahwa usulan kenaikan (Bar Tengah) berusaha mengejar standar Singapura (Bar Kanan).  
        <br><br>
        Namun, perlu Menuntut gaji nominal yang setara tanpa menyeimbangkan dengan kemampuan ekonomi negara adalah bentuk <b>kesenjangan ekspektasi</b>.
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown("#### 10. Implikasi Fiskal (Kepastian Beban)")
        
        df5_simulated['Beban_Miliar'] = df5_simulated['Proyeksi Gaji DPR (Juta)'] / 1000
        
        fig = px.bar(
            df5_simulated, 
            x='Tahun', 
            y='Beban_Miliar',
            text='Beban_Miliar',
            color_discrete_sequence=[Theme.NEUTRAL] 
        )
        
        fig.update_traces(
            texttemplate='Rp %{text:,.1f} M', 
            textposition='outside'
        )
        fig.update_layout(
            template=PLOT_TEMPLATE,
            height=500,
            yaxis=dict(
                title="Estimasi Total Beban Gaji (Miliar Rupiah)",
                showgrid=True,
                gridcolor='#333',
                range=[0, df5_simulated['Beban_Miliar'].max() * 1.2] 
            ),
            xaxis=dict(title="Tahun Anggaran"),
            margin=dict(t=50),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
        <div class="insight-box" style="border-left-color: {Theme.NEUTRAL}; color: {Theme.TEXT};">
        <b>Trade-off Asimetris:</b> 
        Grafik ini menampilkan <b>Kepastian Biaya</b>. Jika kebijakan ini disahkan negara.
        <br><br>
        Namun perlu diingat, penurunan korupsi (yang digambarkan turun drastis di dashboard framing) hanyalah <b>Hipotesis Tak Terjamin</b>. 
        Dalam etika kebijakan publik, tidak boleh menjual harapan (turunnya korupsi) sebagai jaminan untuk membenarkan pengeluaran yang pasti (naiknya gaji).
        </div>""", unsafe_allow_html=True)