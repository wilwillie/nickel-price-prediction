import streamlit as st

# ==================================================
# KONFIGURASI APLIKASI
# ==================================================

st.set_page_config(
    page_title="Prediksi Harga Nikel Dunia",
    page_icon="📈",
    layout="wide"
)


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
    padding-top: 6.5rem !important;
    padding-bottom: 3rem;
}

/* Navbar desktop */
.st-key-desktop_nav {
    display: block !important;
    position: fixed !important;
    top: 40px !important;
    right: 5rem !important;
    box-sizing: border-box;
    z-index: 999999 !important;
    padding: 0.5rem 1rem !important;
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

    /* menghilangkan seluruh isi tombol bawaan Streamlit */
    .st-key-mobile_nav [data-testid="stPopover"] button svg,
    .st-key-mobile_nav [data-testid="stPopover"] button span,
    .st-key-mobile_nav [data-testid="stPopover"] button div,
    .st-key-mobile_nav [data-testid="stPopover"] button::before,
    .st-key-mobile_nav [data-testid="stPopover"] button::after {
        display: none !important;
        visibility: hidden !important;
        content: none !important;
    }

    /* memastikan tiga garis tetap tampil */
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


# ==================================================
# RENDER HALAMAN
# ==================================================

page = st.session_state.page

if page == "Home":
    from home import render
elif page == "Prediction":
    from prediction import render
elif page == "Validation":
    from validation import render
elif page == "Help":
    from help import render
elif page == "About":
    from about import render
else:
    render = None

if render is not None:
    render()
