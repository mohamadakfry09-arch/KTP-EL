import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch

# 1. Pengaturan Halaman
st. set_page_config(
    page_title="Dashboard Kepemilikan KTP-el",
    page_icon="🪪",
    layout="wide"
)

# 2. Judul Dashboard
st.title("🪪 Dashboard Kepemilikan KTP-el Kabupaten Cirebon")
st.write("Visualisasi data kepemilikan KTP-el Kabupaten Cirebon Tahun 2025.")

# 3. Membaca Data
data = pd.read_excel("KTP.xlsx", header=2)

# 4. Pemilihan Kolom yang Digunakan
df = pd.DataFrame({
    "KECAMATAN": data["WILAYAH"],
    "WKTP": data["WKTP"],
    "KTP": data["KTP"],
    "PERSEN_KTP": data["%.1"],
    "BLM_REKAM": data["BLM_REKAM"],
    "KTP_LK": data["KTP_LK"],
    "KTP_PR": data["KTP_PR"],
    "BLMKTP": data["BLMKTP"],
    "BLM_KTP_LK" : data["BLM_KTP_LK"],
    "BLM_KTP_PR" : data["BLM_KTP_PR"]
})

# 5. Data Cleaning
df = df.dropna()
df = df.drop(index=41)

df.reset_index(drop=True, inplace=True)
df.index = range(1, len(df) + 1)

# 6. Perhitungan KPI
total_wktp = df["WKTP"].sum()
total_ktp = df["KTP"].sum()
total_blmktp = df["BLMKTP"].sum()
total_blm_rekam = df["BLM_REKAM"].sum()
total_rekam = total_wktp - total_blm_rekam

persen_kepemilikan = (total_ktp / total_wktp) * 100
persen_belum_ktp = (total_blmktp / total_wktp) * 100
persen_rekam = (total_rekam / total_wktp) * 100
persen_belum_rekam = (total_blm_rekam / total_wktp) * 100

# 7. Tampilan KPI
st.header("📌 Informasi Umum")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Jumlah Kecamatan",
        f"{len(df)} Kecamatan"
    )
with col2:
    st.metric("Wajib KTP-el", f"{total_wktp:,.0f}".replace(",", "."))
with col3:
    st.metric(
        "Memiliki KTP-el",
        f"{total_ktp:,.0f}".replace(",", ".")
    )
    st.caption(
        f"{persen_kepemilikan:.2f}% dari wajib KTP-el".replace(".", ",")
    )

col4, col5, col6 = st.columns(3)
with col4:
    st.metric(
        "Belum Memiliki KTP-el",
        f"{total_blmktp:,.0f}".replace(",", ".")
    )
    st.caption(
        f"{persen_belum_ktp:.2f}% dari wajib KTP-el".replace(".", ",")
    )
with col5:
    st.metric(
        "Sudah Rekam KTP-el",
        f"{total_rekam:,.0f}".replace(",", ".")
    )
    st.caption(
            f"{persen_rekam:.2f}% dari wajib KTP-el".replace(".", ",")
    )
with col6:
    st.metric(
        "Belum Rekam KTP-el",
        f"{total_blm_rekam:,.0f}".replace(",", ".")
    )
    st.caption(
            f"{persen_belum_rekam:.2f}% dari wajib KTP-el".replace(".", ",")
    )

# 8. Capaian Kecamatan
st.subheader("Capaian Kecamatan")
st.caption(
    "Menunjukkan kecamatan dengan persentase kepemilikan KTP-el "
    "tertinggi dan terendah."
)

# Kecamatan dengan persentase kepemilikan tertinggi
tertinggi = df.loc[
    df["PERSEN_KTP"].idxmax()
]

# Kecamatan dengan persentase kepemilikan terendah
terendah = df.loc[
    df["PERSEN_KTP"].idxmin()
]

col_high, col_low = st.columns(2)

with col_high:
    st.success(
        f"**Tertinggi:** {tertinggi['KECAMATAN']} "
        f"({tertinggi['PERSEN_KTP']:.2f}%)"
    )

with col_low:
    st.error(
        f"**Terendah:** {terendah['KECAMATAN']} "
        f"({terendah['PERSEN_KTP']:.2f}%)"
    )

# 9. Grafik 1 : Kepemilikan KTP-el di Kabupaten Cirebon
st.divider()
st.header("📊 Persentase Kepemilikan KTP-el Kabupaten Cirebon")

sudah_memiliki = df["KTP"].sum()
belum_memiliki = df["BLMKTP"].sum()

total = sudah_memiliki + belum_memiliki

persentase_ktp = (sudah_memiliki / total) * 100

fig4, ax4 = plt.subplots(figsize=(8, 5))

wedges, texts, autotexts = ax4.pie(
    [sudah_memiliki, belum_memiliki],
    autopct="%1.1f%%",
    startangle=90,
    colors=["mediumseagreen", "tomato"],
    explode=(0, 0.08),
    wedgeprops=dict(width=0.45),
    pctdistance=1.08
)

