import os
from PIL import Image

def resize_images(input_folder, output_folder):
    # Crear el directorio de salida si no existe
    os.makedirs(output_folder, exist_ok=True)

    # Obtener todas las imágenes del directorio
    images = [f for f in os.listdir(input_folder) if f.lower().endswith(('jpg', 'jpeg', 'webp', 'png'))]

    if not images:
        print("No se encontraron imágenes en la carpeta especificada.")
        return

    # Encontrar la imagen con el menor tamaño
    min_width, min_height = float('inf'), float('inf')
    min_image_name = None
    for img_name in images:
        img_path = os.path.join(input_folder, img_name)
        with Image.open(img_path) as img:
            width, height = img.size
            if width < min_width and height < min_height:
                min_width, min_height = width, height
                min_image_name = img_name

    print(f"El tamaño mínimo encontrado es: {min_width}x{min_height}, en la imagen: {min_image_name}")

    # Redimensionar todas las imágenes al tamaño mínimo
    for img_name in images:
        img_path = os.path.join(input_folder, img_name)
        with Image.open(img_path) as img:
            resized_img = img.resize((min_width, min_height), Image.Resampling.LANCZOS)
            output_path = os.path.join(output_folder, os.path.splitext(img_name)[0] + ".jpg")
            resized_img.convert("RGB").save(output_path, "JPEG")

    print(f"Todas las imágenes han sido redimensionadas y guardadas en '{output_folder}'.")


