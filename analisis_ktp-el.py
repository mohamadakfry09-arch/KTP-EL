import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Membaca dan Memahami Data
data = pd.read_excel("KTP.xlsx", header=2)

print("Header Data")
print(data.head())

print("\nKolom Data")
print(data.columns)

print("\n Info Data")
data.info()

# 2. Pemilihan Kolom yang Digunakan
df = pd.DataFrame({
    "KECAMATAN": data["WILAYAH"],
    "WKTP": data["WKTP"],
    "KTP": data["KTP"],
    "PERSEN_KTP": data["%.1"],
    "BLM_REKAM": data["BLM_REKAM"],
    "KTP_LK": data["KTP_LK"],
    "KTP_PR": data["KTP_PR"],
    "BLMKTP": data["BLMKTP"]
})

# 3. Data Cleaning
# A. Cek Missing Value
print("\nCek missing value")
print(df.isnull().values.any())

# Jumlah Data Sebelum Cleaning
print("\nJumlah data sebelum cleaning :", len(df))

# Menampilkan Seluruh Baris
print("\nData sebelum cleaning :")
print(df.head(45))

# B. Hapus Baris Agregat dan yang Tidak Diperlukan
df = df.dropna()
df = df.drop(index=41)

# Cek Kembali Missing Value
print("\nCek kembali missing value")
print(df.isnull().values.any())

# C. Reset index
df.reset_index(drop=True, inplace=True)
df.index = range(1, len(df) + 1)

# Jumlah Data Setelah Cleaning
print("\nJumlah data setelah cleaning :", len(df))

# Menampilkan Seluruh Baris
print("\nData setelah cleaning :")
print(df.head(40))

# D. Cek Tipe Data
print("\nTipe Data : ")
print(df.dtypes)

# 4. RINGKASAN DATA
print("\n===== RINGKASAN DATA =====")

# Hitung total dan persentase
total_wktp = df["WKTP"].sum()
total_ktp = df["KTP"].sum()
total_blmktp = df["BLMKTP"].sum()
total_blm_rekam = df["BLM_REKAM"].sum()
total_lk = df["KTP_LK"].sum()
total_pr = df["KTP_PR"].sum()

total_rekam = total_wktp - total_blm_rekam

persen_kepemilikan = (total_ktp / total_wktp) * 100
persen_belum_ktp = (total_blmktp / total_wktp) * 100
persen_rekam = (total_rekam / total_wktp) * 100
persen_belum_rekam = (total_blm_rekam / total_wktp) * 100
persen_lk = (total_lk / total_ktp) * 100
persen_pr = (total_pr / total_ktp) * 100

# Menampilkan hasil perhitungan
print("Jumlah Kecamatan :", len(df))

print("Total Wajib KTP-el :", f"{int(total_wktp):,}".replace(",", "."))
print("Total Memiliki KTP-el :", f"{int(total_ktp):,}".replace(",", "."))
print("Total Belum Memiliki KTP-el :", f"{int(total_blmktp):,}".replace(",", "."))
print("Total Sudah Rekam KTP-el :", f"{int(total_rekam):,}".replace(",", "."))
print("Total Belum Rekam KTP-el :", f"{int(total_blm_rekam):,}".replace(",", "."))
print("Total Pemilik KTP-el Laki-Laki :", f"{int(total_lk):,}".replace(",", "."))
print("Total Pemilik KTP-el Perempuan :", f"{int(total_pr):,}".replace(",", "."))
print("Persentase Kepemilikan KTP-el :", f"{persen_kepemilikan:.2f}%")
print("Persentase Belum Memiliki KTP-el :", f"{persen_belum_ktp:.2f}%")
print("Persentase Sudah Rekam KTP-el :", f"{persen_rekam:.2f}%")
print("Persentase Belum Rekam KTP-el :", f"{persen_belum_rekam:.2f}%")
print("Persentase Pemilik KTP-el Laki-Laki :", f"{persen_lk:.2f}%")
print("Persentase Pemilik KTP-el Perempuan :", f"{persen_pr:.2f}%")

# 5. Grafik
# A. Gaya Grafik
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 3.5)

# B. Grafik 1 : Kepemilikan KTP Terendah
top_persen_rendah = df.sort_values(
    "PERSEN_KTP"
).head(5)

plt.figure()

