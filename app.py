
from datetime import date
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px


# ==================================================
# KONFIGURASI APLIKASI
# ==================================================

st.set_page_config(
    page_title="Prediksi Harga Nikel Dunia",
    page_icon="📈",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent

MODEL_DIR = (
    BASE_DIR
    / "hasil_tuning"
    / "evaluasi_final"
)

FEATURES = [
    "LME Nickel stock",
    "LME Aluminium Price",
    "LME Copper Price",
    "LME Zinc Price",
    "Iron Ore Price",
    "Dollar Index",
    "WTI Price",
    "LME Nickel Price Lag 1",
    "LME Nickel Price Lag 2",
    "LME Nickel Price Lag 3",
]

HORIZONS = [1, 2, 3, 4, 5]

MODEL_FILES = {
    1: MODEL_DIR / "model_final_horizon_1.joblib",
    2: MODEL_DIR / "model_final_horizon_2.joblib",
    3: MODEL_DIR / "model_final_horizon_3.joblib",
    4: MODEL_DIR / "model_final_horizon_4.joblib",
    5: MODEL_DIR / "model_final_horizon_5.joblib",
}

EVALUATION = pd.DataFrame({
    "Horizon (hari)": [1, 2, 3, 4, 5],
    "Skema": ["80:20", "80:20", "80:20", "80:20", "80:20"],
    "Jumlah Data Uji": [595, 595, 594, 594, 594],
    "MAE": [
        536.3788, 662.3807, 827.8417, 929.6537, 949.3268
    ],
    "RMSE": [
        633.8613, 826.1914, 989.3937, 1137.2799, 1092.9267
    ],
    "MAPE (%)": [
        3.3708, 4.0928, 5.1143, 5.6962, 5.9050
    ],
    "R2": [
        0.6975, 0.4861, 0.2605, 0.0229, 0.0976
    ],
})


# ==================================================
# MEMUAT MODEL
# ==================================================

@st.cache_resource
def load_model(path_string):
    return joblib.load(path_string)


# ==================================================
# MEMUAT MODEL
# ==================================================

st.markdown("""
<style>
/* ==================================================
   TEMA NIKEL — DARK METALLIC TEAL
   ================================================== */

:root {
    --nickel-dark: #101B21;
    --nickel-panel: #172A32;
    --nickel-teal: #245563;
    --nickel-accent: #69C2C7;
    --nickel-silver: #D9E4E7;
    --nickel-text: #F1F6F7;
    --nickel-muted: #AFC3C8;
    --nickel-border: rgba(190, 220, 224, 0.25);
}

/* Background utama */
.stApp,
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(
            circle at 85% 5%,
            rgba(105, 194, 199, 0.16),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #101B21 0%,
            #172A32 48%,
            #245563 100%
        ) !important;
    color: var(--nickel-text);
}

header[data-testid="stHeader"] {
    display: none !important;
}

div[data-testid="stToolbar"] {
    background: transparent !important;
}

/* Area konten */
.block-container {
    max-width: 1450px;
    padding-top: 1.5rem !important;
    padding-bottom: 3rem;
}

/* Navbar desktop */
.st-key-desktop_nav {
    display: block !important;
    margin-bottom: 2rem;
}

/* Desktop */
.st-key-mobile_nav {
    display: none !important;
}

@media (max-width: 768px) {
    .st-key-desktop_nav {
        display: none !important;
    }

    .st-key-mobile_nav {
        display: block !important;
        position: fixed !important;
        top: 2.7rem !important;
        right: 1rem !important;
        width: 56px !important;
        height: 52px !important;
        z-index: 999999 !important;
    }

    /* Tombol hamburger */
    .st-key-mobile_nav [data-testid="stPopover"] button {
        position: relative !important;
        width: 56px !important;
        height: 52px !important;
        min-width: 56px !important;
        padding: 0 !important;
        margin: 0 !important;
        font-size: 0 !important;
        line-height: 0 !important;
        color: transparent !important;
        text-indent: -9999px !important;
        background-color: #245563 !important;
        background-image:
            linear-gradient(#FFFFFF, #FFFFFF),
            linear-gradient(#FFFFFF, #FFFFFF),
            linear-gradient(#FFFFFF, #FFFFFF) !important;
        background-repeat: no-repeat !important;
        background-size: 30px 4px !important;
        background-position:
            center 14px,
            center 24px,
            center 34px !important;
        border: 1px solid #69C2C7 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }

    /* Hilangkan seluruh isi tombol bawaan Streamlit */
    .st-key-mobile_nav [data-testid="stPopover"] button svg,
    .st-key-mobile_nav [data-testid="stPopover"] button span,
    .st-key-mobile_nav [data-testid="stPopover"] button div,
    .st-key-mobile_nav [data-testid="stPopover"] button::before,
    .st-key-mobile_nav [data-testid="stPopover"] button::after {
        display: none !important;
        visibility: hidden !important;
        content: none !important;
    }

    /* Pastikan tiga garis tetap tampil */
    .st-key-mobile_nav [data-testid="stPopover"] button {
        background-image:
            linear-gradient(#FFFFFF, #FFFFFF),
            linear-gradient(#FFFFFF, #FFFFFF),
            linear-gradient(#FFFFFF, #FFFFFF) !important;
    }

    .st-key-mobile_nav [data-testid="stPopover"] button:hover,
    .st-key-mobile_nav [data-testid="stPopover"] button[aria-expanded="true"] {
        background-color: #69C2C7 !important;
        background-image:
            linear-gradient(#101B21, #101B21),
            linear-gradient(#101B21, #101B21),
            linear-gradient(#101B21, #101B21) !important;
    }

    .st-key-mobile_nav [data-baseweb="popover"] {
        z-index: 1000000 !important;
    }

    .block-container h1 {
        padding-right: 4.5rem !important;
        line-height: 1.2 !important;
    }

    .block-container {
        padding: 1.2rem 1rem 2rem !important;
    }
}

/* Tipografi */
h1, h2, h3, h4 {
    color: var(--nickel-silver) !important;
    font-weight: 700 !important;
    letter-spacing: 0.2px;
}

h1 {
    border-left: 6px solid var(--nickel-accent);
    padding-left: 12px !important;
    margin-bottom: 2.5rem !important;
}

p, li, label, .stMarkdown {
    color: var(--nickel-text);
}

.stCaption,
[data-testid="stCaptionContainer"] {
    color: var(--nickel-muted) !important;
}

/* Hilangkan sidebar bawaan */
section[data-testid="stSidebar"] {
    display: none !important;
}

/* Navigasi */
div[role="radiogroup"] label {
    background: rgba(255, 255, 255, 0.055);
    border: 1px solid transparent;
    border-radius: 9px;
    margin-bottom: 7px;
    padding: 9px 12px;
    transition: all 0.2s ease;
}

div[role="radiogroup"] label:hover {
    background: rgba(105, 194, 199, 0.18);
    border-color: rgba(105, 194, 199, 0.4);
}

/* Kartu metric */
div[data-testid="stMetric"] {
    min-width: 0 !important;
    overflow: visible !important;
    background: linear-gradient(
        145deg,
        rgba(255, 255, 255, 0.13),
        rgba(255, 255, 255, 0.045)
    ) !important;
    border: 1px solid var(--nickel-border);
    border-left: 4px solid var(--nickel-accent);
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0 7px 18px rgba(0, 0, 0, 0.22);
}

div[data-testid="stMetricLabel"] {
    color: var(--nickel-muted) !important;
    font-size: 0.82rem !important;
    white-space: normal !important;
    overflow: visible !important;
}

div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] > div {
    color: #FFFFFF !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    line-height: 1.35 !important;
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: clip !important;
    word-break: break-word !important;
}

/* Input, select, date input */
div[data-baseweb="input"],
div[data-baseweb="select"] > div,
[data-testid="stDateInput"] input {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 1px solid var(--nickel-border) !important;
    border-radius: 8px !important;
    color: #FFFFFF !important;
}

div[data-baseweb="input"]:focus-within,
div[data-baseweb="select"] > div:focus-within {
    border-color: var(--nickel-accent) !important;
    box-shadow: 0 0 0 1px var(--nickel-accent) !important;
}

input,
textarea {
    color: #FFFFFF !important;
}

/* Tombol */
.stButton > button {
    width: 100%;
    min-height: 42px;
    background: linear-gradient(
        135deg,
        #245563,
        #69C2C7
    ) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 9px;
    font-weight: 700;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(
        135deg,
        #69C2C7,
        #B1EBEC
    ) !important;
    color: #102027 !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
}

/* Expander */
details {
    background: rgba(255, 255, 255, 0.055) !important;
    border: 1px solid var(--nickel-border) !important;
    border-radius: 10px !important;
    margin-bottom: 10px;
}

details summary {
    color: var(--nickel-silver) !important;
    font-weight: 600;
}

/* Alert */
div[data-testid="stAlert"] {
    border-radius: 10px;
    border-left: 5px solid var(--nickel-accent);
}

/* Grafik dan tabel transparan */
div[data-testid="stPlotlyChart"],
div[data-testid="stArrowVegaLiteChart"],
div[data-testid="stDataFrame"],
div[data-testid="stTable"],
div[data-testid="stTable"] > div {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* Hilangkan background internal tabel */
div[data-testid="stDataFrame"] > div,
div[data-testid="stDataFrame"] [data-testid="stDataFrameResizable"],
div[data-testid="stDataFrame"] iframe {
    background: transparent !important;
    border: none !important;
}

/* Tabel HTML */
div[data-testid="stTable"] table {
    background: transparent !important;
    color: #F1F6F7 !important;
}

div[data-testid="stTable"] thead tr {
    background: rgba(105, 194, 199, 0.18) !important;
}

div[data-testid="stTable"] tbody tr {
    background: transparent !important;
}

div[data-testid="stTable"] th,
div[data-testid="stTable"] td {
    background: transparent !important;
    color: #F1F6F7 !important;
    border-color: var(--nickel-border) !important;
}

/* Garis pemisah */
hr {
    border-color: var(--nickel-border) !important;
}

/* Tooltip bantuan */
[data-testid="stTooltipIcon"] {
    color: var(--nickel-accent) !important;
}

/* Responsif */
@media (max-width: 768px) {
    .block-container {
        padding: 1.2rem 1rem 2rem;
    }

    div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] > div {
        font-size: 0.95rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# NAVBAR RESPONSIVE
# ==================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "menu_version" not in st.session_state:
    st.session_state.menu_version = 0


def go_to_page(page_name):
    st.session_state.page = page_name
    st.session_state.menu_version += 1
    st.rerun()

with st.container(key="desktop_nav"):
    nav_spacer, nav_home, nav_prediction, nav_validation, nav_help, nav_about = st.columns(
        [3.5, 1, 1.35, 1.2, 0.8, 0.8]
    )

    with nav_home:
        if st.button("Home", key="desktop_home", use_container_width=True):
            go_to_page("Home")

    with nav_prediction:
        if st.button("Prediction", key="desktop_prediction", use_container_width=True):
            go_to_page("Prediction")

    with nav_validation:
        if st.button("Validation", key="desktop_validation", use_container_width=True):
            go_to_page("Validation")

    with nav_help:
        if st.button("Help", key="desktop_help", use_container_width=True):
            go_to_page("Help")

    with nav_about:
        if st.button("About", key="desktop_about", use_container_width=True):
            go_to_page("About")

# Hamburger mobile
with st.container(key="mobile_nav"):
    with st.popover(
        "☰",
        key=f"mobile_menu_{st.session_state.menu_version}"
    ):
        st.markdown("### Menu")

        if st.button("Home", key="mobile_home", use_container_width=True):
            go_to_page("Home")

        if st.button(
            "Prediction",
            key="mobile_prediction",
            use_container_width=True
        ):
            go_to_page("Prediction")

        if st.button(
            "Validation",
            key="mobile_validation",
            use_container_width=True
        ):
            go_to_page("Validation")

        if st.button("Help", key="mobile_help", use_container_width=True):
            go_to_page("Help")

        if st.button("About", key="mobile_about", use_container_width=True):
            go_to_page("About")


page = st.session_state.page


# ==================================================
# HOME
# ==================================================

if page == "Home":

    st.title("🌍 Analisis Harga Nikel Dunia")

    st.markdown("""
    Aplikasi ini menggunakan algoritma **CatBoost Regressor** untuk
    memprediksi harga nikel dunia berdasarkan 10 variabel prediktor,
    yang terdiri dari 7 variabel eksternal dan 3 variabel historis
    harga nikel.

    Variabel-variabel tersebut merepresentasikan kondisi persediaan
    nikel, pergerakan pasar logam industri, kondisi ekonomi global,
    serta pola harga nikel pada periode sebelumnya.
    """)

    st.divider()

    # --------------------------------------------------
    # HORIZON PREDIKSI
    # --------------------------------------------------

    st.subheader("🎯 Horizon Prediksi")

    st.write(
        "Model menghasilkan estimasi harga nikel untuk lima "
        "horizon waktu yang berbeda."
    )

    cols = st.columns(5)

    for col, horizon in zip(cols, HORIZONS):
        with col:
            st.metric(
                label=f"Horizon H+{horizon}",
                value=f"{horizon} hari"
            )

    st.info(
        "Buka halaman Prediction untuk memasukkan data prediktor "
        "dan memperoleh estimasi harga nikel untuk horizon 1–5 hari."
    )

    st.divider()

    # --------------------------------------------------
    # PENJELASAN VARIABEL PREDIKTOR
    # --------------------------------------------------

    st.subheader("📊 Faktor-Faktor yang Berkaitan dengan Harga Nikel")

    st.markdown("""
    Harga nikel dunia dapat bergerak mengikuti perubahan kondisi
    penawaran dan permintaan, aktivitas industri, kondisi ekonomi
    global, serta pergerakan harga pada periode sebelumnya.

    Berikut penjelasan 10 variabel yang digunakan sebagai input model.
    """)

    # --------------------------------------------------
    # KELOMPOK 1: VARIABEL EKSTERNAL
    # --------------------------------------------------

    st.markdown("### A. Variabel Eksternal")

    st.caption(
        "Tujuh variabel yang menggambarkan kondisi pasar komoditas "
        "dan ekonomi global."
    )

    faktor_eksternal = [
        {
            "nama": "1. LME Nickel Stock",
            "kategori": "Persediaan nikel",
            "hubungan": (
                "Persediaan nikel di London Metal Exchange (LME) "
                "menggambarkan jumlah stok nikel yang tercatat di "
                "gudang dalam sistem bursa tersebut."
            ),
            "mekanisme": (
                "Peningkatan stok dapat mengindikasikan ketersediaan "
                "pasokan yang lebih besar dibandingkan kebutuhan pasar "
                "sehingga berpotensi menekan harga. Sebaliknya, penurunan "
                "stok dapat mengindikasikan pengetatan pasokan dan "
                "berpotensi mendukung kenaikan harga."
            ),
            "catatan": (
                "Stok LME bukan keseluruhan persediaan nikel dunia. "
                "Pergerakannya perlu dipahami bersama kondisi produksi, "
                "permintaan, dan persediaan di luar bursa."
            )
        },
        {
            "nama": "2. LME Aluminium Price",
            "kategori": "Harga logam industri",
            "hubungan": (
                "Harga aluminium dapat mencerminkan perubahan kondisi "
                "pasar logam industri dan aktivitas ekonomi."
            ),
            "mekanisme": (
                "Ketika aktivitas manufaktur dan permintaan logam "
                "meningkat, harga aluminium dan nikel berpotensi "
                "bergerak searah. Namun, keduanya memiliki struktur "
                "pasokan, penggunaan, dan faktor pasar yang berbeda."
            ),
            "catatan": (
                "Hubungan ini merupakan kemungkinan berdasarkan kondisi "
                "pasar industri, bukan jaminan bahwa kenaikan aluminium "
                "selalu diikuti kenaikan nikel."
            )
        },
        {
            "nama": "3. LME Copper Price",
            "kategori": "Harga logam industri",
            "hubungan": (
                "Harga tembaga dapat menjadi indikator tambahan "
                "untuk memahami sentimen pasar logam industri."
            ),
            "mekanisme": (
                "Tembaga banyak digunakan dalam aktivitas konstruksi, "
                "kelistrikan, dan manufaktur. Peningkatan permintaan "
                "industri dapat mendukung harga tembaga sekaligus "
                "meningkatkan optimisme terhadap permintaan komoditas "
                "lain, termasuk nikel."
            ),
            "catatan": (
                "Pergerakan harga tembaga tidak selalu searah dengan "
                "nikel karena karakteristik permintaan dan pasokannya "
                "berbeda."
            )
        },
        {
            "nama": "4. LME Zinc Price",
            "kategori": "Harga logam industri",
            "hubungan": (
                "Harga seng dapat memberikan informasi mengenai kondisi "
                "pasar logam dasar dan aktivitas industri global."
            ),
            "mekanisme": (
                "Perubahan permintaan manufaktur, konstruksi, dan "
                "persediaan logam dapat memengaruhi harga seng. "
                "Sebagian kondisi makroekonomi yang memengaruhi seng "
                "juga dapat berkaitan dengan permintaan nikel."
            ),
            "catatan": (
                "Hubungan dengan harga nikel bersifat tidak langsung "
                "dan dapat berubah mengikuti kondisi pasar."
            )
        },
        {
            "nama": "5. Iron Ore Price",
            "kategori": "Harga bahan baku industri baja",
            "hubungan": (
                "Harga bijih besi berkaitan dengan pasar bahan baku "
                "produksi besi dan baja."
            ),
            "mekanisme": (
                "Nikel banyak digunakan dalam produksi baja tahan karat "
                "(stainless steel). Perubahan aktivitas produksi baja "
                "dapat berkaitan dengan permintaan bijih besi dan nikel, "
                "sehingga harga bijih besi berpotensi memberikan sinyal "
                "mengenai kondisi industri baja."
            ),
            "catatan": (
                "Bijih besi dan nikel bukan bahan baku yang saling "
                "menggantikan secara langsung. Harga bijih besi juga "
                "dipengaruhi oleh faktor pasokan dan permintaan tersendiri."
            )
        },
        {
            "nama": "6. Dollar Index",
            "kategori": "Indikator ekonomi dan nilai tukar",
            "hubungan": (
                "Dollar Index mengukur kekuatan dolar AS terhadap "
                "sekelompok mata uang utama."
            ),
            "mekanisme": (
                "Harga komoditas internasional umumnya dinyatakan "
                "dalam dolar AS. Penguatan dolar dapat membuat komoditas "
                "lebih mahal bagi pembeli yang menggunakan mata uang "
                "lain dan berpotensi menekan permintaan. Pelemahan dolar "
                "dapat memberikan efek sebaliknya."
            ),
            "catatan": (
                "Hubungan tersebut tidak selalu berlaku. Kondisi ekonomi "
                "global, suku bunga, dan perubahan permintaan komoditas "
                "dapat memengaruhi hubungan dolar dengan harga nikel."
            )
        },
        {
            "nama": "7. WTI Price",
            "kategori": "Harga minyak dan energi",
            "hubungan": (
                "West Texas Intermediate (WTI) merupakan salah satu "
                "acuan harga minyak mentah."
            ),
            "mekanisme": (
                "Harga minyak berkaitan dengan biaya energi dan "
                "transportasi yang digunakan dalam kegiatan pertambangan, "
                "pengolahan, serta distribusi logam. Perubahan harga "
                "minyak juga dapat mencerminkan kondisi ekonomi dan "
                "permintaan energi global."
            ),
            "catatan": (
                "Kenaikan WTI dapat meningkatkan sebagian biaya produksi, "
                "tetapi dampak akhirnya terhadap harga nikel bergantung "
                "pada kondisi penawaran, permintaan, dan faktor lainnya."
            )
        }
    ]

    for faktor in faktor_eksternal:
        with st.expander(
            f"{faktor['nama']} — {faktor['kategori']}"
        ):
            st.markdown("**Penjelasan variabel**")
            st.write(faktor["hubungan"])

            st.markdown("**Mekanisme hubungan dengan harga nikel**")
            st.write(faktor["mekanisme"])

            st.caption(faktor["catatan"])

    # --------------------------------------------------
    # KELOMPOK 2: VARIABEL HISTORIS NIKEL
    # --------------------------------------------------

    st.markdown("### B. Variabel Historis Harga Nikel")

    st.caption(
        "Tiga variabel lag digunakan untuk menangkap informasi "
        "dari harga nikel pada periode sebelumnya."
    )

    faktor_lag = [
        {
            "nama": "8. LME Nickel Price Lag 1",
            "kategori": "Harga nikel periode sebelumnya",
            "hubungan": (
                "LME Nickel Price Lag 1 merupakan harga nikel pada satu "
                "periode observasi sebelumnya."
            ),
            "mekanisme": (
                "Harga nikel saat ini dapat berkaitan erat dengan "
                "harga pada periode sebelumnya karena penyesuaian "
                "harga pasar tidak selalu terjadi sekaligus. Variabel "
                "ini membantu model mengenali kesinambungan pergerakan "
                "harga jangka pendek."
            )
        },
        {
            "nama": "9. LME Nickel Price Lag 2",
            "kategori": "Harga nikel dua periode sebelumnya",
            "hubungan": (
                "LME Nickel Price Lag 2 merupakan harga nikel pada dua "
                "periode observasi sebelumnya."
            ),
            "mekanisme": (
                "Variabel ini memberikan konteks tambahan mengenai "
                "arah dan pola pergerakan harga sebelum periode "
                "terakhir. Model dapat mempelajari apakah informasi "
                "tersebut membantu memperkirakan harga pada horizon "
                "prediksi."
            )
        },
        {
            "nama": "10. LME Nickel Price Lag 3",
            "kategori": "Harga nikel tiga periode sebelumnya",
            "hubungan": (
                "LME Nickel Price Lag 3 merupakan harga nikel pada tiga "
                "periode observasi sebelumnya."
            ),
            "mekanisme": (
                "Variabel ini memperluas informasi historis yang "
                "tersedia bagi model. Bersama dua variabel lag lainnya, "
                "fitur ini dapat membantu menangkap pola perubahan "
                "harga jangka pendek yang mungkin tidak terlihat "
                "dari satu periode sebelumnya saja."
            )
        }
    ]

    for faktor in faktor_lag:
        with st.expander(
            f"{faktor['nama']} — {faktor['kategori']}"
        ):
            st.markdown("**Penjelasan variabel**")
            st.write(faktor["hubungan"])

            st.markdown("**Mekanisme hubungan dengan harga nikel**")
            st.write(faktor["mekanisme"])

    st.divider()

    # --------------------------------------------------
    # INTERPRETASI HUBUNGAN VARIABEL
    # --------------------------------------------------

    st.subheader("🔎 Bagaimana Model Menggunakan Variabel Ini?")

    st.markdown("""
    CatBoost Regressor mempelajari pola hubungan antara variabel
    prediktor dan harga nikel dari data historis yang digunakan
    selama pelatihan. Model dapat menangkap hubungan nonlinier
    serta interaksi antarvariabel.

    Karena itu, pengaruh suatu variabel tidak harus selalu positif
    atau negatif pada semua kondisi. Hubungannya dapat berubah
    bergantung pada nilai variabel lain dan kondisi pasar.
    """)

    st.warning("""
    **Penting:** penjelasan di atas menggambarkan mekanisme ekonomi
    yang mungkin menghubungkan variabel dengan harga nikel, bukan
    hasil pembuktian kausal dari model. Untuk mengetahui variabel
    mana yang paling berkontribusi pada model final, gunakan hasil
    Feature Importance pada halaman Validation. Feature Importance
    juga tidak dengan sendirinya membuktikan arah pengaruh atau
    hubungan sebab-akibat.
    """)

    st.divider()

    # --------------------------------------------------
    # INFORMASI PENGGUNAAN
    # --------------------------------------------------

    st.subheader("🚀 Mulai Prediksi")

    st.write("""
    Untuk memperoleh estimasi harga nikel:

    1. Buka halaman **Prediction**.
    2. Masukkan tujuh variabel eksternal dan tiga variabel historis.
    3. Pastikan data menggunakan satuan dan definisi yang sesuai
       dengan data yang digunakan saat pelatihan model.
    4. Jalankan prediksi untuk melihat estimasi horizon 1–5 hari.
    """)

    st.caption(
        "Hasil prediksi merupakan estimasi berdasarkan model dan "
        "input yang diberikan, bukan jaminan harga pasar di masa depan."
    )



# ==================================================
# PREDICTION
# ==================================================

elif page == "Prediction":
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
        - Ambil nilai pada kolom **LME Nickel stock**.
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
            "LME Nickel stock": nickel_stock,
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


# ==================================================
# VALIDATION
# ==================================================

elif page == "Validation":
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
    
# ==================================================
# HELP
# ==================================================

elif page == "Help":
    st.title("Panduan Penggunaan")

    st.markdown("""
    Aplikasi ini merupakan purwarupa sistem untuk menghasilkan
    prediksi harga nikel dunia dalam jangka pendek menggunakan
    **CatBoost Regressor**. Model memanfaatkan data historis harga
    nikel dan variabel eksternal sebagai prediktor.

    Tata cara pengoperasian aplikasi dapat dibaca melalui buku manual
    yang tersedia di bawah ini.
    """)

    manual_files = list(BASE_DIR.glob("Manual_Book.*"))

    if manual_files:
        manual_path = manual_files[0]
        mime_type = (
            "application/pdf"
            if manual_path.suffix.lower() == ".pdf"
            else "application/octet-stream"
        )

        st.download_button(
            label="📥 Unduh Buku Manual",
            data=manual_path.read_bytes(),
            file_name=manual_path.name,
            mime=mime_type,
            use_container_width=True,
        )
    else:
        st.error(
            "File Manual_Book tidak ditemukan. "
            "Pastikan file berada di folder app."
        )


# ==================================================
# ABOUT
# ==================================================

elif page == "About":
    st.title("Tentang Aplikasi")

    st.markdown(
        "Aplikasi web untuk menghasilkan estimasi harga nikel dunia "
        "menggunakan model **CatBoost Regressor**."
    )

    st.divider()

    info_col, perancang_col = st.columns([1.5, 1], gap="large")

    with info_col:
        st.subheader("Tentang Proyek")
        st.markdown(
            """
            **Judul skripsi**

            *Perancangan Aplikasi Web Prediksi Harga Nikel Dunia
            Menggunakan CatBoost Regressor*

            Aplikasi ini menggunakan tujuh variabel eksternal dan
            tiga fitur historis harga nikel untuk menghasilkan prediksi
            pada horizon **H+1 hingga H+5**.
            """
        )

    with perancang_col:
        st.subheader("Perancang")
        st.markdown(
            """
            **William Wenstein**<br>
            Mahasiswa Teknik Informatika<br>
            Fakultas Teknologi Informasi<br>
            Universitas Tarumanagara<br>
            Angkatan 2023<br><br>
            [📩 wensteinwilliam@gmail.com](mailto:wensteinwilliam@gmail.com)<br>
            [🔗 Kunjungi profil LinkedIn](https://www.linkedin.com/in/william-wenstein/)
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    st.info(
        "Hasil yang ditampilkan merupakan estimasi model berdasarkan "
        "data input, bukan jaminan harga pasar di masa depan."
    )