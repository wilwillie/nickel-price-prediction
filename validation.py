import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from shared import HORIZONS, MODEL_DIR


def render():
    st.title("Evaluasi Model")

    st.write(
        "Pilih tanggal untuk membandingkan harga aktual dan "
        "prediksi. Metrik evaluasi ditampilkan berdasarkan hasil "
        "pengujian model final terpilih untuk masing-masing horizon."
    )

    # ----------------------------------------------
    # MEMUAT DATA VALIDASI
    # ----------------------------------------------

    @st.cache_data
    def load_validation_data(path_string):
        return pd.read_csv(path_string)

    validation_data = {}
    importance_data = {}

    try:
        for horizon in HORIZONS:

            pred_path = (
                MODEL_DIR / f"validasi_horizon_{horizon}.csv"
            )

            importance_path = (
                MODEL_DIR
                / f"feature_importance_horizon_{horizon}.csv"
            )

            if not pred_path.exists():
                raise FileNotFoundError(
                    f"Data validasi tidak ditemukan: {pred_path}"
                )

            if not importance_path.exists():
                raise FileNotFoundError(
                    f"Feature importance tidak ditemukan: "
                    f"{importance_path}"
                )

            df = load_validation_data(str(pred_path))
            fi = load_validation_data(str(importance_path))

            required_columns = {
                "Tanggal", "Aktual", "Prediksi"
            }

            if not required_columns.issubset(df.columns):
                raise ValueError(
                    f"Kolom CSV validasi horizon {horizon} "
                    "harus mencakup Tanggal, Aktual, dan Prediksi."
                )

            if not {"Fitur", "Importance"}.issubset(fi.columns):
                raise ValueError(
                    f"Kolom feature importance horizon {horizon} "
                    "harus mencakup Fitur dan Importance."
                )

            df["Tanggal"] = pd.to_datetime(
                df["Tanggal"], errors="coerce"
            ).dt.normalize()

            df["Aktual"] = pd.to_numeric(
                df["Aktual"], errors="coerce"
            )

            df["Prediksi"] = pd.to_numeric(
                df["Prediksi"], errors="coerce"
            )

            df = df.dropna(
                subset=["Tanggal", "Aktual", "Prediksi"]
            )

            if df.empty:
                raise ValueError(
                    f"Tidak ada data valid untuk horizon {horizon}."
                )

            if df["Tanggal"].duplicated().any():
                raise ValueError(
                    f"Terdapat tanggal duplikat pada horizon {horizon}."
                )

            if not np.isfinite(
                df[["Aktual", "Prediksi"]].to_numpy()
            ).all():
                raise ValueError(
                    f"Ditemukan angka tidak valid pada horizon {horizon}."
                )

            validation_data[horizon] = df.sort_values(
                "Tanggal"
            ).reset_index(drop=True)

            fi["Importance"] = pd.to_numeric(
                fi["Importance"], errors="coerce"
            )
            fi = fi.dropna(
                subset=["Fitur", "Importance"]
            )

            importance_data[horizon] = fi.sort_values(
                "Importance", ascending=False
            )

    except Exception as e:
        st.error(
            "Data validasi belum siap atau gagal dimuat. "
            "Pastikan file CSV sudah diekspor dari notebook."
        )
        st.exception(e)
        st.stop()

    # ----------------------------------------------
    # PILIH TANGGAL
    # ----------------------------------------------

    tanggal_tersedia = None

    for horizon in HORIZONS:
        tanggal_horizon = set(
            validation_data[horizon]["Tanggal"]
        )

        if tanggal_tersedia is None:
            tanggal_tersedia = tanggal_horizon
        else:
            tanggal_tersedia &= tanggal_horizon

    tanggal_tersedia = sorted(tanggal_tersedia)

    if not tanggal_tersedia:
        st.error(
            "Tidak ada tanggal yang sama pada seluruh data uji. "
            "Periksa kembali penyelarasan tanggal target."
        )
        st.stop()

    tanggal_default = tanggal_tersedia[-1]

    tanggal_pilihan = st.date_input(
        "Tanggal evaluasi",
        value=tanggal_default.date(),
        min_value=tanggal_tersedia[0].date(),
        max_value=tanggal_tersedia[-1].date()
    )

    tanggal_pilihan = pd.Timestamp(
        tanggal_pilihan
    ).normalize()

    # Pastikan tanggal yang dipilih benar-benar tersedia.
    if tanggal_pilihan not in tanggal_tersedia:
        st.warning(
            "Tanggal tersebut tidak tersedia pada seluruh data uji. "
            "Pilih tanggal yang memiliki observasi untuk semua horizon."
        )
        st.stop()

    
    # ----------------------------------------------
    # GRAFIK AKTUAL VS PREDIKSI
    # ----------------------------------------------

    st.divider()
    st.subheader("Perbandingan Harga Aktual dan Prediksi")

    baris_grafik = []

    for horizon in HORIZONS:
        df = validation_data[horizon]

        baris = df.loc[
            df["Tanggal"] == tanggal_pilihan
        ]

        if baris.empty:
            continue

        aktual = float(baris.iloc[0]["Aktual"])
        prediksi = float(baris.iloc[0]["Prediksi"])

        baris_grafik.extend([
            {
                "Horizon": f"H+{horizon}",
                "Jenis": "Harga Aktual",
                "Harga": aktual,
            },
            {
                "Horizon": f"H+{horizon}",
                "Jenis": "Harga Prediksi",
                "Harga": prediksi,
            },
        ])

    df_grafik = pd.DataFrame(baris_grafik)

    fig_perbandingan = px.bar(
        df_grafik,
        x="Horizon",
        y="Harga",
        color="Jenis",
        barmode="group",
        text="Harga",
        title=(
            "Harga Aktual vs Prediksi (USD/ton) — "
            f"{tanggal_pilihan:%d-%m-%Y}"
        ),
        labels={
            "Horizon": "Horizon Prediksi",
            "Harga": "Harga Nikel",
            "Jenis": "Keterangan",
        },
    )

    # Format angka pada label batang: 2 angka desimal
    fig_perbandingan.update_traces(
        texttemplate="%{y:,.2f}",
        textposition="inside",
        hovertemplate=(
            "Keterangan: %{fullData.name}<br>"
            "Horizon Prediksi: %{x}<br>"
            "Harga Nikel: %{y:,.2f}"
            "<extra></extra>"
        ),
    )

    fig_perbandingan.update_layout(
        yaxis=dict(
            title="Harga Nikel",
            tickformat=",.2f",
        ),
        legend_title_text="Keterangan",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F1F6F7"),
    )

    st.plotly_chart(
        fig_perbandingan,
        use_container_width=True,
    )

    # ----------------------------------------------
    # METRIK BERDASARKAN TANGGAL YANG DIPILIH
    # ----------------------------------------------

    st.divider()
    st.subheader("Metrik Evaluasi")

    st.caption(
        "Nilai di bawah dihitung ulang untuk tanggal yang dipilih, "
        "dengan membandingkan harga aktual dan prediksi pada setiap horizon. "
        "Karena hanya satu observasi per horizon yang dibandingkan, "
        "MAE dan RMSE akan sama dengan nilai kesalahan absolut, sedangkan "
        "R² tidak dapat dihitung secara bermakna dari satu observasi."
    )

    hasil_metrik_tanggal = []

    for horizon in HORIZONS:
        df_horizon = validation_data[horizon]
        baris = df_horizon.loc[
            df_horizon["Tanggal"] == tanggal_pilihan
        ]

        if baris.empty:
            continue

        aktual = float(baris.iloc[0]["Aktual"])
        prediksi = float(baris.iloc[0]["Prediksi"])
        error = aktual - prediksi
        error_absolut = abs(error)

        if aktual != 0:
            mape = error_absolut / abs(aktual) * 100
        else:
            mape = np.nan

        hasil_metrik_tanggal.append({
            "Horizon": f"H+{horizon}",
            "Tanggal": tanggal_pilihan.strftime("%d-%m-%Y"),
            "Aktual": aktual,
            "Prediksi": prediksi,
            "Error (Aktual - Prediksi)": error,
            "Absolute Error": error_absolut,
            "MAE": error_absolut,
            "RMSE": error_absolut,
            "MAPE (%)": mape,
            "R²": np.nan,
        })

    df_metrik_tanggal = pd.DataFrame(hasil_metrik_tanggal)

    cols = st.columns(len(HORIZONS))

    for col, horizon in zip(cols, HORIZONS):
        row_df = df_metrik_tanggal.loc[
            df_metrik_tanggal["Horizon"] == f"H+{horizon}"
        ]

        with col:
            st.markdown(f"**Horizon H+{horizon}**")

            if row_df.empty:
                st.warning("Tidak ada data pada tanggal ini.")
                continue

            row = row_df.iloc[0]
            st.metric("Harga Aktual (USD/ton)", f"{row['Aktual']:,.2f}")
            st.metric("Harga Prediksi (USD/ton)", f"{row['Prediksi']:,.2f}")
            st.metric("Absolute Error (USD/ton)", f"{row['Absolute Error']:,.2f}")

    with st.expander("Lihat tabel metrik pada tanggal terpilih"):

        st.dataframe(
            df_metrik_tanggal,
            column_config={
                "Aktual": st.column_config.NumberColumn(
                    "Aktual",
                    format="%.2f",
                ),
                "Prediksi": st.column_config.NumberColumn(
                    "Prediksi",
                    format="%.2f",
                ),
                "Error (Aktual - Prediksi)": st.column_config.NumberColumn(
                    "Error (Aktual - Prediksi)",
                    format="%.2f",
                ),
                "Absolute Error": st.column_config.NumberColumn(
                    "Absolute Error",
                    format="%.2f",
                ),
                "MAE": st.column_config.NumberColumn(
                    "MAE",
                    format="%.2f",
                ),
                "RMSE": st.column_config.NumberColumn(
                    "RMSE",
                    format="%.2f",
                ),
                "MAPE (%)": st.column_config.NumberColumn(
                    "MAPE (%)",
                    format="%.2f",
                ),
                "R²": st.column_config.NumberColumn(
                    "R²",
                    format="%.4f",
                ),
            },
            use_container_width=True,
            hide_index=True,
        )

    # ----------------------------------------------
    # FEATURE IMPORTANCE
    # ----------------------------------------------

    st.divider()
    st.subheader("Feature Importance")

    st.write(
        "Grafik menunjukkan tingkat kepentingan relatif setiap "
        "fitur menurut model final pada masing-masing horizon."
    )

    for horizon in HORIZONS:
        fi = importance_data[horizon].copy()

        fig_importance = px.bar(
            fi,
            x="Importance",
            y="Fitur",
            orientation="h",
            text="Importance",
            title=f"Feature Importance — Horizon H+{horizon}",
            labels={
                "Importance": "Feature Importance",
                "Fitur": "Variabel Prediktor",
            },
        )

        fig_importance.update_traces(
            texttemplate="%{x:.4f}",
            textposition="inside",
            insidetextanchor="end",
            textfont=dict(color="#FFFFFF"),
            hovertemplate=(
                "Feature Importance: %{x:.4f}<br>"
                "Variabel Prediktor: %{y}"
                "<extra></extra>"
            ),
        )

        fig_importance.update_layout(
            yaxis={"categoryorder": "total ascending"},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F1F6F7"),
            margin=dict(r=80),
        )

        st.plotly_chart(
            fig_importance,
            use_container_width=True
        )

    st.caption(
        "Feature importance menunjukkan kontribusi relatif fitur "
        "dalam model, bukan hubungan sebab-akibat."
    )
