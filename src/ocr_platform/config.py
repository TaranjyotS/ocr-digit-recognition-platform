from functools import lru_cache
from pathlib import Path
from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "OCR Digit Recognition Platform"
    model_k: int = 3
    min_contour_width: int = 5
    min_contour_height: int = 25
    training_image_path: Path = Path("data/training/digits.jpg")


@lru_cache
def get_settings() -> Settings:
    return Settings()
