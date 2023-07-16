import os

import numpy as np
from keras.models import load_model
from numpy.typing import NDArray
from sklearn.preprocessing import StandardScaler
from scipy.signal import resample
import joblib

from gesture_recognition.gestures import Gesture

class Recogniser:

  CURR_DIR = os.path.dirname(__file__)
  MODEL_PATH = "lstm_model"
  SAMPLE_POINTS = 50

  def __init__(self) -> None:
    print("* * * loading lstm model * * *")
    self._model = load_model(os.path.join(self.CURR_DIR, self.MODEL_PATH), compile=True)
    self._scaler = StandardScaler()
    self._encoder = joblib.load(os.path.join(self.CURR_DIR, 'encoder.joblib'))
    print("* * * finished loading lstm model * * *")

  def predict(self, data: NDArray) -> Gesture:
    points = self._scaler.fit_transform(data)
    points_resampled = resample(points, self.SAMPLE_POINTS)
    n_array = np.array([points_resampled])
    prediction = self._model.predict(n_array, verbose=0)
    y_predictions = np.argmax(prediction)

    prediction_label = self._encoder.inverse_transform(np.array([y_predictions]))[0]

    return Gesture[prediction_label.upper()]

if __name__ == "__main__":
  recogniser = Recogniser()
  recogniser.predict()