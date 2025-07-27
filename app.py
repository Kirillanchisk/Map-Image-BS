import streamlit as st
from PIL import Image
import numpy as np
import os
from map_converter import convert_image_to_map  # импорт твоей функции из другого файла

st.title("Brawl Stars Map Converter")

uploaded_file = st.file_uploader("Загрузите изображение", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    input_img = Image.open(uploaded_file)
    input_img.save("temp_input.png")

    output_path = "output_map.png"
    convert_image_to_map("temp_input.png", output_path)

    result_img = Image.open(output_path)
    st.image(result_img, caption="Конвертированная карта")
