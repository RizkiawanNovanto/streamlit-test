import plotly.express as px
import streamlit as st

from src import components as ui
from src.components import BRAND
from src.context import csv_button
from src.data import issue_table


def render(c):
    ui.page_header("Masalah Pengguna", "Area layanan yang paling sering muncul pada review negatif menurut prediksi model.", "ISSUE INTELLIGENCE")
    if not c.has_detail:
        return ui.empty_state("Dataset detail belum tersedia. Pastikan file model_predictions_common_test_set.csv ada di folder data/final/.")
    neg = c.neg
    s = issue_table(neg)
    if s.empty:
        return ui.empty_state("Belum ada issue yang dapat dipetakan.")

    ui.section_label("PETA MASALAH")
    fig = px.bar(s.sort_values("jumlah"), x="jumlah", y="kategori", orientation="h", text="jumlah",
                 color_discrete_sequence=[BRAND["red"]])
    fig.update_traces(textposition="outside")
    fig.update_layout(xaxis_title="Jumlah review negatif", yaxis_title=None)
    st.plotly_chart(ui.style_fig(fig, 340, legend=False), use_container_width=True)
    other = int((neg["kategori"] == "Lainnya").sum())
    st.caption(f"Sumber prediksi: {c.prediction_col} • {other:,} review negatif belum masuk kategori mana pun (lihat di “Lainnya”).")

    ui.section_label("BACA REVIEW PER MASALAH")
    focus = st.selectbox("Fokus pada masalah", ["Semua masalah"] + s["kategori"].tolist() + ["Lainnya"])
    n, sort = c.example_controls("mp")
    csv_button(neg[[x for x in ["content", "score", "at", "reviewCreatedVersion", "kategori"] if x in neg.columns]],
               "⬇️ Unduh review negatif (CSV)", "review_negatif_alfagift.csv", "dl_mp")
    st.write("")
    if focus == "Lainnya":
        c.show_issue("Lainnya", other, other / max(len(neg), 1) * 100, n, sort)
    else:
        rows = s if focus == "Semua masalah" else s[s["kategori"] == focus]
        for r in rows.itertuples():
            c.show_issue(r.kategori, int(r.jumlah), float(r.persentase), n, sort)
