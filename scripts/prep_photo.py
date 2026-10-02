import sys
from PIL import Image
import numpy as np
import cv2
from rembg import remove

def prep_photo(input_path, output_path="source-prepped.png"):
    print("Removing background...")
    input_image = Image.open(input_path)
    output_image = remove(input_image)
    
    # Convert PIL to OpenCV format (BGR)
    img_np = np.array(output_image)
    
    # If image has alpha channel, composite on white background
    if img_np.shape[2] == 4:
        alpha = img_np[:, :, 3] / 255.0
        rgb = img_np[:, :, :3]
        white_bg = np.ones_like(rgb, dtype=np.uint8) * 255
        img_np = (rgb * alpha[:, :, np.newaxis] + white_bg * (1 - alpha[:, :, np.newaxis])).astype(np.uint8)

    # Convert to grayscale for CLAHE
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    
    print("Applying CLAHE contrast boost...")
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    # Save prepped image
    cv2.imwrite(output_path, enhanced)
    print(f"Saved prepped photo to {output_path}")

if __name__ == "__main__":
    img_file = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
    prep_photo(img_file)