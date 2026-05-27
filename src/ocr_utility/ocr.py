import pytesseract
from PIL import Image
from pathlib import Path
from preprocessing import preprocess_image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

def extract_text_from_image(image_path: str | Path, preprocess: bool = True) -> str:
    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    if preprocess:
        processed_image = preprocess_image(
            image_path,
            save_debug=True,
            # debug_dir=Path("data/debug"),
        )
        text = pytesseract.image_to_string(processed_image)
    else:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)

    return text