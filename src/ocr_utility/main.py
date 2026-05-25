from pathlib import Path

from ocr import extract_text_from_image


BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_DIR = BASE_DIR / "data/input"
OUTPUT_DIR = BASE_DIR / "data/output"

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}


def is_supported_image(file_path: Path) -> bool:
    return file_path.suffix.lower() in SUPPORTED_EXTENSIONS


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    image_files = [
        file_path
        for file_path in INPUT_DIR.iterdir()
        if file_path.is_file() and is_supported_image(file_path)
    ]

    if not image_files:
        print("No supported image files found.")
        print(f"Input folder: {INPUT_DIR}")
        print(f"Supported extensions: {sorted(SUPPORTED_EXTENSIONS)}")
        return

    for image_path in image_files:
        print(f"Processing: {image_path.name}")

        try:
            text = extract_text_from_image(image_path)

            output_path = OUTPUT_DIR / f"{image_path.stem}_output.txt"
            output_path.write_text(text, encoding="utf-8")

            print(f"Saved: {output_path.name}")

        except Exception as error:
            print(f"Failed to process {image_path.name}: {error}")

    print("\nOCR batch complete.")


if __name__ == "__main__":
    main()