import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch

# 1. Load data
data = pd.read_excel('KTP.xlsx', header=2)

df = pd.DataFrame({
    'KECAMATAN': data['WILAYAH'],
    'WKTP': data['WKTP'],
    'KTP': data['KTP'],
    'PERSEN_KTP': data['%.1'],
    'BLM_REKAM': data['BLM_REKAM'],
    'KTP_LK': data['KTP_LK'],
    'KTP_PR': data['KTP_PR'],
    'BLMKTP': data['BLMKTP'],
    'BLM_KTP_LK': data['BLM_KTP_LK'],
    'BLM_KTP_PR': data['BLM_KTP_PR']
})

# Data cleaning: drop header/aggregate rows
df = df.dropna().drop(index=41).reset_index(drop=True)
df['NO'] = range(1, len(df) + 1)

# Ensure numeric types
cols_int = ['WKTP', 'KTP', 'BLM_REKAM', 'KTP_LK', 'KTP_PR', 'BLMKTP', 'BLM_KTP_LK', 'BLM_KTP_PR']
for c in cols_int:
    df[c] = df[c].astype(int)
df['PERSEN_KTP'] = df['PERSEN_KTP'].astype(float)

# Rearrange columns
cols_order = ['NO', 'KECAMATAN', 'WKTP', 'KTP', 'PERSEN_KTP', 'BLMKTP', 'BLM_REKAM', 'KTP_LK', 'KTP_PR', 'BLM_KTP_LK', 'BLM_KTP_PR']
df = df[cols_order]

# Save clean CSV for GitHub table preview
df.to_csv('KTP.csv', index=False, encoding='utf-8-sig')

# Styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

# 1. Donut Chart - Proporsi Kepemilikan KTP-el Cirebon
sudah_memiliki = df['KTP'].sum()
belum_memiliki = df['BLMKTP'].sum()
total = sudah_memiliki + belum_memiliki
persentase_ktp = (sudah_memiliki / total) * 100

fig4, ax4 = plt.subplots(figsize=(7, 4.5), dpi=300)
wedges, texts, autotexts = ax4.pie(
    [sudah_memiliki, belum_memiliki],
    autopct='%1.1f%%',
    startangle=90,
    colors=['#2ECC71', '#E74C3C'],
    explode=(0, 0.08),
    wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2),
    pctdistance=1.08
)
for autotext in autotexts:
    autotext.set_fontsize(10)
    autotext.set_fontweight('bold')
