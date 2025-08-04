import streamlit as st
import subprocess
import os

st.set_page_config(page_title="BSW — Map Image", layout="centered", initial_sidebar_state="auto")

st.markdown("""
<style>
body, html, [class*="css"] {
    background-color: #2f2f2f;
    color: white;
    font-family: sans-serif;
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
    min-width: 240px;
    transition: background-color 0.3s ease;
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

final_image_path = None

if uploaded_file is not None:
    with open("input_image.png", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image("input_image.png", caption="ИСХОДНОЕ ИЗОБРАЖЕНИЕ", use_container_width=True)

    add_background = st.checkbox(
        "Добавить фон?", 
        value=True, 
        help="Рекомендуем добавить серый фон к карте для лучшего вида изображения. Если вам нужен прозрачный фон, то не используйте эту функцию."
    )

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
<hr style="border-color: #555;">
<div style="text-align: center; color: #aaa; font-size: 0.9rem; margin-top: 1rem;">
    Сайт Map Image предназначен для преобразования изображений в карту размером 60x60 блоков из Brawl Stars. Мы не несём ответственности за созданный контент. Проект находится в разработке. Благодарим за использование и продвижение.<br><br><br>
    Данный контент не связан с компанией Supercell, не поддерживается, не спонсируется и не был утвержден ею. Для получения большей информации смотрите <a href="https://supercell.com/en/fan-content-policy/" target="_blank" style="color:#4CAF50;">Правила Supercell для фанатского контента</a>.<br><br>
    © Brawl Stars Вики 2025<br><br>
    <a href="https://discord.gg/KGKVGbrWH8" target="_blank" style="color:#4CAF50;">Discord</a> • <a href="https://t.me/bswlab" target="_blank" style="color:#4CAF50;">Telegram</a> • <a href="https://brawlstars.fandom.com/ru/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0" target="_blank" style="color:#4CAF50;">Вики</a>

</div>
""", unsafe_allow_html=True)
