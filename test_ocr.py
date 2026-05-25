from pathlib import Path

import pytesseract
from PIL import Image


# Windows tesseract executable path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

image_path = Path("data/input/panda expres rec.jpg")

if not image_path.exists():
    raise FileNotFoundError(f"Image not found: {image_path}")

# Open image
image = Image.open(image_path)

# Extract text
text = pytesseract.image_to_string(image)

print("\n--- OCR OUTPUT ---\n")
print(text)
