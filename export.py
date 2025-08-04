from PIL import Image

bg = Image.open("background.png").convert("RGBA")
fg = Image.open("output_map.png").convert("RGBA")

bg.paste(fg, (0, 0), fg)
bg.save("final_image.png")
