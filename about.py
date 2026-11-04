import streamlit as st

from shared import load_circular_portrait


def render():
    st.title("Tentang Aplikasi")

    st.markdown(
        "Aplikasi web untuk menghasilkan estimasi harga nikel dunia "
        "menggunakan model **CatBoost Regressor**."
    )

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

    st.subheader("Dosen Pembimbing")

    pembimbing_utama, pembimbing_kedua = st.columns(2, gap="large")

    with pembimbing_utama:
        st.image(
            load_circular_portrait("tri_sutrisno.jpg"),
            width=220
        )
        st.markdown("**Tri Sutrisno, S.Si., M.Sc.**")
        st.caption("Dosen Pembimbing Utama")

    with pembimbing_kedua:
        st.image(
            load_circular_portrait("novario_jp.jpg"),
            width=220
        )
        st.markdown("**Novario Jaya Perdana, S.Kom., M.T.**")
        st.caption("Dosen Pembimbing Kedua")

    st.divider()

    st.info(
        "Hasil yang ditampilkan merupakan estimasi model berdasarkan "
        "data input, bukan jaminan harga pasar di masa depan."
    )