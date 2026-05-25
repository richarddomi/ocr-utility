# OCR Utility

A Python-based OCR utility for extracting text from images using Tesseract OCR.

This project is being built as a practical software engineering project to process images, extract text, and eventually export structured data for analysis.

## Current Status

Working proof of concept:

- Python virtual environment created
- Tesseract OCR installed and connected
- `pytesseract` successfully extracts text from an image
- Basic project structure created
- Git/GitHub workflow initialized

## Tech Stack

- Python
- Tesseract OCR
- pytesseract
- Pillow
- OpenCV
- pandas
- Git/GitHub

## Project Structure

```text
ocr-utility/
├── README.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── test_ocr.py
├── src/
│   └── ocr_utility/
├── tests/
├── data/
│   ├── input/
│   ├── output/
│   └── samples/
└── docs/