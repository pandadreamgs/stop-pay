import os
from PIL import Image, ImageOps

# Налаштування
SOURCE_DIR = 'images'
DEST_DIR = 'assets/icons'
SIZE = (128, 128)

def process_icons():
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)
        print(f"Створено папку: {DEST_DIR}")

    for filename in os.listdir(SOURCE_DIR):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            try:
                img_path = os.path.join(SOURCE_DIR, filename)
                img = Image.open(img_path).convert("RGBA")

                # Робимо картинку квадратною без спотворень (додаємо прозорі боки)
                img.thumbnail(SIZE, Image.Resampling.LANCZOS)
                
                # Створюємо порожнє прозоре полотно 128x128
                new_img = Image.new("RGBA", SIZE, (0, 0, 0, 0))
                # Центруємо іконку на полотні
                upper_left = (
                    (SIZE[0] - img.size[0]) // 2,
                    (SIZE[1] - img.size[1]) // 2
                )
                new_img.paste(img, upper_left)

                # Зберігаємо як PNG
                base_name = os.path.splitext(filename)[0]
                save_path = os.path.join(DEST_DIR, f"{base_name}.png")
                new_img.save(save_path, "PNG", optimize=True)
                
                print(f"✅ Оброблено: {filename} -> {base_name}.png")
            except Exception as e:
                print(f"❌ Помилка при обробці {filename}: {e}")

if __name__ == "__main__":
    if os.path.exists(SOURCE_DIR):
        process_icons()
    else:
        print(f"Папка {SOURCE_DIR} не знайдена!")
