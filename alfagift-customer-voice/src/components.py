"""UI components & design system - Alfagift Customer Voice Analytics."""
import base64
import html
import re
from pathlib import Path

import streamlit as st

# ----------------------------------------------------------------------------
# DESIGN TOKENS (warna mengacu ke identitas Alfagift: merah, biru, kuning)
# ----------------------------------------------------------------------------
BRAND = {
    "red": "#E4002B", "red_dark": "#B30022", "red_soft": "#FDECEE",
    "navy": "#0B3A82", "navy_soft": "#EAF0FA",
    "yellow": "#FFC72C", "yellow_soft": "#FFF6D9",
    "ink": "#2B2B35", "muted": "#6B7280", "line": "#ECE7E7",
    "bg": "#FAF8F8", "card": "#FFFFFF",
}
SENTIMENT_COLORS = {"Positif": "#1E9E5A", "Netral": "#F5B000", "Negatif": "#E4002B"}

LOGO_NAMES = ["alfagift_logo.png", "alfagift_logo.jpg", "alfagift_logo.svg", "logo.png"]
LOGO_DIRS = [Path(__file__).resolve().parents[1] / "assets"]


def _md(markup: str):
    """Render HTML lewat st.markdown (hapus newline agar tidak dibaca sebagai code block)."""
    st.markdown(re.sub(r"\n\s*", "", markup), unsafe_allow_html=True)


def esc(text) -> str:
    """Escape teks review sebelum disisipkan ke HTML."""
    return html.escape(str(text))


# ----------------------------------------------------------------------------
# LOGO
# ----------------------------------------------------------------------------
def _logo_data_uri():
    for folder in LOGO_DIRS:
        for name in LOGO_NAMES:
            p = folder / name
            if p.exists():
                mime = {"png": "image/png", "jpg": "image/jpeg", "svg": "image/svg+xml"}[p.suffix[1:]]
                return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"
    return None


def logo_html(height=34) -> str:
    uri = _logo_data_uri()
    if uri:
        return f'<img src="{uri}" style="height:{height}px;display:block;" alt="Alfagift">'
    # Fallback wordmark bila file logo belum tersedia
    return (f'<span style="font-weight:900;font-size:{height*0.62}px;letter-spacing:-.03em;'
            f'color:{BRAND["red"]};">alfa</span>'
            f'<span style="font-weight:900;font-size:{height*0.62}px;letter-spacing:-.03em;'
            f'color:{BRAND["navy"]};">gift</span>')


