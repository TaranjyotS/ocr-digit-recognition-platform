import numpy as np
from ocr_platform.preprocessing import make_square, resize_to_20x20


def test_make_square_returns_square_image():
    image = np.zeros((10, 20), dtype=np.uint8)
    square = make_square(image)
    assert square.shape[0] == square.shape[1]


def test_resize_to_20x20_returns_expected_shape():
    image = np.zeros((25, 12), dtype=np.uint8)
    resized = resize_to_20x20(image)
    assert resized.shape == (20, 20)
