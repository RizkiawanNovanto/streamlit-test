import plotly.express as px
import streamlit as st

from src import components as ui
from src.components import BRAND


def render(c):
    ui.page_header("Versi Aplikasi", "Melihat volume review dan tingkat keluhan berdasarkan versi yang tercatat.", "VERSION MONITORING")
    if c.vcol is None:
        return ui.empty_state("Informasi versi belum tersedia.")
    fdf = c.fdf
    g = (fdf.assign(v=fdf[c.vcol].fillna("Tidak diketahui").astype(str)).groupby("v")
         .agg(total=("v", "size"), negatif=("is_neg", "sum")).reset_index())
    g["persen_negatif"] = g["negatif"] / g["total"] * 100

    t1, t2 = st.tabs(["📊 Volume review", "⚠️ Tingkat review negatif"])
    with t1:
        top = g.sort_values("total", ascending=False).head(15).sort_values("total")
        fig = px.bar(top, x="total", y="v", orientation="h", text="total", color_discrete_sequence=[BRAND["red"]])
        fig.update_traces(textposition="outside")
        fig.update_layout(xaxis_title="Jumlah review", yaxis_title=None)
        st.plotly_chart(ui.style_fig(fig, 520, legend=False), use_container_width=True)
    with t2:
        min_n = st.slider("Minimal jumlah review per versi", 5, 200, 30,
                          help="Versi dengan review sedikit disembunyikan agar persentasenya tidak menyesatkan.")
        gg = g[g["total"] >= min_n].sort_values("persen_negatif", ascending=False).head(15).sort_values("persen_negatif")
        if gg.empty:
            return ui.empty_state("Tidak ada versi yang memenuhi batas minimal.")
        fig = px.bar(gg, x="persen_negatif", y="v", orientation="h", color_discrete_sequence=[BRAND["navy"]],
                     text=gg["persen_negatif"].map(lambda x: f"{x:.1f}%"), hover_data=["total", "negatif"])
        fig.update_traces(textposition="outside")
        fig.update_layout(xaxis_title="% review negatif", yaxis_title=None)
        st.plotly_chart(ui.style_fig(fig, 520, legend=False), use_container_width=True)
