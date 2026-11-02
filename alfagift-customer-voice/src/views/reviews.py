import streamlit as st

from src import components as ui
from src.config import ORDER
from src.context import csv_button
from src.issues import ISSUES


def render(c):
    ui.page_header("Reviews", "Cari dan baca suara pengguna secara langsung.", "REVIEW EXPLORER")
    if c.df.empty or "content" not in c.df.columns:
        return ui.empty_state("Dataset detail belum tersedia.")
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    kw = c1.text_input("Cari review", placeholder="contoh: pembayaran, kurir, promo")
    sf = c2.selectbox("Sentiment", ["Semua"] + ORDER)
    cat = c3.selectbox("Masalah", ["Semua"] + list(ISSUES) + ["Lainnya"])
    size = c4.selectbox("Per halaman", [25, 50, 100, 300], index=1)

    view = c.fdf
    if kw:
        view = view[view["content"].astype(str).str.contains(kw, case=False, na=False, regex=False)]
    if sf != "Semua" and "sentiment" in view.columns:
        view = view[view["sentiment"] == sf]
    if cat != "Semua":
        view = view[view["kategori"] == cat]

    pages = max(1, -(-len(view) // size))
    pg = st.number_input("Halaman", 1, pages, 1) if pages > 1 else 1
    cols = [x for x in ["reviewId", "content", "score", "sentiment", "indobert_pred", "kategori", "reviewCreatedVersion", "at"] if x in view.columns]
    st.caption(f"{len(view):,} review ditemukan • halaman {pg} dari {pages}")
    st.dataframe(view[cols].iloc[(pg - 1) * size: pg * size], hide_index=True, use_container_width=True,
                 column_config={"content": st.column_config.TextColumn("Review", width="large")})
    csv_button(view[cols], "⬇️ Unduh hasil pencarian (CSV)", "review_alfagift.csv", "dl_rv")
