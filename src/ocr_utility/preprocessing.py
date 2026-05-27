from pathlib import Path
import cv2

BASE_DIR = Path(__file__).resolve().parents[2]
DEBUG_DIR = BASE_DIR / "data/debug"

def preprocess_image(image_path: str | Path,
    save_debug: bool = False,
    debug_dir: str | Path = DEBUG_DIR
) -> any:
    image_path = Path(image_path)
    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError(f"Could not read image: {image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, h=30)
    thresholded = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        15,
    )

    if save_debug:
        print("Saving debug images...")
        debug_dir = Path(debug_dir)
        debug_dir.mkdir(parents=True, exist_ok=True)

        # print(f"Debug directory: {debug_dir.resolve().parents[2]}")
        # print(f"Debug directory: {debug_dir}")

        cv2.imwrite(str(debug_dir / f"{image_path.stem}_gray.png"), gray)
        cv2.imwrite(str(debug_dir / f"{image_path.stem}_denoised.png"), denoised)
        cv2.imwrite(str(debug_dir / f"{image_path.stem}_thresholded.png"), thresholded)

    return thresholded