from pathlib import Path
from ocr import extract_text_from_image
from pdf import extract_text_from_pdf

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_DIR = BASE_DIR / "data/input"
OUTPUT_DIR = BASE_DIR / "data/output"

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".pdf"}

def is_supported_file(file_path: Path) -> bool:
    return file_path.suffix.lower() in SUPPORTED_EXTENSIONS


def extract_text_from_file(file_path: Path) -> str:
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    return extract_text_from_image(file_path)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    files = [
        file_path
        for file_path in INPUT_DIR.iterdir()
        if file_path.is_file() and is_supported_file(file_path)
    ]

    if not files:
        print("No supported files found.")
        print(f"Input folder: {INPUT_DIR}")
        print(f"Supported extensions: {sorted(SUPPORTED_EXTENSIONS)}")
        return

    for file_path in files:
        print(f"Processing: {file_path.name}")

        try:
            text = extract_text_from_file(file_path)

            output_path = OUTPUT_DIR / f"{file_path.stem}_output.txt"
            output_path.write_text(text, encoding="utf-8")

            print(f"Saved: {output_path.name}")

        except Exception as error:
            print(f"Failed to process {file_path.name}: {error}")

    print("\nOCR batch complete.")


if __name__ == "__main__":
    main()