for autotext in autotexts:
    autotext.set_fontsize(10)
    autotext.set_fontweight("bold")

autotexts[0].set_text("")
autotexts[1].set_y(1.15)

ax4.text(
    0,
    0,
    f"{persentase_ktp:.1f}%",
    ha="center",
    va="center",
    fontsize=18,
    fontweight="bold"
)

legend = ax4.legend(
    wedges,
    [
        f"Sudah Memiliki KTP ({sudah_memiliki:,.0f})".replace(",", "."),
        f"Belum Memiliki KTP ({belum_memiliki:,.0f})".replace(",", ".")
    ],
    title="Keterangan",
    loc="center left",
    bbox_to_anchor=(1, 0.5)
)
legend.get_title().set_fontweight("bold")

ax4.axis("equal")

plt.tight_layout()

st.pyplot(fig4)

st.caption(
    "Diagram menunjukkan persentase penduduk Wajib KTP-el yang sudah "
    "memiliki dan yang belum memiliki KTP-el."
)

# Analisis per Kecamatan
st.divider()
st.header("📍 Analisis per Kecamatan")

# 10. Grafik 2 : Kepemilikan KTP-el Terendah
st.subheader("1. Kecamatan dengan Persentase Kepemilikan KTP-el Terendah")
top_persen_rendah = df.sort_values(
    "PERSEN_KTP"
).head(5)

fig1, ax1 = plt.subplots(figsize=(10, 5))

sns.barplot(
    data=top_persen_rendah,
    x="PERSEN_KTP",
    y="KECAMATAN",
    color="steelblue",
    edgecolor="none",
    ax=ax1
)

ax1.set_xlabel(
    "Persentase Kepemilikan KTP (%)",
    fontweight="bold"
)

ax1.set_ylabel("")

ax1.grid(
    axis="x",
    linestyle="--",
    alpha=0.5
)

for p in ax1.patches:
    ax1.annotate(
        f"{p.get_width():.1f}%".replace(".", ","),
        (
            p.get_width(),
            p.get_y() + p.get_height() / 2
        ),
        va="center"
    )

sns.despine(
    ax=ax1,
    left=True,
    bottom=True
)

plt.tight_layout()

st.pyplot(fig1)

# 11. Grafik 3 : Belum Memiliki KTP-el Terbanyak
st.subheader("2. Kecamatan dengan Jumlah Belum Memiliki KTP-el Terbanyak")
top_blm_ktp = df.sort_values(
    "BLMKTP",
    ascending=False
).head(5)

fig2, ax2 = plt.subplots(figsize=(10, 5))

sns.barplot(
    data=top_blm_ktp,
    x="BLMKTP",
    y="KECAMATAN",
    color="darkorange",
    edgecolor="none",
    ax=ax2
)

ax2.set_xlabel(
    "Jumlah Penduduk",
    fontweight="bold"
)

ax2.set_ylabel("")

ax2.grid(
    axis="x",
    linestyle="--",
    alpha=0.5
)

for p in ax2.patches:
    ax2.annotate(
        f"{p.get_width():,.0f}".replace(",", "."),
        (
            p.get_width(),
            p.get_y() + p.get_height() / 2
        ),
        va="center"
    )

sns.despine(
    ax=ax2,
    left=True,
    bottom=True
)

plt.tight_layout()

st.pyplot(fig2)

# 12. Grafik 4 : Belum Rekam KTP-el Terbanyak
st.subheader("3. Kecamatan dengan Jumlah Belum Rekam KTP-el Terbanyak")
top_blm_rekam = df.sort_values(
    "BLM_REKAM",
    ascending=False
).head(5)

fig3, ax3 = plt.subplots(figsize=(10, 5))

sns.barplot(
    data=top_blm_rekam,
    x="BLM_REKAM",
    y="KECAMATAN",
    color="tomato",
    edgecolor="none",
    ax=ax3
)

ax3.set_xlabel(
    "Jumlah Penduduk",
    fontweight="bold"
)

ax3.set_ylabel("")

ax3.grid(
    axis="x",
    linestyle="--",
    alpha=0.5
)

for p in ax3.patches:
    ax3.annotate(
        f"{p.get_width():,.0f}".replace(",", "."),
        (
            p.get_width(),
            p.get_y() + p.get_height() / 2
        ),
        va="center"
    )

sns.despine(
    ax=ax3,
    left=True,
    bottom=True
)

plt.tight_layout()

st.pyplot(fig3)

# 13. Grafik 5 : Kepemilikan KTP-el Berdasarkan Jenis Kelamin
st.divider()
st.header("👥 Kepemilikan KTP-el Berdasarkan Jenis Kelamin")
st.caption(
    "Perbandingan jumlah penduduk laki-laki dan perempuan berdasarkan "
    "status kepemilikan KTP-el."
)