ax = sns.barplot(
    data=top_persen_rendah,
    x="PERSEN_KTP",
    y="KECAMATAN",
    color="steelblue"
)

plt.title("5 Kecamatan dengan Kepemilikan KTP-el Terendah")
plt.xlabel("Persentase Kepemilikan KTP (%)")
plt.ylabel("")
plt.grid(axis="x", linestyle="--", alpha=0.5)

for p in ax.patches:
    ax.annotate(
        f"{p.get_width():.1f}%".replace(".", ","),
        (p.get_width(), p.get_y() + p.get_height()/2),
        va="center"
    )

plt.tight_layout()
#plt.savefig("grafik_1_persentase_kepemilikan_ktp.png", dpi=300, bbox_inches="tight")
plt.show()

# C. Grafik 2 : Belum Memiliki KTP Terbanyak
top_blmktp = df.sort_values(
    "BLMKTP",
    ascending=False
).head(5)

plt.figure()

ax = sns.barplot(
    data=top_blmktp,
    x="BLMKTP",
    y="KECAMATAN",
    color="darkorange"
)

plt.title("5 Kecamatan Belum Memiliki KTP-el Terbanyak")
plt.xlabel("Jumlah Penduduk")
plt.ylabel("")
plt.grid(axis="x", linestyle="--", alpha=0.5)

for p in ax.patches:
    ax.annotate(
        f"{int(p.get_width()):,}".replace(",", "."),
        (p.get_width(), p.get_y() + p.get_height()/2),
        va="center"
    )

plt.tight_layout()
#plt.savefig("grafik_2_belum_memiliki_ktp.png", dpi=300, bbox_inches="tight")
plt.show()

# D. Grafik 3 : Belum Rekam KTP Terbanyak
top_blmrekam = df.sort_values(
    "BLM_REKAM",
    ascending=False
).head(5)

plt.figure()

ax = sns.barplot(
    data=top_blmrekam,
    x="BLM_REKAM",
    y="KECAMATAN",
    color="tomato"
)

plt.title("5 Kecamatan Belum Rekam KTP-el Terbanyak")
plt.xlabel("Jumlah Penduduk")
plt.ylabel("")
plt.grid(axis="x", linestyle="--", alpha=0.5)

for p in ax.patches:
    ax.annotate(
        f"{int(p.get_width()):,}".replace(",", "."),
        (p.get_width(), p.get_y() + p.get_height()/2),
        va="center"
    )

plt.tight_layout()
#plt.savefig("grafik_3_belum_rekam.png", dpi=300, bbox_inches="tight")
plt.show()

# E. Grafik 4 : Kepemilikan KTP di Kabupaten Cirebon
sudah_memiliki = df["KTP"].sum()
belum_memiliki = df["BLMKTP"].sum()

total = sudah_memiliki + belum_memiliki

persentase_ktp = (sudah_memiliki / total) * 100

plt.figure(figsize=(8, 5))

wedges, texts, autotexts = plt.pie(
    [sudah_memiliki, belum_memiliki],
    autopct="%1.1f%%",
    startangle=90,
    colors=["mediumseagreen", "tomato"],
    explode=(0, 0.08),
    wedgeprops=dict(width=0.45),
    pctdistance=1.08
)

# Ukuran teks persentase
for autotext in autotexts:
    autotext.set_fontsize(10)
    autotext.set_fontweight("bold")

autotexts[0].set_text("")
autotexts[1].set_y(1.15)

# Teks di tengah donut
plt.text(
    0,
    0,
    f"{persentase_ktp:.1f}%",
    ha="center",
    va="center",
    fontsize=18,
    fontweight="bold"
)

# Keterangan
plt.legend(
    wedges,
    [
        f"Sudah Memiliki KTP ({sudah_memiliki:,.0f})".replace(",", "."),
        f"Belum Memiliki KTP ({belum_memiliki:,.0f})".replace(",", ".")
    ],
    title="Keterangan",
    loc="center left",
    bbox_to_anchor=(0.85, 0.5)
)

plt.title("Persentase Kepemilikan KTP-el Kabupaten Cirebon", fontsize=12, fontweight="bold", x=0.73)
plt.axis("equal")
plt.tight_layout()
#plt.savefig("grafik_4_kepemilikan_ktp.png", dpi=300, bbox_inches="tight")
plt.show()