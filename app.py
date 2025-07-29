import streamlit as st
from PIL import Image
import os

st.set_page_config(page_title="Map Image", layout="centered")

st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #1c1c1c, #2a2a2a);
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }
    .main {
        padding-top: 50px;
    }
    .upload-btn {
        background-color: #22c55e;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 25px;
        font-size: 18px;
        font-weight: 600;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .upload-btn:hover {
        background-color: #16a34a;
    }
    .footer {
        font-size: 12px;
        color: #aaa;
        margin-top: 80px;
        text-align: center;
    }
    .footer a {
        color: #aaa;
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

logo_path = "logo.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=120)

st.markdown("""
    <h1 style='text-align: center; font-size: 48px; margin-bottom: 30px;'>Map Image</h1>
""", unsafe_allow_html=True)

st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
input_file = st.file_uploader(" ", type=["png"], label_visibility="collapsed")
if input_file:
    with open("input_image.png", "wb") as f:
        f.write(input_file.read())
    st.image("input_image.png", caption="Загруженное изображение", use_column_width=True)
    os.system("python map_converter.py input_image.png output_map.png")
    st.success("Изображение преобразовано!")
    st.image("output_map.png", caption="Результат", use_column_width=True)

    if st.button("Добавить фон", key="bg_button"):
        os.system("python export.py")
        st.success("Фон добавлен!")
        st.image("final_output.png", caption="Финальный результат", use_column_width=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
    <div class="footer">
        <p>Контент предоставлен Brawl Stars Wiki</p>
        <p>Данный контент не связан с компанией Supercell, не поддерживается, не спонсируется и не был утвержден ею, и компания Supercell не несет за него ответственность.<br>
        Для получения большей информации смотрите <a href="https://supercell.com/en/fan-content-policy/" target="_blank">Правила Supercell для фанатского контента</a>.</p>
    </div>
""", unsafe_allow_html=True)
