import streamlit as st
import pandas as pd

st.title("Simulasi Permintaan acak dengan Metode Monte Carlo")

# ====== Upload Excel ======
uploaded_file = st.file_uploader("Upload file Excel (harus ada kolom 'permintaan')", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    if 'permintaan' not in df.columns:
        st.error("File harus memiliki kolom bernama 'permintaan'.")
    else:
        # Hitung frekuensi
        frekuensi_series = df['permintaan'].value_counts().sort_index()
        permintaan = frekuensi_series.index.tolist()
        frekuensi = frekuensi_series.tolist()
        total_frekuensi = sum(frekuensi)

        # Hitung probabilitas dan kumulatif
        probabilitas = [f / total_frekuensi for f in frekuensi]
        prob_kumulatif = []
        kumulatif_kali_seratus = []
        kumulatif = 0
        for p in probabilitas:
            kumulatif += p
            prob_kumulatif.append(round(kumulatif, 2))
            kumulatif_kali_seratus.append(round(kumulatif * 100))

        # Rentang angka acak
        rentang = []
        awal = 0
        for nilai in kumulatif_kali_seratus:
            akhir = nilai
            rentang.append((awal, akhir))
            awal = nilai + 1

        # Tampilkan Tabel Distribusi
        st.subheader("Tabel Distribusi Permintaan")
        distribusi_df = pd.DataFrame({
            'Permintaan': permintaan,
            'Frekuensi': frekuensi,
            'Probabilitas': [round(p, 2) for p in probabilitas],
            'Prob Kumulatif': prob_kumulatif,
            'Kumulatif*100': kumulatif_kali_seratus,
            'Rentang': [f"{start:02d}-{end:02d}" for start, end in rentang]
        })
        st.dataframe(distribusi_df)

        # Input jumlah simulasi & angka acak
        st.subheader("Simulasi Monte Carlo")
        jumlah_simulasi = st.number_input("Berapa hari ingin disimulasikan?", min_value=1, value=5, step=1)

        angka_acak_input = st.text_input(
            f"Masukkan {jumlah_simulasi} angka acak (0–99) dipisahkan koma",
            placeholder="Contoh: 12,45,30,88,3"
        )

        if angka_acak_input:
            try:
                angka_acak = [int(x.strip()) for x in angka_acak_input.split(",")]
                if len(angka_acak) != jumlah_simulasi:
                    st.warning(f"Jumlah angka acak harus sebanyak {jumlah_simulasi}.")
                else:
                    # Simulasi Monte Carlo
                    hasil_simulasi = []
                    hasil_tabel = []
                    for hari, acak in enumerate(angka_acak, 1):
                        for i, (start, end) in enumerate(rentang):
                            if start <= acak <= end:
                                prediksi = permintaan[i]
                                hasil_simulasi.append(prediksi)
                                hasil_tabel.append((hari, acak, prediksi))
                                break

                    # Tampilkan hasil simulasi
                    st.markdown("### Hasil Simulasi:")
                    hasil_df = pd.DataFrame(hasil_tabel, columns=["Hari", "Angka Acak", "Permintaan"])
                    st.dataframe(hasil_df)

                    # Tampilkan rata-rata
                    rata_rata = sum(hasil_simulasi) / jumlah_simulasi
                    st.success(f"Rata-rata permintaan hasil simulasi: {rata_rata:.2f}")
            except:
                st.error("Format angka acak salah. Pastikan hanya angka dipisahkan koma.")
