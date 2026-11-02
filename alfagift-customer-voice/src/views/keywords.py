import plotly.express as px
import streamlit as st

from src import components as ui
from src.components import BRAND, SENTIMENT_COLORS as SC
from src.data import top_terms


def render(c):
    ui.page_header("Kata Kunci", "Kata dan frasa yang paling sering muncul dalam review.", "KEYWORD EXPLORER")
    if not c.has_detail:
        return ui.empty_state("Dataset detail belum tersedia.")
    c1, c2, c3 = st.columns(3)
    seg = c1.selectbox("Kelompok review", ["Negatif", "Netral", "Positif", "Semua"])
    gram = c2.radio("Jenis", ["Kata tunggal", "Frasa 2 kata"], horizontal=True)
    k = c3.slider("Jumlah teratas", 10, 30, 20)
    sub = c.fdf if seg == "Semua" else c.fdf[c.fdf[c.prediction_col].astype(str).str.lower() == seg.lower()]
    terms = top_terms(sub["content"].astype(str), 1 if gram == "Kata tunggal" else 2, k)
    if terms.empty:
        return ui.empty_state("Belum ada kata yang bisa ditampilkan.")

    fig = px.bar(terms.sort_values("jumlah"), x="jumlah", y="kata", orientation="h", text="jumlah",
                 color_discrete_sequence=[SC.get(seg, BRAND["navy"])])
    fig.update_traces(textposition="outside")
    fig.update_layout(xaxis_title="Frekuensi", yaxis_title=None)
    st.plotly_chart(ui.style_fig(fig, 80 + 24 * len(terms), legend=False), use_container_width=True)

    ui.section_label("LIHAT REVIEW YANG MENGANDUNG KATA INI")
    left, _ = st.columns([1, 2])
    word = left.selectbox("Kata / frasa", terms["kata"].tolist())
    n, sort = c.example_controls("kw")
    hit = sub[sub["content"].astype(str).str.contains(word, case=False, regex=False)]
    st.caption(f"{len(hit):,} review mengandung “{word}”")
    c.render_quotes(c.pick_examples(hit, n, sort))
