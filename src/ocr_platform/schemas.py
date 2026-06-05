from pydantic import BaseModel, Field


class Prediction(BaseModel):
    digit: str
    x: int
    y: int
    width: int
    height: int
    confidence_distance: float = Field(description="Lower KNN distance is usually better.")


class OCRResponse(BaseModel):
    digits: list[str]
    text: str
    predictions: list[Prediction]
