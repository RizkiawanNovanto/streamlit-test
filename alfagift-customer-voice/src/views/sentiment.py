import plotly.express as px
import streamlit as st

from src import components as ui
from src.components import SENTIMENT_COLORS as SC
from src.config import ORDER


def render(c):
    ui.page_header("Sentiment", "Melihat bagaimana pengalaman pengguna tersebar di tiga kelas sentimen.", "USER EXPERIENCE")
    if c.df.empty or "sentiment" not in c.df.columns:
        return ui.empty_state("Dataset detail belum tersedia.")
    fdf = c.fdf
    a, b = st.columns(2, gap="large")
    with a:
        ui.section_label("JUMLAH PER SENTIMEN")
        counts = (fdf["sentiment"].value_counts().reindex(ORDER).fillna(0).astype(int)
                  .rename_axis("sentiment").reset_index(name="jumlah"))
        fig = px.bar(counts, x="sentiment", y="jumlah", text="jumlah", color="sentiment", color_discrete_map=SC)
        fig.update_traces(textposition="outside")
        fig.update_layout(xaxis_title=None, yaxis_title=None)
        st.plotly_chart(ui.style_fig(fig, 350, legend=False), use_container_width=True)
    with b:
        ui.section_label("SENTIMEN BERDASARKAN RATING")
        if "score" in fdf.columns:
            ct = fdf.groupby(["score", "sentiment"]).size().reset_index(name="jumlah")
            fig = px.bar(ct, x="score", y="jumlah", color="sentiment", color_discrete_map=SC,
                         category_orders={"sentiment": ORDER})
            fig.update_layout(xaxis=dict(tickmode="linear", title="Rating"), yaxis_title=None)
            st.plotly_chart(ui.style_fig(fig, 350), use_container_width=True)

    ui.section_label("CONTOH PENGALAMAN PENGGUNA")
    c1, c2 = st.columns(2)
    pick = c1.selectbox("Sentiment", ["Negatif", "Netral", "Positif"])
    n = c2.select_slider("Jumlah baris", [10, 20, 50, 100, 200], value=20)
    view = fdf[fdf["sentiment"] == pick]
    cols = [x for x in ["content", "score", "reviewCreatedVersion", "at"] if x in view.columns]
    st.dataframe(view[cols].head(n), hide_index=True, use_container_width=True,
                 column_config={"content": st.column_config.TextColumn("Review", width="large")})
