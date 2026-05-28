# OCR Utility

A Python-based OCR utility for extracting text from images and PDFs using Tesseract OCR.

This project is being built as a practical software engineering project for document ingestion, OCR text extraction, receipt parsing, and structured data storage.

## Current Status

Implemented features:

- Python virtual environment setup
- Tesseract OCR integration
- Image OCR using `pytesseract`
- PDF text extraction and OCR fallback using PyMuPDF
- Flask single-page upload interface
- Image preprocessing support with OpenCV
- Debug image output for preprocessing experiments
- Receipt field parsing
- SQLite database storage
- Git/GitHub workflow

## Tech Stack

- Python
- Flask
- Tesseract OCR
- pytesseract
- Pillow
- OpenCV
- PyMuPDF
- pandas
- SQLite
- Git/GitHub

## Project Structure

```text
ocr-utility/
├── README.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── src/
│   └── ocr_utility/
│       ├── app.py
│       ├── main.py
│       ├── ocr.py
│       ├── pdf.py
│       ├── preprocessing.py
│       ├── parser.py
│       ├── database.py
│       └── templates/
│           └── index.html
├── tests/
├── data/
│   ├── input/
│   ├── output/
│   ├── debug/
│   └── receipts.db
└── docs/