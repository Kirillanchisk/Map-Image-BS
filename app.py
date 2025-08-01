import streamlit as st
from PIL import Image
import subprocess
import os

st.set_page_config(page_title="BSW — Map Image", layout="centered", initial_sidebar_state="auto")

st.markdown("""
<style>
@font-face {
    font-family: 'Lilita One';
    src: url('https://fankit.supercell.com/api/assets/YvtsWV4pUQVm/files/LilitaOne-Regular.ttf') format('truetype');
    font-weight: normal;
    font-style: normal;
}

body, html, [class*="css"] {
    font-family: 'Lilita One', sans-serif;
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
    font-family: 'Lilita One', sans-serif;
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
    font-family: 'Lilita One', sans-serif;
    transition: background-color 0.3s ease;
    min-width: 240px;
}

.stButton>button:hover {
    background-color: #45a049;
    cursor: pointer;
}

footer {
    color: #aaa;
    font-size: 0.9rem;
    margin-top: 3rem;
    text-align: center;
    font-family: 'Lilita One', sans-serif;
}

footer a {
    color: #4CAF50;
    text-decoration: none;
}

footer a:hover {
    text-decoration: underline;
}

footer img {
    margin-top: 1rem;
    width: 80px;
    opacity: 0.8;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1>MAP IMAGE</h1>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("ЗАГРУЗИТЬ ИЗОБРАЖЕНИЕ", type=["png", "jpg", "jpeg"])

final_image_path = None

if uploaded_file is not None:
    with open("input_image.png", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image("input_image.png", caption="ИСХОДНОЕ ИЗОБРАЖЕНИЕ", use_container_width=True)

    add_background = st.checkbox("Добавить фон", value=True, help="Рекомендуем добавить серый фон к карте для лучшего вида изображения.")

    if st.button("ПРЕОБРАЗОВАТЬ В КАРТУ"):
        try:
            subprocess.run(["python3", "map_converter.py", "input_image.png", "output_map.png"], check=True)

            if add_background:
                subprocess.run(["python3", "export.py"], check=True)
                final_image_path = "final_image.png"
                st.success("КАРТА С ФОНОМ УСПЕШНО СОЗДАНА!")
                st.image(final_image_path, caption="КАРТА С ФОНОМ", use_container_width=True)
            else:
                final_image_path = "output_map.png"
                st.success("КАРТА С ПРОЗРАЧНЫМ ФОНОМ УСПЕШНО СОЗДАНА!")
                st.image(final_image_path, caption="КАРТА С ПРОЗРАЧНЫМ ФОНОМ", use_container_width=True)

        except subprocess.CalledProcessError as e:
            st.error(f"ОШИБКА ПРИ ОБРАБОТКЕ ИЗОБРАЖЕНИЯ: {e}")

    if final_image_path and os.path.exists(final_image_path):
        with open(final_image_path, "rb") as file:
            st.download_button(
                label="СКАЧАТЬ",
                data=file,
                file_name=final_image_path,
                mime="image/png"
            )

st.markdown("""
<footer>
    Сайт Map Image предназначен для преобразования изображений в игровую карту размером 60х60 блоков из Brawl Stars. Мы не несём ответственности за созданный контент на сайте. Проект находится в стадии разработки. Благодарим за использование и продвижение.<br><br>
    Данный контент не связан с компанией Supercell, не поддерживается, не спонсируется и не был утвержден ею, и компания Supercell не несет за него ответственность. Для получения большей информации смотрите <a href="https://supercell.com/en/fan-content-policy/" target="_blank">Правила Supercell для фанатского контента</a>.<br>
    © Brawl Stars Вики 2025<br>
    <img src="logo.png" alt="logo">
</footer>
""", unsafe_allow_html=True)
