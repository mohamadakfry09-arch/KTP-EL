import pandas as pd

# Load cleaned data
df = pd.read_csv('KTP.csv')

total_wktp = int(df['WKTP'].sum())
total_ktp = int(df['KTP'].sum())
total_blmktp = int(df['BLMKTP'].sum())
total_blm_rekam = int(df['BLM_REKAM'].sum())
total_rekam = total_wktp - total_blm_rekam
total_lk = int(df['KTP_LK'].sum())
total_pr = int(df['KTP_PR'].sum())
total_blm_lk = int(df['BLM_KTP_LK'].sum())
total_blm_pr = int(df['BLM_KTP_PR'].sum())

persen_kepemilikan = (total_ktp / total_wktp) * 100
persen_belum_ktp = (total_blmktp / total_wktp) * 100
persen_rekam = (total_rekam / total_wktp) * 100
persen_belum_rekam = (total_blm_rekam / total_wktp) * 100

tertinggi = df.loc[df['PERSEN_KTP'].idxmax()]
terendah = df.loc[df['PERSEN_KTP'].idxmin()]

fmt_num = lambda x: f"{x:,.0f}".replace(",", ".")

table_rows = []
for idx, r in df.iterrows():
    table_rows.append(
        f"| {int(r['NO'])} | {r['KECAMATAN']} | {fmt_num(r['WKTP'])} | {fmt_num(r['KTP'])} | {fmt_num(r['BLMKTP'])} | {fmt_num(r['BLM_REKAM'])} | {fmt_num(r['KTP_LK'])} | {fmt_num(r['KTP_PR'])} | **{r['PERSEN_KTP']:.2f}%** |"
    )

table_str = "\n".join(table_rows)

