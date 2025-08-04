from PIL import Image
import numpy as np
import os
import sys

BLOCKS_DIR = 'blocks/'
BLOCK_WIDTH = 20
BLOCK_HEIGHT = 20
LAST_ROW_HEIGHT = 30
MAP_SIZE = 60
WATERMARK_PATH = 'watermark.png' 

def average_color(img):
    np_img = np.array(img)
    if np_img.ndim == 3 and np_img.shape[2] == 4:
        alpha = np_img[:, :, 3] / 255
        rgb = np_img[:, :, :3]
        weighted = rgb * alpha[:, :, np.newaxis]
        avg = weighted.sum(axis=(0, 1)) / alpha.sum()
    else:
        avg = np_img[:, :, :3].mean(axis=(0, 1))
    return avg

def load_blocks():
    block_images = []
    block_colors = []
    for filename in os.listdir(BLOCKS_DIR):
        if filename.endswith(".png"):
            path = os.path.join(BLOCKS_DIR, filename)
            original = Image.open(path).convert("RGBA")
            w, h = original.size
            resized = original.resize((BLOCK_WIDTH, int(h * (BLOCK_WIDTH / w))), Image.LANCZOS)
            avg_color = average_color(resized.crop((0, 0, BLOCK_WIDTH, BLOCK_HEIGHT)))
            block_images.append(resized)
            block_colors.append(avg_color)
    if not block_images:
        raise ValueError(f"В папке {BLOCKS_DIR} нет PNG-файлов с блоками!")
    return block_images, np.array(block_colors)

def find_best_block(pixel_color, block_colors):
    distances = np.linalg.norm(block_colors - pixel_color, axis=1)
    return np.argmin(distances)

def add_watermark(base_image):
    if not os.path.exists(WATERMARK_PATH):
        print(f"Внимание: файл ватермарки '{WATERMARK_PATH}' не найден. Пропускаю.")
        return base_image

    watermark = Image.open(WATERMARK_PATH).convert("RGBA")
    max_w = base_image.width // 5
    max_h = base_image.height // 5
    if watermark.width > max_w or watermark.height > max_h:
        ratio = min(max_w / watermark.width, max_h / watermark.height)
        new_size = (int(watermark.width * ratio), int(watermark.height * ratio))
        watermark = watermark.resize(new_size, Image.LANCZOS)
    alpha = watermark.split()[3].point(lambda p: p * 0.8)
    watermark.putalpha(alpha)
    x = base_image.width - watermark.width - 10
    y = base_image.height - watermark.height - 10

    base_image.paste(watermark, (x, y), mask=watermark)
    return base_image

def convert_image_to_map(image_path, output_path):
    print("Загрузка блоков...")
    block_images, block_colors = load_blocks()

    print(f"Обработка изображения: {image_path}")
    input_img = Image.open(image_path).convert("RGB").resize((MAP_SIZE, MAP_SIZE))
    input_pixels = np.array(input_img)

    final_image_height = (MAP_SIZE - 1) * BLOCK_HEIGHT + LAST_ROW_HEIGHT
    final_image = Image.new("RGBA", (MAP_SIZE * BLOCK_WIDTH, final_image_height))

    for y in range(MAP_SIZE):
        for x in range(MAP_SIZE):
            pixel_color = input_pixels[y, x]
            idx = find_best_block(pixel_color, block_colors)
            block = block_images[idx]

            block_height = block.height
            y_pixel = y * BLOCK_HEIGHT if y < MAP_SIZE - 1 else (MAP_SIZE - 1) * BLOCK_HEIGHT

            num_slices = (block_height + BLOCK_HEIGHT - 1) // BLOCK_HEIGHT
            for i in range(num_slices):
                top = i * BLOCK_HEIGHT
                bottom = min(top + BLOCK_HEIGHT, block_height)
                slice_img = block.crop((0, top, BLOCK_WIDTH, bottom))

                target_y = y_pixel + top
                if target_y >= final_image.height:
                    continue

                final_image.paste(slice_img, (x * BLOCK_WIDTH, target_y), mask=slice_img)

    final_image = add_watermark(final_image)
    final_image.save(output_path)
    print(f"Готово! Сохранено в: {output_path}")

if __name__ == "__main__":
    input_file = "input_image.png"
    output_file = "output_map.png"
    if len(sys.argv) >= 2:
        input_file = sys.argv[1]
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    convert_image_to_map(input_file, output_file)
