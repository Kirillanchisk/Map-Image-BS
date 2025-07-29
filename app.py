import streamlit as st
from PIL import Image
import subprocess
import os

st.set_page_config(page_title="Map Image Converter", layout="centered", initial_sidebar_state="auto")

# --- Стилизация (темный фон с градиентом)
st.markdown("""
<style>
    html, body, #root > div {
        height: 100%;
        margin: 0;
        padding: 0;
        background: linear-gradient(135deg, #2f2f2f, #1a1a1a);
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-size: 1.2rem;
        font-weight: 600;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        cursor: pointer;
    }
    footer {
        color: #aaa;
        font-size: 0.8rem;
        margin-top: 3rem;
        text-align: center;
    }
    footer a {
        color: #4CAF50;
        text-decoration: none;
    }
    footer a:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main">', unsafe_allow_html=True)

st.title("Map Image")

uploaded_file = st.file_uploader("Загрузить изображение", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Сохраняем загруженный файл локально
    with open("input_image.png", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image("input_image.png", caption="Исходное изображение", use_container_width=True)

    if st.button("Преобразовать в карту"):
        # Запускаем map_converter.py (предполагается, что он есть в проекте)
        try:
            # Подключаем map_converter.py как модуль или запускаем subprocess
            # Запуск через subprocess для изоляции
            subprocess.run(
                ["python3", "map_converter.py", "input_image.png", "output_map.png"],
                check=True
            )
            st.success("Карта успешно создана!")
            st.image("output_map.png", caption="Карта", use_container_width=True)
        except subprocess.CalledProcessError as e:
            st.error(f"Ошибка при конвертации изображения: {e}")

    if os.path.exists("output_map.png"):
        if st.button("Добавить фон"):
            try:
                subprocess.run(["python3", "export.py"], check=True)
                st.success("Фон успешно добавлен!")
                st.image("final_image.png", caption="Финальное изображение", use_container_width=True)
            except subprocess.CalledProcessError as e:
                st.error(f"Ошибка при добавлении фона: {e}")

st.markdown("""
<footer style="color: #aaa; font-size: 0.8rem; margin-top: 3rem;">
    © Brawl Stars Вики<br>
    Данный контент не связан с компанией Supercell, не поддерживается, не спонсируется и не был утвержден ею, и компания Supercell не несет за него ответственность.
    Для получения большей информации смотрите <a href="https://supercell.com/en/fan-content-policy/" target="_blank" style="color:#4CAF50;">Правила Supercell для фанатского контента</a>.
</footer>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
