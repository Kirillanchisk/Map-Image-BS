import streamlit as st
import os
from PIL import Image

st.set_page_config(page_title="Map Image", layout="centered")

# ===== Стили =====
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #1f1f1f, #2c2c2c);
        color: white;
    }
    .center {
        text-align: center;
        margin-top: 2rem;
    }
    .btn {
        background-color: #00cc66;
        color: white;
        border: none;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-family: 'Segoe UI', sans-serif;
        border-radius: 8px;
        cursor: pointer;
        transition: 0.3s;
        margin: 1rem;
    }
    .btn:hover {
        background-color: #00b359;
    }
    .footer {
        font-size: 0.75rem;
        text-align: center;
        color: #aaa;
        margin-top: 3rem;
    }
    </style>
""", unsafe_allow_html=True)

# ===== Заголовок и логотип =====
st.markdown("""
<div class="center">
    <img src="logo.png" width="100">
    <h1>Map Image</h1>
</div>
""", unsafe_allow_html=True)

# ===== Загрузка изображения =====
uploaded_file = st.file_uploader("Загрузить изображение", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    with open("output_map.png", "wb") as f:
        f.write(uploaded_file.read())

    st.image("output_map.png", caption="Загруженное изображение", use_container_width=True)

    # ===== Кнопка "Добавить фон" =====
    if st.button("Добавить фон"):
        try:
            os.system("python export.py")

            if os.path.exists("final_image.png"):
                st.image("final_image.png", caption="Финальный результат", use_container_width=True)
            else:
                st.error("Файл final_image.png не найден. Проверь работу export.py.")
        except Exception as e:
            st.error(f"Произошла ошибка при обработке изображения: {e}")

# ===== Футер с лицензией =====
st.markdown("""
    <div class="footer">
        Контент создан при поддержке Brawl Stars Вики.<br>
        Данный контент не связан с компанией Supercell, не поддерживается, не спонсируется и не был утвержден ею, и компания Supercell не несет за него ответственность.<br>
        <a href="https://supercell.com/en/fan-content-policy/" target="_blank" style="color: #00cc66;">
            Правила Supercell для фанатского контента
        </a>
    </div>
""", unsafe_allow_html=True)