gender_ktp = pd.DataFrame({
    "Jenis Kelamin": [
        "Laki-Laki",
        "Perempuan"
    ],
    "Memiliki KTP-el": [
        df["KTP_LK"].sum(),
        df["KTP_PR"].sum()
    ],
    "Belum Memiliki KTP-el": [
        df["BLM_KTP_LK"].sum(),
        df["BLM_KTP_PR"].sum()
    ]
})

gender_long = gender_ktp.melt(
    id_vars="Jenis Kelamin",
    var_name="Status",
    value_name="Jumlah"
)

fig5, ax5 = plt.subplots(figsize=(10, 5))

sns.barplot(
    data=gender_long,
    x="Jenis Kelamin",
    y="Jumlah",
    hue="Status",
    palette={
        "Memiliki KTP-el": "#7EFF98",
        "Belum Memiliki KTP-el": "#F95A92"
    },
    edgecolor="none",
    ax=ax5
)

ax5.set_xlabel(
    "Jenis Kelamin",
    fontsize=11,
    fontweight="bold"
)

ax5.set_ylabel(
    "Jumlah Penduduk",
    fontsize=11,
    fontweight="bold"
)

ax5.grid(
    axis="y",
    linestyle="--",
    alpha=0.4
)

for p in ax5.patches:
    tinggi = p.get_height()

    if tinggi > 0:
        ax5.annotate(
            f"{tinggi:,.0f}".replace(",", "."),
            (
                p.get_x() + p.get_width() / 2,
                tinggi
            ),
            ha="center",
            va="bottom",
            fontsize=10,
            xytext=(0, 4),
            textcoords="offset points"
        )

sns.despine(
    ax=ax5,
    left=True,
    bottom=True
)

legend = ax5.legend(
    title="Status",
    loc="upper right",
    frameon=True
)

legend.get_title().set_fontweight("bold")

plt.tight_layout()

st.pyplot(fig5)

# 14. Grafik 6 : Top 3 Teratas dan 3 Terbawah Belum Memiliki KTP-el Terbanyak
st.divider()
st.header("📍 Perbandingan Kecamatan")
st.caption(
    "Perbandingan tiga kecamatan dengan jumlah penduduk belum memiliki "
    "KTP-el terbanyak dan tiga kecamatan dengan jumlah terendah."
)

top3_blm_ktp = df.sort_values(
    "BLMKTP",
    ascending=False
).head(3).copy()

top3_blm_ktp["Kategori"] = (
    "Belum Memiliki KTP-el Terbanyak"
)

bottom3_blm_ktp = df.sort_values(
    "BLMKTP",
    ascending=True
).head(3).copy()

bottom3_blm_ktp["Kategori"] = (
    "Belum Memiliki KTP-el Terendah"
)

grafik_6 = pd.concat([
    top3_blm_ktp,
    bottom3_blm_ktp
])

grafik_6 = grafik_6.sort_values(
    "BLMKTP",
    ascending=False
)

warna = grafik_6["Kategori"].map({
    "Belum Memiliki KTP-el Terbanyak": "#F95A92",
    "Belum Memiliki KTP-el Terendah": "#7FB3D5"
})

fig6, ax6 = plt.subplots(figsize=(10, 5))

sns.barplot(
    data=grafik_6,
    x="BLMKTP",
    y="KECAMATAN",
    palette=warna.tolist(),
    edgecolor="none",
    ax=ax6
)

ax6.set_xlabel(
    "Jumlah Penduduk",
    fontweight="bold"
)

ax6.set_ylabel("")

ax6.grid(
    axis="x",
    linestyle="--",
    alpha=0.5
)

for p in ax6.patches:
    lebar = p.get_width()

    if lebar > 0:
        ax6.annotate(
            f"{lebar:,.0f}".replace(",", "."),
            (
                lebar,
                p.get_y() + p.get_height() / 2
            ),
            va="center",
            xytext=(5, 0),
            textcoords="offset points"
        )

legend_elements = [
    Patch(
        facecolor="#F95A92",
        label="Belum Memiliki KTP-el Terbanyak"
    ),
    Patch(
        facecolor="#7FB3D5",
        label="Belum Memiliki KTP-el Terendah"
    )
]

legend = ax6.legend(
    handles=legend_elements,
    title="Kategori",
    loc="lower right",
    frameon=True
)

legend.get_title().set_fontweight("bold")

sns.despine(
    ax=ax6,
    left=True,
    bottom=True
)

plt.tight_layout()

st.pyplot(fig6)

# 14. Tabel Data
st.divider()
st.header("📋 Data Kepemilikan KTP-el per Kecamatan")
with st.expander("📋 Lihat Data Seluruh Kecamatan"):
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

st.caption("Sumber data: Buku Profil Perkembangan Kependudukan Tahun 2025")