import os, time
from collections import deque

import numpy as np

from recogniser import Recogniser
from gestures import Gesture
from DIPPID import SensorUDP


class Input:

  def __init__(self, port: int, capabilities: list[str]) -> None:
    self._port = port
    self._sensor = SensorUDP(self._port)
    
    self._capabilities = capabilities
    self._state = {}
  
  def get_state(self) -> dict:
    for capability in self._capabilities:
      data = self._sensor.get_value(capability)

      if data is not None:
         self._state[capability] = data

    return self._state

  def terminate_sensor(self) -> None:
    self._sensor.disconnect()


class Application:
  NAME = "Gesture App"
  SCRIPT_DIR = os.path.dirname(__file__)
  FPS = 1 / 60
  CAPABILITIES = ["accelerometer"]
  DQ_MAX_LEN = 50
  PORT = 5700

  def __init__(self) -> None:
    self._recogniser = Recogniser()
    self._input = Input(self.PORT, self.CAPABILITIES)

    self._deque_list = deque([], maxlen=self.DQ_MAX_LEN)
    self._current_activity = Gesture.NEUTRAL

  def _transform_data(self, data: dict) -> tuple:
    x = data["accelerometer"]["x"]
    y = data["accelerometer"]["y"]
    z = data["accelerometer"]["z"]

    return [x,y,z]

  def run(self) -> None:
    while True:
      data = self._input.get_state()
      if not bool(data):
        continue

      self._deque_list.append(self._transform_data(data))
      
      if len(self._deque_list) == self.DQ_MAX_LEN:
        result = self._recogniser.predict(list(self._deque_list))
        print(result.name)

      time.sleep(self.FPS)       

if __name__ == "__main__":
  application = Application()
  application.run()