from pathlib import Path
import cv2
import numpy as np


class DigitKNNModel:
    """OpenCV KNN model trained on the standard 0-9 handwritten digit grid."""

    def __init__(self, training_image_path: Path, k: int = 3) -> None:
        self.training_image_path = Path(training_image_path)
        self.k = k
        self.model = cv2.ml.KNearest_create()
        self._trained = False

    def train(self) -> float:
        image = cv2.imread(str(self.training_image_path))
        if image is None:
            raise FileNotFoundError(f"Training image not found: {self.training_image_path}")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cells = [np.hsplit(row, 100) for row in np.vsplit(gray, 50)]
        cell_array = np.array(cells)

        train = cell_array[:, :70].reshape(-1, 400).astype(np.float32)
        test = cell_array[:, 70:100].reshape(-1, 400).astype(np.float32)
        labels = np.arange(10)
        train_labels = np.repeat(labels, 350)[:, np.newaxis]
        test_labels = np.repeat(labels, 150)[:, np.newaxis]

        self.model.train(train, cv2.ml.ROW_SAMPLE, train_labels)
        _, results, _, _ = self.model.findNearest(test, k=self.k)
        accuracy = float(np.count_nonzero(results == test_labels) * 100.0 / results.size)
        self._trained = True
        return accuracy

    def predict(self, sample: np.ndarray, k: int = 1) -> tuple[str, float]:
        if not self._trained:
            self.train()
        sample = sample.reshape((1, 400)).astype(np.float32)
        _, result, _, distances = self.model.findNearest(sample, k=k)
        return str(int(result[0][0])), float(distances[0][0])