autotexts[0].set_text('')
autotexts[1].set_y(1.15)
ax4.text(0, 0, f'{persentase_ktp:.2f}%', ha='center', va='center', fontsize=20, fontweight='bold', color='#2C3E50')
legend = ax4.legend(
    wedges,
    [f'Sudah Memiliki KTP ({sudah_memiliki:,.0f})'.replace(',', '.'),
     f'Belum Memiliki KTP ({belum_memiliki:,.0f})'.replace(',', '.')],
    title='Status Kepemilikan',
    loc='center left',
    bbox_to_anchor=(1, 0.5),
    fontsize=10
)
legend.get_title().set_fontweight('bold')
ax4.set_title('Persentase Kepemilikan KTP-el Kabupaten Cirebon', fontsize=13, fontweight='bold', pad=15)
ax4.axis('equal')
plt.tight_layout()
plt.savefig('grafik_proporsi_kepemilikan.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. 5 Kecamatan Persentase Kepemilikan Terendah
top_persen_rendah = df.sort_values('PERSEN_KTP').head(5)
fig1, ax1 = plt.subplots(figsize=(9, 4), dpi=300)
sns.barplot(data=top_persen_rendah, x='PERSEN_KTP', y='KECAMATAN', color='#3498DB', edgecolor='none', ax=ax1)
ax1.set_xlabel('Persentase Kepemilikan KTP (%)', fontweight='bold', fontsize=11)
ax1.set_ylabel('')
ax1.set_title('5 Kecamatan dengan Persentase Kepemilikan KTP-el Terendah', fontweight='bold', fontsize=12, pad=10)
ax1.grid(axis='x', linestyle='--', alpha=0.5)
for p in ax1.patches:
    ax1.annotate(f'{p.get_width():.2f}%'.replace('.', ','), (p.get_width(), p.get_y() + p.get_height() / 2), va='center', xytext=(5, 0), textcoords='offset points', fontweight='bold')
sns.despine(ax=ax1, left=True, bottom=True)
plt.tight_layout()
plt.savefig('grafik_kepemilikan_terendah.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. 5 Kecamatan Belum Memiliki KTP Terbanyak
top_blm_ktp = df.sort_values('BLMKTP', ascending=False).head(5)
fig2, ax2 = plt.subplots(figsize=(9, 4), dpi=300)
sns.barplot(data=top_blm_ktp, x='BLMKTP', y='KECAMATAN', color='#E67E22', edgecolor='none', ax=ax2)
ax2.set_xlabel('Jumlah Penduduk (Jiwa)', fontweight='bold', fontsize=11)
ax2.set_ylabel('')
ax2.set_title('5 Kecamatan dengan Penduduk Belum Memiliki KTP-el Terbanyak', fontweight='bold', fontsize=12, pad=10)
ax2.grid(axis='x', linestyle='--', alpha=0.5)
for p in ax2.patches:
    ax2.annotate(f'{int(p.get_width()):,}'.replace(',', '.'), (p.get_width(), p.get_y() + p.get_height() / 2), va='center', xytext=(5, 0), textcoords='offset points', fontweight='bold')
sns.despine(ax=ax2, left=True, bottom=True)
plt.tight_layout()
plt.savefig('grafik_belum_memiliki_terbanyak.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. 5 Kecamatan Belum Rekam KTP Terbanyak
top_blm_rekam = df.sort_values('BLM_REKAM', ascending=False).head(5)
fig3, ax3 = plt.subplots(figsize=(9, 4), dpi=300)
sns.barplot(data=top_blm_rekam, x='BLM_REKAM', y='KECAMATAN', color='#E74C3C', edgecolor='none', ax=ax3)
ax3.set_xlabel('Jumlah Penduduk (Jiwa)', fontweight='bold', fontsize=11)
ax3.set_ylabel('')
ax3.set_title('5 Kecamatan dengan Penduduk Belum Rekam KTP-el Terbanyak', fontweight='bold', fontsize=12, pad=10)
ax3.grid(axis='x', linestyle='--', alpha=0.5)
for p in ax3.patches:
    ax3.annotate(f'{int(p.get_width()):,}'.replace(',', '.'), (p.get_width(), p.get_y() + p.get_height() / 2), va='center', xytext=(5, 0), textcoords='offset points', fontweight='bold')
sns.despine(ax=ax2, left=True, bottom=True)
plt.tight_layout()
plt.savefig('grafik_belum_rekam_terbanyak.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. Kepemilikan Berdasarkan Gender
gender_ktp = pd.DataFrame({
    'Jenis Kelamin': ['Laki-Laki', 'Perempuan'],
    'Memiliki KTP-el': [df['KTP_LK'].sum(), df['KTP_PR'].sum()],
    'Belum Memiliki KTP-el': [df['BLM_KTP_LK'].sum(), df['BLM_KTP_PR'].sum()]
})
gender_long = gender_ktp.melt(id_vars='Jenis Kelamin', var_name='Status', value_name='Jumlah')
fig5, ax5 = plt.subplots(figsize=(9, 4.5), dpi=300)
sns.barplot(data=gender_long, x='Jenis Kelamin', y='Jumlah', hue='Status', palette={'Memiliki KTP-el': '#2ECC71', 'Belum Memiliki KTP-el': '#E74C3C'}, edgecolor='none', ax=ax5)
ax5.set_xlabel('Jenis Kelamin', fontsize=11, fontweight='bold')
ax5.set_ylabel('Jumlah Penduduk', fontsize=11, fontweight='bold')
ax5.set_title('Kepemilikan KTP-el Berdasarkan Jenis Kelamin', fontsize=12, fontweight='bold', pad=10)
ax5.grid(axis='y', linestyle='--', alpha=0.4)
for p in ax5.patches:
    tinggi = p.get_height()
    if tinggi > 0:
        ax5.annotate(f'{int(tinggi):,}'.replace(',', '.'), (p.get_x() + p.get_width() / 2, tinggi), ha='center', va='bottom', fontsize=9, xytext=(0, 4), textcoords='offset points', fontweight='bold')
sns.despine(ax=ax5, left=True, bottom=True)
legend = ax5.legend(title='Status', loc='upper right', frameon=True)
legend.get_title().set_fontweight('bold')
plt.tight_layout()
plt.savefig('grafik_gender.png', dpi=300, bbox_inches='tight')
plt.close()

# 6. Top 3 Terbanyak vs Terendah Belum Memiliki KTP-el
top3 = df.sort_values('BLMKTP', ascending=False).head(3).copy()
top3['Kategori'] = 'Belum Memiliki KTP-el Terbanyak'
bot3 = df.sort_values('BLMKTP', ascending=True).head(3).copy()
bot3['Kategori'] = 'Belum Memiliki KTP-el Terendah'
g6 = pd.concat([top3, bot3]).sort_values('BLMKTP', ascending=False)
warna = g6['Kategori'].map({'Belum Memiliki KTP-el Terbanyak': '#E74C3C', 'Belum Memiliki KTP-el Terendah': '#3498DB'})
fig6, ax6 = plt.subplots(figsize=(9, 4.5), dpi=300)
sns.barplot(data=g6, x='BLMKTP', y='KECAMATAN', hue='KECAMATAN', palette=warna.tolist(), legend=False, edgecolor='none', ax=ax6)
ax6.set_xlabel('Jumlah Penduduk', fontweight='bold')
ax6.set_ylabel('')
ax6.set_title('Perbandingan Top 3 & Bottom 3 Belum Memiliki KTP-el', fontweight='bold', fontsize=12, pad=10)
ax6.grid(axis='x', linestyle='--', alpha=0.5)
for p in ax6.patches:
    lebar = p.get_width()
    if lebar > 0:
        ax6.annotate(f'{int(lebar):,}'.replace(',', '.'), (lebar, p.get_y() + p.get_height() / 2), va='center', xytext=(5, 0), textcoords='offset points', fontweight='bold')
legend_elements = [
    Patch(facecolor='#E74C3C', label='Belum Memiliki KTP-el Terbanyak'),
    Patch(facecolor='#3498DB', label='Belum Memiliki KTP-el Terendah')
]
legend = ax6.legend(handles=legend_elements, title='Kategori', loc='lower right', frameon=True)
legend.get_title().set_fontweight('bold')
sns.despine(ax=ax6, left=True, bottom=True)
plt.tight_layout()
plt.savefig('grafik_perbandingan_top_bottom.png', dpi=300, bbox_inches='tight')
plt.close()

# 7. Ranking Seluruh 40 Kecamatan Berdasarkan Persentase Kepemilikan KTP-el
df_sorted = df.sort_values('PERSEN_KTP', ascending=True)
fig7, ax7 = plt.subplots(figsize=(10, 12), dpi=300)
sns.barplot(data=df_sorted, x='PERSEN_KTP', y='KECAMATAN', hue='KECAMATAN', palette='Blues_r', legend=False, edgecolor='none', ax=ax7)
ax7.set_xlabel('Persentase Kepemilikan KTP (%)', fontweight='bold', fontsize=11)
ax7.set_ylabel('')
ax7.set_title('Peringkat Persentase Kepemilikan KTP-el 40 Kecamatan', fontweight='bold', fontsize=13, pad=12)
ax7.grid(axis='x', linestyle='--', alpha=0.5)
for p in ax7.patches:
    ax7.annotate(f'{p.get_width():.2f}%'.replace('.', ','), (p.get_width(), p.get_y() + p.get_height() / 2), va='center', xytext=(5, 0), textcoords='offset points', fontsize=9)
sns.despine(ax=ax7, left=True, bottom=True)
plt.tight_layout()
plt.savefig('grafik_ranking_semua_kecamatan.png', dpi=300, bbox_inches='tight')
plt.close()

print('ALL ASSETS UPDATED CLEANLY!')
