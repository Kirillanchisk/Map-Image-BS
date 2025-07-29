import streamlit as st
from PIL import Image
import subprocess
import os

st.set_page_config(page_title="Map Image by BSW", layout="centered", initial_sidebar_state="auto")

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

h1 {
    text-align: center;
    font-weight: 800;
    font-size: 3rem;
    margin-bottom: 2rem;
}

.stButton>button {
    display: block;
    margin: 1rem auto;
    background-color: #4CAF50;
    color: white;
    border-radius: 12px;
    padding: 0.75rem 1.5rem;
    font-size: 1.2rem;
    font-weight: 700;
    border: none;
    font-family: 'Inter', sans-serif;
    transition: background-color 0.3s ease;
    min-width: 240px;
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

st.markdown('<h1>MAP IMAGE</h1>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("ЗАГРУЗИТЬ ИЗОБРАЖЕНИЕ", type=["png", "jpg", "jpeg"])

converted = False
background_added = False

if uploaded_file is not None:
    with open("input_image.png", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image("input_image.png", caption="ИСХОДНОЕ ИЗОБРАЖЕНИЕ", use_container_width=True)

    if st.button("ПРЕОБРАЗОВАТЬ В КАРТУ"):
        try:
            subprocess.run(
                ["python3", "map_converter.py", "input_image.png", "output_map.png"],
                check=True
            )
            st.success("КАРТА УСПЕШНО СОЗДАНА!")
            st.image("output_map.png", caption="КАРТА С ПРОЗРАЧНЫМ ФОНОМ", use_container_width=True)
            converted = True
        except subprocess.CalledProcessError as e:
            st.error(f"ОШИБКА ПРИ КОНВЕРТАЦИИ ИЗОБРАЖЕНИЯ: {e}")

    if os.path.exists("output_map.png"):
        if st.button("ДОБАВИТЬ ФОН?"):
            try:
                subprocess.run(["python3", "export.py"], check=True)
                st.success("ФОН УСПЕШНО ДОБАВЛЕН!")
                st.image("final_image.png", caption="КАРТА С ФОНОМ", use_container_width=True)
                background_added = True
            except subprocess.CalledProcessError as e:
                st.error(f"ОШИБКА ПРИ ДОБАВЛЕНИИ ФОНА: {e}")

    download_path = "final_image.png" if background_added and os.path.exists("final_image.png") else "output_map.png"
    if os.path.exists(download_path):
        with open(download_path, "rb") as file:
            st.download_button(
                label="СКАЧАТЬ",
                data=file,
                file_name=download_path,
                mime="image/png",
                key="download-btn"
            )

st.markdown("""
<footer>
    © Brawl Stars Вики<br><br>
    Данный контент не связан с компанией Supercell, не поддерживается, не спонсируется и не был утвержден ею, и компания Supercell не несет за него ответственность.
    Для получения большей информации смотрите <a href="https://supercell.com/en/fan-content-policy/" target="_blank">Правила Supercell для фанатского контента</a>.
</footer>
""", unsafe_allow_html=True)