# ----------------------------------------------------------------------------
# GLOBAL CSS
# ----------------------------------------------------------------------------
def inject_css():
    b = BRAND
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"], .stApp {{ font-family:'Plus Jakarta Sans',sans-serif; }}
:root {{ color-scheme:light; }}
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{ background:{b['bg']}; color:{b['ink']}; }}
.block-container {{ max-width:1400px; padding:3.2rem 2rem 2.5rem; }}
#MainMenu, footer {{ visibility:hidden; }}
header[data-testid="stHeader"] {{ background:transparent; }}
[data-testid="stSidebarCollapseButton"] button {{ background:{b['red_soft']}; color:{b['red']}; border-radius:10px; }}
[data-testid="stExpandSidebarButton"], [data-testid="collapsedControl"] {{
    background:{b['red']}; color:#fff; border-radius:0 14px 14px 0; box-shadow:0 4px 14px rgba(228,0,43,.35); }}
[data-testid="stExpandSidebarButton"] *, [data-testid="collapsedControl"] * {{ color:#fff !important; fill:#fff !important; }}
h1,h2,h3 {{ color:{b['ink']}; letter-spacing:-.02em; font-weight:800; }}

/* Sidebar */
[data-testid="stSidebar"] {{ background:#fff; border-right:1px solid {b['line']}; }}
[data-testid="stSidebar"] > div:first-child {{ background:#fff; }}
[data-testid="stSidebar"] .block-container {{ padding-top:1rem; }}
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] {{ gap:4px; }}
[data-testid="stSidebar"] [data-testid="stRadio"] label {{
    padding:9px 12px; border-radius:10px; transition:.15s; width:100%; margin:0; cursor:pointer; }}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {{ background:{b['red_soft']}; }}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {{ background:{b['red']}; }}
[data-testid="stSidebar"] [data-testid="stRadio"] label p {{ color:{b['ink']}; font-weight:600; font-size:.9rem; margin:0; }}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p {{ color:#fff !important; font-weight:700; }}
/* sembunyikan bulatan radio (apa pun urutan elemennya), sisakan teks menu */
[data-testid="stSidebar"] [data-testid="stRadio"] label > div:not([data-testid="stMarkdownContainer"]):not(:has([data-testid="stMarkdownContainer"])) {{ display:none; }}
.side-brand {{ padding:4px 6px 14px; border-bottom:3px solid {b['yellow']}; margin-bottom:14px; }}
.side-sub {{ color:{b['muted']}; font-size:.72rem; margin-top:6px; letter-spacing:.04em; }}
.side-chip {{ background:{b['navy_soft']}; color:{b['navy']}; border-radius:10px;
    padding:9px 12px; font-size:.76rem; font-weight:600; margin-top:8px; }}

/* Hero & page header */
.hero {{ background:linear-gradient(120deg,{b['red']} 0%,{b['red_dark']} 100%);
    border-radius:22px; padding:24px 28px; margin-bottom:18px; color:#fff;
    display:flex; justify-content:space-between; align-items:center; gap:20px;
    box-shadow:0 10px 28px rgba(228,0,43,.18); position:relative; overflow:hidden; }}
.hero::after {{ content:""; position:absolute; right:-40px; top:-60px; width:220px; height:220px;
    border-radius:50%; background:rgba(255,199,44,.22); }}
.hero-tag {{ display:inline-block; background:{b['yellow']}; color:{b['ink']}; font-weight:800;
    font-size:.66rem; letter-spacing:.1em; padding:4px 10px; border-radius:999px; }}
.hero-title {{ font-size:1.8rem; font-weight:800; line-height:1.1; margin-top:9px; }}
.hero-sub {{ font-size:.88rem; opacity:.92; margin-top:6px; max-width:620px; }}
.hero-logo {{ background:#fff; border-radius:14px; padding:10px 16px; z-index:1; }}

.page-head {{ background:#fff; border:1px solid {b['line']}; border-left:5px solid {b['red']};
    border-radius:16px; padding:16px 20px; margin-bottom:18px; }}
.page-badge {{ color:{b['red']}; font-size:.68rem; font-weight:800; letter-spacing:.12em; }}
.page-title {{ font-size:1.5rem; font-weight:800; color:{b['ink']}; margin-top:2px; }}
.page-sub {{ color:{b['muted']}; font-size:.85rem; margin-top:3px; }}

.section-label {{ display:flex; align-items:center; gap:8px; color:{b['navy']};
    font-size:.72rem; font-weight:800; letter-spacing:.12em; margin:4px 0 10px; }}
.section-label::before {{ content:""; width:18px; height:3px; border-radius:3px; background:{b['yellow']}; }}

/* Cards */
.card {{ background:#fff; border:1px solid {b['line']}; border-radius:16px; padding:14px 16px;
    margin-bottom:10px; box-shadow:0 1px 2px rgba(0,0,0,.03); }}
.card-title {{ font-weight:800; font-size:.9rem; color:{b['ink']}; }}
.card-body {{ color:{b['muted']}; font-size:.8rem; line-height:1.55; margin-top:5px; }}
.card.pink {{ background:{b['red_soft']}; border-color:#F7C9D0; }}
.card.yellow {{ background:{b['yellow_soft']}; border-color:#F2DC9B; }}
.card.blue {{ background:{b['navy_soft']}; border-color:#C9D7EF; }}

.kpi {{ background:#fff; border:1px solid {b['line']}; border-radius:16px; padding:16px 18px;
    min-height:108px; border-top:4px solid var(--accent); box-shadow:0 1px 2px rgba(0,0,0,.03); }}
.kpi-label {{ color:{b['muted']}; font-size:.76rem; font-weight:600; }}
.kpi-value {{ color:{b['ink']}; font-size:1.7rem; font-weight:800; margin-top:6px; line-height:1.1; }}
.kpi-note {{ color:#9CA3AF; font-size:.72rem; margin-top:5px; }}

.rank {{ background:#fff; border:1px solid {b['line']}; border-radius:14px; padding:12px 14px; margin-bottom:8px; }}
.rank-top {{ display:flex; justify-content:space-between; align-items:center; font-weight:700; font-size:.88rem; }}
.rank-num {{ display:inline-flex; width:24px; height:24px; border-radius:8px; background:{b['red']};
    color:#fff; font-size:.75rem; font-weight:800; align-items:center; justify-content:center; margin-right:9px; }}
.rank-bar {{ height:6px; background:#F3EEEE; border-radius:6px; margin-top:9px; overflow:hidden; }}
.rank-bar > div {{ height:100%; border-radius:6px; background:linear-gradient(90deg,{b['red']},{b['yellow']}); }}
.rank-meta {{ color:{b['muted']}; font-size:.73rem; margin-top:6px; }}

.issue {{ background:#fff; border:1px solid {b['line']}; border-radius:18px; padding:18px 20px;
    margin-bottom:6px; box-shadow:0 1px 2px rgba(0,0,0,.03); }}
.issue-head {{ display:flex; align-items:center; gap:12px; }}
.issue-icon {{ width:42px; height:42px; border-radius:12px; background:{b['red_soft']};
    display:flex; align-items:center; justify-content:center; font-size:1.25rem; }}
.issue-title {{ font-size:1.05rem; font-weight:800; color:{b['ink']}; }}
.issue-meta {{ color:{b['muted']}; font-size:.76rem; margin-top:2px; }}
.pill {{ margin-left:auto; background:{b['red']}; color:#fff; font-weight:800; font-size:.78rem;
    padding:5px 12px; border-radius:999px; white-space:nowrap; }}
.issue-body {{ color:#4B5563; font-size:.83rem; line-height:1.6; margin-top:12px; }}
.reco {{ background:{b['yellow_soft']}; border:1px solid #F2DC9B; border-left:4px solid {b['yellow']};
    border-radius:12px; padding:11px 14px; margin-top:12px; }}
.reco b {{ color:#8A6A00; font-size:.7rem; text-transform:uppercase; letter-spacing:.07em; }}
.reco div {{ color:#5C4A12; font-size:.82rem; line-height:1.5; margin-top:3px; }}
.quote {{ border-left:3px solid {b['red']}; background:{b['bg']}; padding:8px 12px;
    color:#4B5563; font-size:.8rem; line-height:1.5; margin:8px 0; border-radius:0 8px 8px 0; }}
.empty {{ text-align:center; background:#fff; border:1px dashed #E5C9CD; border-radius:16px;
    padding:28px 20px; color:{b['muted']}; font-size:.85rem; }}
.footer {{ color:#9CA3AF; font-size:.72rem; text-align:center; padding-top:26px; }}

.quote-meta {{ color:#9CA3AF; font-size:.7rem; margin-top:4px; font-weight:600; }}
.trend {{ font-weight:700; font-size:.72rem; padding:2px 8px; border-radius:999px; margin-left:6px; }}
.trend.up {{ background:{b['red_soft']}; color:{b['red']}; }}
.trend.down {{ background:#E6F6EC; color:#1E9E5A; }}
.note {{ background:#fff; border:1px solid {b['line']}; border-radius:12px; padding:8px 14px;
    font-size:.78rem; color:{b['muted']}; margin-bottom:14px; }}
.stTabs [data-baseweb="tab"] {{ font-weight:700; }}
.stTabs [aria-selected="true"] {{ color:{b['red']}; }}
.stTabs [data-baseweb="tab-highlight"] {{ background:{b['red']}; }}
.chip {{ display:inline-block; padding:3px 10px; border-radius:999px; font-size:.74rem; font-weight:700; margin:0 6px 6px 0; background:{b['navy_soft']}; color:{b['navy']}; }}
.chip.red {{ background:{b['red_soft']}; color:{b['red']}; }}
.chip.yellow {{ background:{b['yellow_soft']}; color:#8A6A00; }}
.chip.green {{ background:#E6F6EC; color:#1E9E5A; }}
.banner {{ border-radius:16px; padding:16px 20px; margin:6px 0 16px; display:flex; gap:14px; align-items:flex-start; border:1px solid; }}
.banner.red {{ background:{b['red_soft']}; border-color:#F7C9D0; }}
.banner.yellow {{ background:{b['yellow_soft']}; border-color:#F2DC9B; }}
.banner.green {{ background:#E6F6EC; border-color:#BFE6CD; }}
.banner-icon {{ font-size:1.7rem; line-height:1.1; }}
.banner-title {{ font-weight:800; font-size:1rem; color:{b['ink']}; }}
.banner-text {{ color:#4B5563; font-size:.84rem; line-height:1.55; margin-top:3px; }}
.pbar-row {{ display:flex; align-items:center; gap:10px; margin:10px 0; font-size:.82rem; }}
.pbar-label {{ width:62px; font-weight:700; color:{b['ink']}; }}
.pbar-track {{ flex:1; height:10px; background:#F3EEEE; border-radius:10px; overflow:hidden; }}
.pbar-fill {{ height:100%; border-radius:10px; }}
.pbar-val {{ width:44px; text-align:right; font-weight:700; color:{b['ink']}; }}
.steps {{ counter-reset:s; margin:8px 0 0; padding:0; list-style:none; }}
.steps li {{ position:relative; padding:9px 0 9px 40px; font-size:.84rem; color:#374151; line-height:1.5; border-bottom:1px dashed {b['line']}; }}
.steps li:last-child {{ border-bottom:none; }}
.steps li::before {{ counter-increment:s; content:counter(s); position:absolute; left:0; top:8px; width:26px; height:26px; border-radius:9px;
    background:{b['red']}; color:#fff; font-weight:800; font-size:.78rem; display:flex; align-items:center; justify-content:center; }}
.steps.soft li::before {{ background:{b['navy']}; }}
.owner {{ margin-top:10px; font-size:.78rem; color:{b['muted']}; }}
.owner b {{ color:{b['navy']}; }}
.stars {{ color:{b['yellow']}; letter-spacing:2px; }}
button[kind="primary"], button[kind="primaryFormSubmit"] {{ background:{b['red']}; border-color:{b['red']}; color:#fff; border-radius:12px; font-weight:700; }}
button[kind="primary"]:hover, button[kind="primaryFormSubmit"]:hover {{ background:{b['red_dark']}; border-color:{b['red_dark']}; color:#fff; }}
[data-testid="stVerticalBlockBorderWrapper"] {{ border-radius:16px; }}
[data-testid="stTextArea"] textarea {{ border-radius:12px; }}
/* Streamlit widgets */
[data-testid="stExpander"] {{ border:1px solid {b['line']}; border-radius:12px; background:#fff; margin-bottom:14px; }}
[data-testid="stDataFrame"] {{ border:1px solid {b['line']}; border-radius:12px; overflow:hidden; }}
/* Widget: paksa tampilan terang supaya tidak bentrok dengan dark mode browser/OS */
[data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] * {{ color:{b['ink']} !important; font-weight:600; }}
[data-testid="stMain"] [data-testid="stMarkdownContainer"] p {{ color:{b['ink']}; }}
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * {{ color:{b['muted']} !important; }}
[data-baseweb="select"] > div, [data-baseweb="base-input"], [data-baseweb="input"], [data-baseweb="textarea"] {{
    background:#fff !important; border-color:#E3DCDC !important; border-radius:10px; }}
[data-baseweb="select"] *, [data-baseweb="base-input"] input, textarea,
input:not([type="radio"]):not([type="checkbox"]) {{ color:{b['ink']} !important; background-color:transparent; }}
[data-baseweb="select"] svg {{ fill:{b['muted']}; }}
[data-baseweb="popover"] ul, [data-baseweb="popover"] [data-baseweb="menu"], [data-baseweb="calendar"] {{
    background:#fff !important; color:{b['ink']} !important; }}
[data-baseweb="popover"] li {{ color:{b['ink']} !important; background:#fff; }}
[data-baseweb="popover"] li:hover, [data-baseweb="popover"] li[aria-selected="true"] {{ background:{b['red_soft']} !important; }}
[data-baseweb="tag"] {{ background:{b['red_soft']} !important; border-radius:8px; }}
[data-baseweb="tag"] span, [data-baseweb="tag"] svg {{ color:{b['red']} !important; fill:{b['red']} !important; }}
[data-testid="stExpander"] details, [data-testid="stExpander"] summary {{ background:#fff; color:{b['ink']}; }}
[data-testid="stExpander"] summary * {{ color:{b['ink']} !important; font-weight:600; }}
button[kind="secondary"] {{ background:#fff; color:{b['ink']}; border:1px solid #E3DCDC; border-radius:12px; font-weight:600; }}
button[kind="secondary"]:hover {{ border-color:{b['red']}; color:{b['red']}; background:{b['red_soft']}; }}
button[kind="secondary"] p {{ color:inherit !important; }}
.stTabs [data-baseweb="tab"] {{ color:{b['muted']}; }}
[data-testid="stMain"] [data-testid="stRadio"] label p {{ color:{b['ink']}; }}
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# COMPONENTS
# ----------------------------------------------------------------------------
def sidebar_brand(subtitle="Dashboard Skripsi Rizkiawan Novanto 2026"):
    st.sidebar.markdown(
        f'<div class="side-brand">{logo_html(54)}<div class="side-sub">{esc(subtitle)}</div></div>',
        unsafe_allow_html=True)


def sidebar_chip(text):
    st.sidebar.markdown(f'<div class="side-chip">{text}</div>', unsafe_allow_html=True)


def hero(tag, title, subtitle):
    _md(f"""<div class="hero"><div style="z-index:1;">
        <span class="hero-tag">{esc(tag)}</span>
        <div class="hero-title">{esc(title)}</div>
        <div class="hero-sub">{esc(subtitle)}</div></div>
        <div class="hero-logo">{logo_html(58)}</div></div>""")


def page_header(title, subtitle, badge=""):
    _md(f"""<div class="page-head"><div class="page-badge">{esc(badge)}</div>
        <div class="page-title">{esc(title)}</div>
        <div class="page-sub">{esc(subtitle)}</div></div>""")


def section_label(text):
    _md(f'<div class="section-label">{esc(text)}</div>')


def metric_card(column, label, value, note="", accent=None):
    accent = accent or BRAND["red"]
    column.markdown(re.sub(r"\n\s*", "", f"""<div class="kpi" style="--accent:{accent};">
        <div class="kpi-label">{esc(label)}</div><div class="kpi-value">{esc(value)}</div>
        <div class="kpi-note">{esc(note)}</div></div>"""), unsafe_allow_html=True)


def info_card(title, body, tone="plain"):
    _md(f'<div class="card {tone}"><div class="card-title">{esc(title)}</div>'
        f'<div class="card-body">{esc(body)}</div></div>')


def insight_card(title, body, tone="plain"):
    info_card(title, body, tone)


def rank_card(rank, name, count, pct, trend=None):
    _md(f"""<div class="rank"><div class="rank-top"><span><span class="rank-num">{rank}</span>{esc(name)}</span>
        <span>{count:,}</span></div>
        <div class="rank-bar"><div style="width:{min(pct,100):.1f}%;"></div></div>
        <div class="rank-meta">{pct:.1f}% dari review negatif{_trend(trend)}</div></div>""")


def issue_card(name, icon, count, pct, description, recommendation, trend=None):
    _md(f"""<div class="issue"><div class="issue-head"><div class="issue-icon">{icon}</div>
        <div><div class="issue-title">{esc(name)}</div>
        <div class="issue-meta">{count:,} review negatif • {pct:.1f}% dari seluruh review negatif{_trend(trend)}</div></div>
        <div class="pill">{pct:.1f}%</div></div>
        <div class="issue-body"><b>Yang terlihat dari review</b><br>{esc(description)}</div>
        <div class="reco"><b>Rekomendasi perbaikan</b><div>{esc(recommendation)}</div></div></div>""")


def quote(text, meta=""):
    m = f'<div class="quote-meta">{esc(meta)}</div>' if meta else ""
    _md(f'<div class="quote">“{esc(text)}”{m}</div>')


def note(markup):
    _md(f'<div class="note">{markup}</div>')


def _trend(t):
    return f'<span class="trend {t[1]}">{esc(t[0])}</span>' if t else ""


def empty_state(message):
    _md(f'<div class="empty">📭<br>{esc(message)}</div>')


def style_fig(fig, height=380, legend=True):
    """Seragamkan tampilan grafik Plotly."""
    fig.update_layout(
        height=height, margin=dict(l=8, r=8, t=10, b=8), showlegend=legend, legend_title=None,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color=BRAND["ink"], size=12),
        legend=dict(orientation="h", y=-0.12, x=0.5, xanchor="center"),
    )
    fig.update_xaxes(showgrid=False, linecolor=BRAND["line"])
    fig.update_yaxes(gridcolor="#F1ECEC", zeroline=False)
    return fig


def footer(text):
    _md(f'<div class="footer">{esc(text)}</div>')


def chips(items, tone="plain"):
    return "".join(f'<span class="chip {tone}">{esc(i)}</span>' for i in items)


def banner(title, text, tone="yellow", icon="💡"):
    _md(f'<div class="banner {tone}"><div class="banner-icon">{icon}</div><div><div class="banner-title">{esc(title)}</div>'
        f'<div class="banner-text">{esc(text)}</div></div></div>')


def prob_bars(probs, colors, best=None):
    rows = ""
    for k, v in probs.items():
        op = 1 if k == best else 0.55
        rows += (f'<div class="pbar-row"><div class="pbar-label">{esc(k)}</div><div class="pbar-track">'
                 f'<div class="pbar-fill" style="width:{v*100:.1f}%;background:{colors[k]};opacity:{op};"></div></div>'
                 f'<div class="pbar-val">{v*100:.0f}%</div></div>')
    _md(f'<div class="card">{rows}</div>')


def action_card(icon, title, meta, chips_html, steps, owner, soft=False):
    lis = "".join(f"<li>{esc(x)}</li>" for x in steps)
    _md(f'<div class="issue"><div class="issue-head"><div class="issue-icon">{icon}</div><div><div class="issue-title">{esc(title)}</div>'
        f'<div class="issue-meta">{esc(meta)}</div></div></div>'
        + (f'<div class="issue-body" style="margin-top:10px;">{chips_html}</div>' if chips_html else "")
        + '<div class="issue-body" style="margin-top:6px;"><b>Yang sebaiknya dilakukan</b></div>'
        + f'<ol class="steps{" soft" if soft else ""}">{lis}</ol>'
        + (f'<div class="owner">Tim yang relevan: <b>{esc(owner)}</b></div>' if owner else "") + '</div>')


def stars_text(n):
    return "★" * n + "☆" * (5 - n)