readme_content = f"""# 🪪 Analisis & Dashboard Kepemilikan KTP-el Kabupaten Cirebon

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Dataset](https://img.shields.io/badge/Dataset-KTP%20Cirebon-2ECC71?style=for-the-badge&logo=microsoftexcel&logoColor=white)](KTP.csv)

Repository ini berisi analisis data komprehensif dan aplikasi dashboard interaktif untuk visualisasi statistik **Kepemilikan KTP Elektronik (KTP-el)** di **Kabupaten Cirebon** berdasarkan data 40 kecamatan.

---

## 📌 Ringkasan Data Utama Kabupaten Cirebon

| Indikator | Jumlah / Nilai | Keterangan |
| :--- | :--- | :--- |
| 👥 **Jumlah Wilayah** | **40 Kecamatan** | Wilayah administratif Kabupaten Cirebon |
| 📑 **Total Wajib KTP-el** | **{fmt_num(total_wktp)} Jiwa** | Seluruh penduduk usia wajib memiliki KTP-el |
| ✅ **Sudah Memiliki KTP-el** | **{fmt_num(total_ktp)} Jiwa** | **{persen_kepemilikan:.2f}%** dari total Wajib KTP-el |
| ❌ **Belum Memiliki KTP-el** | **{fmt_num(total_blmktp)} Jiwa** | **{persen_belum_ktp:.2f}%** dari total Wajib KTP-el |
| 📸 **Sudah Rekam KTP-el** | **{fmt_num(total_rekam)} Jiwa** | **{persen_rekam:.2f}%** dari total Wajib KTP-el |
| ⏳ **Belum Rekam KTP-el** | **{fmt_num(total_blm_rekam)} Jiwa** | **{persen_belum_rekam:.2f}%** dari total Wajib KTP-el |
| 👨 **Pemilik KTP-el Laki-Laki** | **{fmt_num(total_lk)} Jiwa** | Belum memiliki: {fmt_num(total_blm_lk)} Jiwa |
| 👩 **Pemilik KTP-el Perempuan** | **{fmt_num(total_pr)} Jiwa** | Belum memiliki: {fmt_num(total_blm_pr)} Jiwa |
| 🏆 **Cakupan Tertinggi** | **{tertinggi['KECAMATAN']} ({tertinggi['PERSEN_KTP']:.2f}%)** | Kecamatan dengan persentase kepemilikan tertinggi |
| ⚠️ **Cakupan Terendah** | **{terendah['KECAMATAN']} ({terendah['PERSEN_KTP']:.2f}%)** | Kecamatan dengan persentase kepemilikan terendah |

---

## 📈 Visualisasi & Grafik Analisis

### 1. Proporsi Kepemilikan KTP-el Kabupaten Cirebon
Persentase penduduk Wajib KTP-el yang sudah memiliki vs belum memiliki KTP-el:
![Proporsi Kepemilikan KTP-el](grafik_proporsi_kepemilikan.png)

---

### 2. Kepemilikan Berdasarkan Jenis Kelamin
Perbandingan jumlah penduduk laki-laki dan perempuan berdasarkan status kepemilikan:
![Kepemilikan Gender](grafik_gender.png)

---

### 3. Analisis Kecamatan Prioritas
Perbandingan wilayah dengan persentase terendah serta wilayah dengan jumlah belum memiliki / belum rekam terbanyak:

| 5 Kecamatan Persentase Terendah | 5 Kecamatan Belum Memiliki Terbanyak |
| :---: | :---: |
| ![Kepemilikan Terendah](grafik_kepemilikan_terendah.png) | ![Belum Memiliki Terbanyak](grafik_belum_memiliki_terbanyak.png) |

| 5 Kecamatan Belum Rekam Terbanyak | Top 3 vs Bottom 3 Belum Memiliki |
| :---: | :---: |
| ![Belum Rekam Terbanyak](grafik_belum_rekam_terbanyak.png) | ![Perbandingan Top Bottom](grafik_perbandingan_top_bottom.png) |

---

### 4. Peringkat Persentase Kepemilikan 40 Kecamatan
Peringkat seluruh kecamatan dari persentase terendah hingga tertinggi:
![Ranking Seluruh Kecamatan](grafik_ranking_semua_kecamatan.png)

---

## 📋 Tabel Data Kepemilikan KTP-el Per Kecamatan

> [!TIP]
> File data terstruktur juga dapat langsung dilihat dan diekspor dalam format **[KTP.csv](KTP.csv)** (kompatibel dengan tabel interaktif GitHub).

<details>
<summary><b>🔍 Klik di sini untuk melihat tabel data lengkap 40 Kecamatan</b></summary>

| No | Kecamatan | Wajib KTP | Memiliki KTP | Belum KTP | Belum Rekam | KTP (L) | KTP (P) | Capaian (%) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
{table_str}

</details>

---

## 📁 Struktur Direktori Repositori

```text
├── KTP.xlsx                          # Dataset sumber format Excel
├── KTP.csv                           # Dataset bersih CSV (tampilan tabel di GitHub)
├── analisis_ktp-el.py                # Script analisis data Python
├── analisis_ktp-el.ipynb             # Jupyter Notebook eksplorasi & visualisasi
├── app.py                            # Dashboard aplikasi interaktif Streamlit
├── export_assets.py                  # Script pembuatan visualisasi & ekspor CSV
├── generate_readme.py                # Script generator README.md otomatis
├── grafik_proporsi_kepemilikan.png    # Grafik Donut proporsi total Cirebon
├── grafik_gender.png                 # Grafik perbandingan gender Laki-laki vs Perempuan
├── grafik_kepemilikan_terendah.png   # Grafik 5 kecamatan persentase terendah
├── grafik_belum_memiliki_terbanyak.png# Grafik 5 kecamatan belum memiliki terbanyak
├── grafik_belum_rekam_terbanyak.png  # Grafik 5 kecamatan belum rekam terbanyak
├── grafik_perbandingan_top_bottom.png# Grafik perbandingan Top 3 & Bottom 3
├── grafik_ranking_semua_kecamatan.png# Grafik ranking 40 kecamatan
└── README.md                         # Dokumentasi utama tampilan antarmuka GitHub
```

---

## 🚀 Cara Menjalankan Proyek Secara Lokal

### 1. Instalasi Dependensi
Pastikan Python 3.9+ telah terpasang, lalu instal dependensi berikut:
```bash
pip install pandas openpyxl matplotlib seaborn streamlit
```

### 2. Menjalankan Dashboard Streamlit
Jalankan perintah berikut pada terminal:
```bash
streamlit run app.py
```

### 3. Menjalankan Script Analisis
```bash
python analisis_ktp-el.py
```

---

## 📚 Sumber Data
Data bersumber dari **Buku Profil Perkembangan Kependudukan Tahun 2025**, Dinas Kependudukan dan Pencatatan Sipil (Disdukcapil) Kabupaten Cirebon.
"""

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme_content)

print('README.md successfully generated!')
