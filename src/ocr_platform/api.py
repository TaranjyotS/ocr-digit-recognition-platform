from fastapi import FastAPI, File, HTTPException, UploadFile
from .schemas import OCRResponse
from .service import decode_image_bytes, get_model, get_model_accuracy, recognize_image

app = FastAPI(
    title="OCR Digit Recognition Platform",
    description="OpenCV/KNN handwritten digit recognition API upgraded from an academic OCR project.",
    version="1.0.0",
)


@app.on_event("startup")
def startup() -> None:
    get_model()


@app.get("/health")
def health() -> dict[str, str | float | None]:
    return {"status": "ok", "model_accuracy": get_model_accuracy()}


@app.post("/predict", response_model=OCRResponse)
async def predict(file: UploadFile = File(...)) -> OCRResponse:
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload an image file.")
    try:
        image = decode_image_bytes(await file.read())
        return recognize_image(image)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
