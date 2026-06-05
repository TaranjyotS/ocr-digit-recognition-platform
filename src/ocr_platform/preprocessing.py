import cv2
import numpy as np


def contour_x(contour: np.ndarray) -> int:
    if cv2.contourArea(contour) <= 10:
        return 0
    moments = cv2.moments(contour)
    if moments["m00"] == 0:
        return 0
    return int(moments["m10"] / moments["m00"])


def make_square(image: np.ndarray) -> np.ndarray:
    height, width = image.shape[:2]
    if height == width:
        return image
    size = max(height, width)
    top = (size - height) // 2
    bottom = size - height - top
    left = (size - width) // 2
    right = size - width - left
    return cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])


def resize_to_20x20(image: np.ndarray) -> np.ndarray:
    square = make_square(image)
    resized = cv2.resize(square, (16, 16), interpolation=cv2.INTER_AREA)
    return cv2.copyMakeBorder(resized, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=[0, 0, 0])


def extract_digit_regions(image: np.ndarray, min_width: int = 5, min_height: int = 25) -> list[tuple[np.ndarray, tuple[int, int, int, int]]]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 30, 150)
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=contour_x)

    regions: list[tuple[np.ndarray, tuple[int, int, int, int]]] = []
    for contour in contours:
        x, y, width, height = cv2.boundingRect(contour)
        if width >= min_width and height >= min_height:
            roi = blurred[y : y + height, x : x + width]
            _, thresholded = cv2.threshold(roi, 127, 255, cv2.THRESH_BINARY_INV)
            regions.append((resize_to_20x20(thresholded), (x, y, width, height)))
    return regions
