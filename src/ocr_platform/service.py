from pathlib import Path
import cv2
import numpy as np
from .config import get_settings
from .model import DigitKNNModel
from .preprocessing import extract_digit_regions
from .schemas import OCRResponse, Prediction


_model: DigitKNNModel | None = None
_model_accuracy: float | None = None


def get_model() -> DigitKNNModel:
    global _model, _model_accuracy
    settings = get_settings()
    if _model is None:
        _model = DigitKNNModel(settings.training_image_path, k=settings.model_k)
        _model_accuracy = _model.train()
    return _model


def get_model_accuracy() -> float | None:
    return _model_accuracy


def recognize_image(image: np.ndarray) -> OCRResponse:
    settings = get_settings()
    model = get_model()
    regions = extract_digit_regions(image, settings.min_contour_width, settings.min_contour_height)

    predictions: list[Prediction] = []
    for region, (x, y, width, height) in regions:
        digit, distance = model.predict(region)
        predictions.append(Prediction(digit=digit, x=x, y=y, width=width, height=height, confidence_distance=distance))

    digits = [prediction.digit for prediction in predictions]
    return OCRResponse(digits=digits, text="".join(digits), predictions=predictions)


def recognize_file(path: Path) -> OCRResponse:
    image = cv2.imread(str(path))
    if image is None:
        raise ValueError(f"Could not read image: {path}")
    return recognize_image(image)


def decode_image_bytes(content: bytes) -> np.ndarray:
    array = np.frombuffer(content, np.uint8)
    image = cv2.imdecode(array, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Uploaded file is not a valid image.")
    return image
