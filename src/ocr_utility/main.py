from pathlib import Path
from ocr import extract_text_from_image

def main() -> None:
    BASE_DIR = Path(__file__).resolve().parents[2]
    
    input_path = Path(BASE_DIR / "data" / "input" / "panda expres rec.jpg")
    output_path = Path(BASE_DIR / "data" / "output" / "sample_output.txt")

    text = extract_text_from_image(input_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")

    print("\n--- OCR COMPLETE ---")
    print(f"Input: {input_path}")
    print(f"Output saved to: {output_path}")


if __name__ == "__main__":
    main()