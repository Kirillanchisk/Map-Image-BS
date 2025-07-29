import streamlit as st
from PIL import Image
import subprocess
import os

st.set_page_config(page_title="Map Image Converter", layout="centered", initial_sidebar_state="auto")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter&display=swap&subset=cyrillic');

body, #root > div {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
                 Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    background-color: #2f2f2f;
    color: white;
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
    font-family: 'Inter', sans-serif;
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
    font-family: 'Inter', sans-serif;
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

uploaded_file = st.file_uploader("ЗАГРУЗИТЬ ИЗОБРАЖЕНИЕ", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    with open("input_image.png", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image("input_image.png", caption="ИСХОДНОЕ ИЗОБРАЖЕНИЕ", use_container_width=True)

    if st.button("Преобразовать в карту"):
        try:
            subprocess.run(
                ["python3", "map_converter.py", "input_image.png", "output_map.png"],
                check=True
            )
            st.success("КАРТА УСПЕШНО СОЗДАНА!")
            st.image("output_map.png", caption="КАРТА С ПРОЗРАЧНЫМ ФОНОМ", use_container_width=True)
        except subprocess.CalledProcessError as e:
            st.error(f"ОШИБКА ПРИ КОНВЕРТАЦИИ ИЗОБРАЖЕНИЯ: {e}")

    if os.path.exists("output_map.png"):
        if st.button("ДОБАВИТЬ ФОН?"):
            try:
                subprocess.run(["python3", "export.py"], check=True)
                st.success("ФОН УСПЕШНО ДОБАВЛЕН!")
                st.image("final_image.png", caption="КАРТА С ФОНОМ", use_container_width=True)
            except subprocess.CalledProcessError as e:
                st.error(f"ОШИБКА ПРИ ДОБАВЛЕНИИ ФОНА: {e}")

st.markdown("""
<footer style="color: #aaa; font-size: 0.8rem; margin-top: 3rem;">
    © Brawl Stars Вики<br>
    Данный контент не связан с компанией Supercell, не поддерживается, не спонсируется и не был утвержден ею, и компания Supercell не несет за него ответственность.
    Для получения большей информации смотрите <a href="https://supercell.com/en/fan-content-policy/" target="_blank" style="color:#4CAF50;">Правила Supercell для фанатского контента</a>.
</footer>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
