from datetime import date

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from shared import FEATURES, HORIZONS, MODEL_FILES, load_model


def render():
    st.title("Prediksi Harga Nikel Dunia")

    
    # ----------------------------------------------
    # PANDUAN PENGAMBILAN DATA
    # ----------------------------------------------

    with st.expander(
        "📚 Panduan Pengambilan Data",
        expanded=False
    ):
        st.markdown("""
        ### Cara Mengisi Data Prediksi

        Sebelum melakukan prediksi, siapkan 10 variabel input
        berdasarkan tanggal acuan yang dipilih. Gunakan sumber
        data berikut untuk memperoleh nilai yang sesuai.

        ---

        ### A. Data Harga dan Stok Logam LME

        **1. LME Nickel Stock**

        - [Buka data Nickel di Westmetall](https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Ni_cash)
        - Cari tanggal acuan/terakhir pada tabel.
        - Ambil nilai pada kolom **LME Nickel Stock**.
        - Satuan: ton.

        **2. LME Aluminium Price**

        - [Buka data Aluminium di Westmetall](https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Al_cash)
        - Cari tanggal acuan/terakhir.
        - Ambil nilai **LME Aluminium Cash-Settlement**.

        **3. LME Copper Price**

        - [Buka data Copper di Westmetall](https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Cu_cash)
        - Cari tanggal acuan/terakhir.
        - Ambil nilai **LME Copper Cash-Settlement**.

        **4. LME Zinc Price**

        - [Buka data Zinc di Westmetall](https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Zn_cash)
        - Cari tanggal acuan/terakhir.
        - Ambil nilai **LME Zinc Cash-Settlement**.

        **Catatan:** Pastikan menggunakan kolom Cash-Settlement,
        bukan harga 3-month. Untuk Nickel, input yang dibutuhkan
        adalah stok nikel, bukan harga nikel.

        ---

        ### B. Indeks Dolar AS

        **5. Dollar Index**

        - [Buka data Dollar Index di FRED](https://fred.stlouisfed.org/series/DTWEXBGS)
        - Ambil nilai indeks terakhir.

        **Jika data tanggal acuan belum tersedia**, misalnya karena
        tanggal tersebut merupakan akhir pekan, hari libur, atau
        data belum dipublikasikan, gunakan nilai terakhir yang
        tersedia sebelum tanggal acuan.

        Jangan mengisi nilai perkiraan sendiri.

        ---

        ### C. Harga Minyak Mentah

        **6. WTI Price**

        - [Buka data WTI Price di FRED](https://fred.stlouisfed.org/series/DCOILWTICO)
        - Ambil harga minyak mentah WTI terakhir.
        - Satuan: dolar AS per barel (USD/barrel).

        **Jika data tanggal acuan belum tersedia**, gunakan nilai
        terakhir yang tersedia sebelum tanggal acuan. 

        Perhatikan bahwa nilai WTI dapat bernilai negatif pada
        kondisi pasar tertentu. Masukkan nilai sesuai data sumber.

        ---

        ### D. Harga Bijih Besi

        **7. Iron Ore Price**

        - [Buka data Iron Ore 62% CFR Futures di Investing.com](https://id.investing.com/commodities/iron-ore-62-cfr-futures)
        - Buka bagian data historis (*Historical Data*).
        - Pilih frekuensi harian (*Daily*).
        - Cari tanggal acuan/terakhir dan ambil nilai **Close**.


        ---

        ### E. Riwayat Harga Nikel

        Tiga input terakhir menggunakan riwayat harga nikel
        yang tersedia sebelum tanggal acuan.

        **8. LME Nickel Price (H-1)**

        - [Buka data Nickel di Westmetall](https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Ni_cash)
        - Ambil harga Cash-Settlement dari satu hari pengamatan
          sebelumnya.

        **9. LME Nickel Price (H-2)**

        - Ambil harga Cash-Settlement dari dua hari pengamatan
          sebelumnya.

        **10. LME Nickel Price (H-3)**

        - Ambil harga Cash-Settlement dari tiga hari pengamatan
          sebelumnya.

        H-1, H-2, dan H-3 mengacu pada urutan hari pengamatan
        dalam data, bukan selalu hari kalender. Jika tidak ada
        perdagangan pada akhir pekan atau hari libur, gunakan
        pengamatan perdagangan sebelumnya sesuai urutan data.

        ---

        ### Hal yang Perlu Diperhatikan

        1. Jika data tanggal acuan tidak tersedia, gunakan data
           terakhir sebelum tanggal acuan, jangan memasukkan nol 
           hanya karena data tidak ditemukan.
        2. Jangan mengubah satuan atau menggunakan kolom harga
           yang berbeda dari seri yang digunakan saat pelatihan.
        3. Aplikasi ini tidak mengambil data pasar secara otomatis.
           Seluruh input harus dimasukkan oleh pengguna.
        """)


    st.write(
        "Masukkan data terbaru yang tersedia. Sistem akan "
        "menghasilkan prediksi untuk horizon 1, 2, 3, 4, dan 5 hari "
        "dalam satu kali proses."
    )

    tanggal_acuan = st.date_input(
        "Tanggal acuan prediksi",
        value=date.today()
    )

    st.caption(
        "Tanggal acuan digunakan sebagai referensi input. "
        "Aplikasi tidak mengambil data pasar secara otomatis."
    )

    st.divider()

    # ----------------------------------------------
    # A. VARIABEL EKSTERNAL
    # ----------------------------------------------

    def number_input_with_source(label, source_url, **kwargs):
        label_with_source = f"{label} ([Buka Sumber]({source_url}))"
        return st.number_input(label_with_source, **kwargs)

    st.subheader("A. Variabel Eksternal")

    col1, col2 = st.columns(2)

    with col1:
        nickel_stock = number_input_with_source(
            "LME Nickel Stock (USD/ton)",
            "https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Ni_cash",
            value=None,
            step=1.0,
            format="%.0f",
            placeholder="15545",
            help="Masukkan nilai stok nikel terakhir yang tersedia.",
        )

        dollar_index = number_input_with_source(
            "Dollar Index (index)",
            "https://fred.stlouisfed.org/series/DTWEXBGS",
            value=None,
            format="%.4f",
            placeholder="121.3848",
            help="Masukkan indeks dolar terakhir yang tersedia.",
        )

        wti_price = number_input_with_source(
            "WTI Price (USD/barrel)",
            "https://fred.stlouisfed.org/series/DCOILWTICO",
            value=None,
            format="%.2f",
            placeholder="96.24",
            help="Nilai negatif diperbolehkan sesuai data sumber.",
        )

    with col2:
        aluminium_price = number_input_with_source(
            "LME Aluminium Price (USD/ton)",
            "https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Al_cash",
            value=None,
            step=0.1,
            format="%.1f",
            placeholder="3055.5",
            help="Masukkan harga aluminium terakhir yang tersedia.",
        )

        copper_price = number_input_with_source(
            "LME Copper Price (USD/ton)",
            "https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Cu_cash",
            value=None,
            step=0.1,
            format="%.1f",
            placeholder="14689",
            help="Masukkan harga tembaga terakhir yang tersedia.",
        )

        zinc_price = number_input_with_source(
            "LME Zinc Price (USD/ton)",
            "https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Zn_cash",
            value=None,
            step=0.1,
            format="%.1f",
            placeholder="3840",
            help="Masukkan harga seng terakhir yang tersedia.",
        )

        iron_ore_price = number_input_with_source(
            "Iron Ore Price (USD/ton)",
            "https://id.investing.com/commodities/iron-ore-62-cfr-futures",
            value=None,
            format="%.2f",
            placeholder="90.68",
            help="Masukkan harga bijih besi terakhir yang tersedia.",
        )


    st.subheader("B. Riwayat Harga Nikel")

    lag_source = (
        "https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Ni_cash"
    )

    lag_col1, lag_col2, lag_col3 = st.columns(3)

    with lag_col1:
        lag1 = number_input_with_source(
            "LME Nickel Price (H-1) (USD/ton)",
            lag_source,
            value=None,
            format="%.2f",
            placeholder="15415",
            help="Masukkan harga nikel satu hari sebelumnya.",
        )

    with lag_col2:
        lag2 = number_input_with_source(
            "LME Nickel Price (H-2) (USD/ton)",
            lag_source,
            value=None,
            format="%.2f",
            placeholder="15645",
            help="Masukkan harga nikel dua hari sebelumnya.",
        )

    with lag_col3:
        lag3 = number_input_with_source(
            "LME Nickel Price (H-3) (USD/ton)",
            lag_source,
            value=None,
            format="%.2f",
            placeholder="15530",
            help="Masukkan harga nikel tiga hari sebelumnya.",
        )
        

    # ----------------------------------------------
    # C. PROSES PREDIKSI SEMUA HORIZON
    # ----------------------------------------------

    if st.button("Prediksi Semua Horizon", type="primary"):

        input_data = {
            "LME Nickel Stock": nickel_stock,
            "LME Aluminium Price": aluminium_price,
            "LME Copper Price": copper_price,
            "LME Zinc Price": zinc_price,
            "Iron Ore Price": iron_ore_price,
            "Dollar Index": dollar_index,
            "WTI Price": wti_price,
            "LME Nickel Price Lag 1": lag1,
            "LME Nickel Price Lag 2": lag2,
            "LME Nickel Price Lag 3": lag3,
        }

        # Validasi angka
        if any(
            v is None or not isinstance(v, (int, float, np.number))
            or not np.isfinite(v)
            for v in input_data.values()
        ):
            st.error(
                "Semua input harus berupa angka yang valid."
            )

        # Nol tidak diperbolehkan untuk seluruh fitur
        elif any(v == 0 for v in input_data.values()):
            st.error(
                "Input tidak boleh bernilai nol. "
                "Periksa kembali semua kolom."
            )

        # Nilai negatif hanya diperbolehkan untuk WTI
        elif any(
            v < 0
            for feature, v in input_data.items()
            if feature != "WTI Price"
        ):
            st.error(
                "Nilai negatif hanya diperbolehkan pada WTI Price. "
                "Sembilan fitur lainnya harus bernilai positif."
            )

        else:
            # Susun data sesuai urutan fitur model
            X = pd.DataFrame(
                [[input_data[f] for f in FEATURES]],
                columns=FEATURES
            )

            hasil_prediksi = {}

            try:
                # Periksa keberadaan seluruh file model
                missing_models = [
                    str(MODEL_FILES[h])
                    for h in HORIZONS
                    if not MODEL_FILES[h].exists()
                ]

                if missing_models:
                    st.error(
                        "File model berikut tidak ditemukan:\n\n"
                        + "\n".join(missing_models)
                    )
                    st.stop()

                # Jalankan seluruh model untuk horizon 1–5
                for horizon in HORIZONS:
                    model = load_model(
                        str(MODEL_FILES[horizon])
                    )

                    model_features = getattr(
                        model, "feature_names_", None
                    )

                    if model_features:
                        if (
                            len(model_features) != len(FEATURES)
                            or set(model_features) != set(FEATURES)
                        ):
                            raise ValueError(
                                f"Fitur model horizon {horizon} hari "
                                "tidak sesuai dengan fitur aplikasi."
                            )

                        X_model = X[model_features]
                    else:
                        X_model = X

                    prediction = float(
                        np.asarray(
                            model.predict(X_model)
                        ).reshape(-1)[0]
                    )

                    if not np.isfinite(prediction):
                        raise ValueError(
                            f"Prediksi horizon {horizon} hari "
                            "menghasilkan angka yang tidak valid."
                        )

                    hasil_prediksi[horizon] = prediction

                
                # ----------------------------------
                # TAMPILKAN HASIL
                # ----------------------------------

                st.success(
                    "Kelima prediksi berhasil dihasilkan."
                )

                st.subheader("Hasil Prediksi")

                # Kartu metrik H+1 sampai H+5
                cols = st.columns(len(HORIZONS))

                for col, horizon in zip(cols, HORIZONS):
                    col.metric(
                        f"Prediksi H+{horizon} (USD/ton)",
                        f"{hasil_prediksi[horizon]:,.2f}",
                    )

                # ----------------------------------
                # GRAFIK PREDIKSI HARI KE-1 S.D. 5
                # ----------------------------------

                st.subheader("Grafik Prediksi Harga Nikel")

                grafik_df = pd.DataFrame({
                    "Horizon": [
                        f"H+{h}" for h in HORIZONS
                    ],
                    "Harga Prediksi": [
                        hasil_prediksi[h] for h in HORIZONS
                    ]
                })

                fig_prediksi = px.line(
                    grafik_df,
                    x="Horizon",
                    y="Harga Prediksi",
                    markers=True,
                    labels={
                        "Horizon": "Horizon Prediksi",
                        "Harga Prediksi": "Harga Nikel (USD/ton)",
                    },
                )

                fig_prediksi.update_traces(
                    mode="lines+markers+text",
                    line_color="#69C2C7",
                    marker_color="#FFFFFF",
                    marker_size=9,
                    textposition="top center",
                    texttemplate=(
                        "Horizon: %{x}<br>"
                        "Harga: %{y:,.2f} USD/ton"
                    ),
                    textfont=dict(color="#F1F6F7", size=11),
                    cliponaxis=False,
                    hovertemplate="%{x}: %{y:,.2f} USD/ton<extra></extra>",
                )

                fig_prediksi.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#F1F6F7"),
                    xaxis=dict(
                        gridcolor="rgba(190, 220, 224, 0.2)"
                    ),
                    yaxis=dict(
                        gridcolor="rgba(190, 220, 224, 0.2)"
                    ),
                )

                st.plotly_chart(
                    fig_prediksi,
                    use_container_width=True,
                    config={
                        "displayModeBar": True,
                        "displaylogo": False,
                        "scrollZoom": True,
                    },
                )

                st.caption(
                    "H+1 hingga H+5 menunjukkan horizon prediksi "
                    "1 sampai 5 hari ke depan. Grafik menghubungkan "
                    "kelima estimasi harga yang dihasilkan oleh model. "
                    "Hasil merupakan estimasi model, bukan harga pasar "
                    "aktual atau jaminan harga di masa depan. "
                    "Seluruh prediksi menggunakan input yang sama."
                )

            except Exception as e:
                st.error(
                    "Prediksi gagal dijalankan. Periksa file model, "
                    "nama fitur, dan kompatibilitas model."
                )
                st.exception(e)
