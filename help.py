import streamlit as st

from shared import BASE_DIR


def render():
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
