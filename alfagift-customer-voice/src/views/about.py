import streamlit as st

from src import components as ui


def render(c):
    ui.page_header("Tentang Alfagift", "Ringkasan pengalaman yang tersedia di aplikasi.", "APP OVERVIEW")
    ui.info_card("Belanja kebutuhan sehari-hari",
        "Alfagift menjadi kanal digital untuk mencari dan membeli berbagai kebutuhan harian serta melihat penawaran yang tersedia.", "pink")
    a, b = st.columns(2, gap="large")
    with a:
        ui.section_label("PENGALAMAN BELANJA")
        ui.info_card("🛍️ Katalog & Produk", "Pengguna mencari produk, memilih item, memasukkan barang ke keranjang, lalu melanjutkan ke checkout.")
        ui.info_card("🏷️ Promo & Benefit", "Promo, voucher, diskon, dan program membership menjadi bagian dari pengalaman belanja.", "yellow")
        ui.info_card("💳 Order & Pembayaran", "Pengguna menyelesaikan pembelian melalui alur checkout dan metode pembayaran yang tersedia.")
    with b:
        ui.section_label("SETELAH ORDER")
        ui.info_card("🛵 Pengiriman", "Pesanan diproses untuk pengiriman sesuai layanan dan ketersediaan yang dipilih.", "pink")
        ui.info_card("📍 Tracking", "Status pesanan membantu pengguna mengetahui perkembangan order.", "yellow")
        ui.info_card("🎧 Customer Service", "Jalur bantuan diperlukan ketika pengguna mengalami kendala atau membutuhkan penyelesaian masalah.")
