from pathlib import Path

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from ocr import extract_text_from_image
from pdf import extract_text_from_pdf


BASE_DIR = Path(__file__).resolve().parents[2]

UPLOAD_DIR = BASE_DIR / "data/input"
OUTPUT_DIR = BASE_DIR / "data/output"

SUPPORTED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".tif",
    ".tiff",
    ".bmp",
    ".pdf",
}

app = Flask(__name__)


def is_supported_file(filename: str) -> bool:
    return Path(filename).suffix.lower() in SUPPORTED_EXTENSIONS


def extract_text_from_file(
    file_path: Path,
    preprocess: bool = True,
) -> str:
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    return extract_text_from_image(
        file_path,
        preprocess=preprocess,
    )


@app.route("/", methods=["GET", "POST"])
def index():
    extracted_text = None
    error = None
    uploaded_filename = None

    if request.method == "POST":
        file = request.files.get("receipt")

        preprocess_enabled = (
            request.form.get("preprocess") == "on"
        )

        if not file or file.filename == "":
            error = "No file selected."

        elif not is_supported_file(file.filename):
            error = "Unsupported file type."

        else:
            UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

            safe_filename = secure_filename(file.filename)

            input_path = UPLOAD_DIR / safe_filename

            file.save(input_path)

            try:
                extracted_text = extract_text_from_file(
                    input_path,
                    preprocess=preprocess_enabled,
                )

                output_path = (
                    OUTPUT_DIR
                    / f"{input_path.stem}_output.txt"
                )

                output_path.write_text(
                    extracted_text,
                    encoding="utf-8",
                )

                uploaded_filename = safe_filename

            except Exception as exc:
                error = f"Failed to process file: {exc}"

    return render_template(
        "index.html",
        extracted_text=extracted_text,
        error=error,
        uploaded_filename=uploaded_filename,
        supported_extensions=", ".join(
            sorted(SUPPORTED_EXTENSIONS)
        ),
    )


if __name__ == "__main__":
    app.run(debug=True)