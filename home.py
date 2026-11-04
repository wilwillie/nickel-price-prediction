import streamlit as st
from shared import HORIZONS, load_company_image, load_nickel_image


def render():
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
    # JENIS BIJIH NIKEL
    # --------------------------------------------------

    st.subheader("⛏️ Mengenal Jenis Bijih Nikel")

    st.markdown("""
    Nikel yang ditambang umumnya berasal dari dua tipe endapan bijih:
    **sulfida magmatik** dan **laterit**. Perbedaannya terutama terletak
    pada proses pembentukan, mineral pembawa nikel, serta kondisi
    geologinya.
    """)

    col_sulfida, col_laterit = st.columns(2)

    with col_sulfida:
        st.markdown("### Bijih Sulfida Magmatik")
        st.image(
            load_nickel_image("Pentlandite-120151.jpg"),
            caption="Contoh mineral pentlandit dari Sudbury, Kanada.",
            use_container_width=True
        )
        st.markdown("""
        Mineral utama pembawa nikelnya adalah **pentlandit**
        ((Ni,Fe)₉S₈). Endapan ini terbentuk dari proses magmatik dan
        umumnya berasosiasi dengan batuan kaya magnesium dan besi
        (ultramafik); sebagian endapannya berada jauh di bawah permukaan.
        """)

    with col_laterit:
        st.markdown("### Bijih Laterit")
        st.image(
            load_nickel_image("Nickel_limonite_laterite.jpg"),
            caption="Limonit bernikel di bawah lapisan laterit.",
            use_container_width=True
        )
        st.markdown("""
        Endapan ini terbentuk ketika batuan ultramafik mengalami
        pelapukan intensif, sehingga umumnya ditemukan dekat permukaan.
        Mineral pembawa nikelnya antara lain **limonit bernikel**
        ((Fe,Ni)O(OH)) dan **garnierit** (silikat nikel terhidrasi).
        Ketebalan serta komposisi lapisan bijih dapat berbeda antar lokasi.
        """)

    st.divider()

    # --------------------------------------------------
    # PERUSAHAAN DALAM RANTAI PASOK BIJIH NIKEL
    # --------------------------------------------------

    st.subheader("🏭 Perusahaan dalam Rantai Pasok Bijih Nikel Indonesia")

    st.markdown("""
    Berikut beberapa contoh perusahaan yang bergerak di pertambangan
    atau pengolahan nikel di Indonesia. Perusahaan-perusahaan ini tidak
    semuanya merupakan distributor independen: bijih dapat dipasok ke
    fasilitas pengolahan sendiri maupun melalui kerja sama dan kontrak.
    """)

    perusahaan_nikel = [
        {
            "nama": "PT ANTAM Tbk",
            "gambar": "antam.png",
            "deskripsi": (
                "Perusahaan pertambangan milik negara dengan kegiatan "
                "usaha di sektor nikel, termasuk pertambangan dan "
                "pengolahan. Ketersediaan serta penjualan bijih mengikuti "
                "kegiatan operasional dan ketentuan yang berlaku."
            ),
        },
        {
            "nama": "PT Vale Indonesia Tbk",
            "gambar": "vale.png",
            "deskripsi": (
                "Perusahaan pertambangan nikel yang beroperasi di "
                "Indonesia. Kegiatannya mencakup penambangan bijih dan "
                "pengolahan nikel; tidak semua bijihnya dipasarkan sebagai "
                "produk untuk pembeli umum."
            ),
        },
        {
            "nama": "Harita Nickel (PT Trimegah Bangun Persada Tbk)",
            "gambar": "harita_logo.png",
            "deskripsi": (
                "Perusahaan nikel terintegrasi yang mencantumkan bijih "
                "saprolit dan limonit sebagai produknya, selain produk "
                "hasil pengolahan."
            ),
        },
    ]

    kolom_perusahaan = st.columns(3, gap="large")

    for kolom, perusahaan in zip(kolom_perusahaan, perusahaan_nikel):
        with kolom:
            st.image(
                load_company_image(perusahaan["gambar"]),
                width=250
            )
            
            st.markdown(f"### {perusahaan['nama']}")
            st.write(perusahaan["deskripsi"])

    st.caption(
        "Contoh di atas bukan daftar lengkap. Status operasi, izin, "
        "spesifikasi bijih, dan mekanisme penjualan dapat berubah; "
        "konfirmasi informasi terbaru langsung ke perusahaan terkait."
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
