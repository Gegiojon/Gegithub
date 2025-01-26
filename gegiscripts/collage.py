import cv2
import numpy as np
import os
import re

# Function to calculate mean dimensions of images
def calculate_mean_dimensions(images):
    total_width = 0
    total_height = 0
    total_images = len(images)

    for img in images:
        height, width, _ = img.shape
        total_width += width
        total_height += height

    mean_width = int(total_width / total_images)
    mean_height = int(total_height / total_images)

    return mean_width, mean_height

# Function to resize images
def resize_images(images, mean_width, mean_height):
    resized_images = []

    for img in images:
        resized_img = cv2.resize(img, (mean_width, mean_height))
        resized_images.append(resized_img)

    return resized_images

# Function to calculate the dimensions of the collage grid
def calculate_dimensions(n):
    """
    Calculate the dimensions of a grid that is as close to square as possible
    and can contain 'n' elements.
    """
    min_diff = n
    best_a = 1
    best_b = n
    
    # Find the pair of numbers that minimize the difference
    for a in range(1, n + 1):
        b = n // a
        if a * b == n:
            diff = abs(a - b)
            if diff < min_diff:
                min_diff = diff
                best_a = a
                best_b = b
    
    return best_a, best_b

# Function to create a collage from images
def create_collage(images, collage_size):
    # Create a blank canvas for the collage
    collage_height = images[0].shape[0] * collage_size[0]
    collage_width = images[0].shape[1] * collage_size[1]
    collage = np.zeros((collage_height, collage_width, 3), dtype=np.uint8)

    # Fill the collage with images
    index = 0
    for row in range(collage_size[0]):
        for col in range(collage_size[1]):
            if index < len(images):
                collage[row * images[0].shape[0]:(row + 1) * images[0].shape[0],
                        col * images[0].shape[1]:(col + 1) * images[0].shape[1]] = images[index]
                index += 1
            else:
                # If all images are used, return the collage
                return collage

    return collage  # Return the collage after all cells are filled

# Directory containing your images
input_dir = r"C:\Users\Usuario\Desktop\PROJECTS\KIOSKOLO\ALMACEN"

# Load all images from the directory
original_images = []
wrapped_images = []
for filename in os.listdir(input_dir):
    filepath = os.path.join(input_dir, filename)
    print("Loading image:", filepath)  # Print the filename being loaded
    if filename.startswith("(WRAPPED)"):
        img = cv2.imread(filepath)
        if img is not None:
            print("Image loaded successfully:", filepath)  # Print if the image is loaded successfully
            wrapped_images.append((filename, img))  # Store both filename and image
        else:
            print("Failed to load image:", filepath)  # Print if the image loading failed
    else:
        img = cv2.imread(filepath)
        if img is not None:
            print("Image loaded successfully:", filepath)  # Print if the image is loaded successfully
            original_images.append((filename, img))  # Store both filename and image
        else:
            print("Failed to load image:", filepath)  # Print if the image loading failed

# Sort images by filename
original_images.sort(key=lambda x: int(re.search(r'\d+', x[0]).group()))
wrapped_images.sort(key=lambda x: int(re.search(r'\d+', x[0]).group()))

# Calculate mean dimensions
mean_width, mean_height = calculate_mean_dimensions([img for _, img in original_images + wrapped_images])

# Resize images
resized_original_images = resize_images([img for _, img in original_images], mean_width, mean_height)
resized_wrapped_images = resize_images([img for _, img in wrapped_images], mean_width, mean_height)

# Determine collage size
n_original_images = len(resized_original_images)
a, b = calculate_dimensions(n_original_images)
collage_size_original = (a, b)

n_wrapped_images = len(resized_wrapped_images)
a, b = calculate_dimensions(n_wrapped_images)
collage_size_wrapped = (a, b)

# Create collages
collage_original = create_collage(resized_original_images, collage_size_original)
collage_wrapped = create_collage(resized_wrapped_images, collage_size_wrapped)

# Save collages
output_dir = r"C:\Users\Usuario\Desktop\PROJECTS\KIOSKOLO\KIOSKO"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

cv2.imwrite(os.path.join(output_dir, "COLLAGE.jpg"), collage_original)
print("Collage of original images saved to:", os.path.join(output_dir, "COLLAGE.jpg"))

cv2.imwrite(os.path.join(output_dir, "(WRAPPED) COLLAGE.jpg"), collage_wrapped)
print("Collage of wrapped images saved to:", os.path.join(output_dir, "(WRAPPED) COLLAGE.jpg"))
