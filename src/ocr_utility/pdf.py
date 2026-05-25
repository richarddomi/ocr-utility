from pathlib import Path

import fitz  # PyMuPDF

from ocr import extract_text_from_image


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    document = fitz.open(pdf_path)
    extracted_pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text().strip()

        if text:
            extracted_pages.append(f"\n--- Page {page_number} Text Layer ---\n{text}")
        else:
            pixmap = page.get_pixmap(dpi=300)
            temp_image_path = pdf_path.parent / f"{pdf_path.stem}_page_{page_number}.png"
            pixmap.save(temp_image_path)

            ocr_text = extract_text_from_image(temp_image_path)
            extracted_pages.append(f"\n--- Page {page_number} OCR ---\n{ocr_text}")

            temp_image_path.unlink(missing_ok=True)

    document.close()

    return "\n".join(extracted_pages)