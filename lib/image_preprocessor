import os
import cv2
import numpy as np

def apply_clahe_rgb(image, clip_limit=2.0, tile_grid=(8, 8)):
    """
    Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) 
    to the L-channel of the LAB color space of an RGB image.

    Args:
        image (numpy.ndarray): Input image in BGR format.
        clip_limit (float): Threshold for contrast limiting.
        tile_grid (tuple): Size of grid for histogram equalization.

    Returns:
        numpy.ndarray: Image with enhanced contrast in BGR format.
    """
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid)
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l_eq = clahe.apply(l)
    lab_eq = cv2.merge((l_eq, a, b))
    return cv2.cvtColor(lab_eq, cv2.COLOR_LAB2BGR)

def split_into_patches(image, patch_size=256):
    """
    Split an image into non-overlapping square patches.

    Args:
        image (numpy.ndarray): Input image.
        patch_size (int): Width and height of each patch.

    Returns:
        list: List of image patches (numpy.ndarray).
    """
    patches = []
    h, w, _ = image.shape
    for y in range(0, h, patch_size):
        for x in range(0, w, patch_size):
            patch = image[y:y + patch_size, x:x + patch_size]
            if patch.shape[:2] == (patch_size, patch_size):  # Skip incomplete patches
                patches.append(patch)
    return patches

def preprocess_and_patch(input_dir, output_dir, categories=("fire", "no_fire"), patch_size=256):
    """
    Preprocess images in folders by applying CLAHE and splitting into patches.

    Args:
        input_dir (str): Path to the root directory containing category subfolders.
        output_dir (str): Directory to save processed patches.
        categories (tuple): Folder names representing class labels.
        patch_size (int): Size of each image patch.

    Returns:
        None
    """
    for category in categories:
        src = os.path.join(input_dir, category)
        dst = os.path.join(output_dir, category)
        os.makedirs(dst, exist_ok=True)

        for filename in os.listdir(src):
            if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
                continue

            img_path = os.path.join(src, filename)
            image = cv2.imread(img_path)
            if image is None:
                print(f"Skipping unreadable image: {img_path}")
                continue

            image_eq = apply_clahe_rgb(image)
            patches = split_into_patches(image_eq, patch_size)

            for i, patch in enumerate(patches, 1):
                out_name = f"{os.path.splitext(filename)[0]}_patch_{i}.png"
                cv2.imwrite(os.path.join(dst, out_name), patch)

    print("Done")
