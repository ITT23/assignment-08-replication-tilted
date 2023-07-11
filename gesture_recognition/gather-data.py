# this program gathers sensor data
import os, sys, time
from typing import TypedDict
from argparse import ArgumentParser, ArgumentTypeError

from DIPPID import SensorUDP
from gestures import Gesture


class CapabilityValues(TypedDict):
  x: int
  y: int
  z: int
  

class Input:

  def __init__(self, port: int, capabilities: list[str], toggle_button: str, terminate_button: str) -> None:
    self._port = port
    self._sensor = SensorUDP(self._port)
    
    self._capabilities = capabilities
    self._state: dict[str, CapabilityValues] = {}

    #handle button_1 events separately so that we do not have to split it from the rest of the sensor data later
    self._toggle_button = toggle_button
    self._terminate_button = terminate_button
    self.__toggle_button_pressed = False
  
  def get_button_1(self) -> bool:
    '''
      returns boolean value that indicates if button_1 from M5Stack was pressed. if M5Stack returns a value that can not be type cast to boolean, it returns `False`. As M5Stack returns `True` as long as a button is held, therefore button_1_pressed was introduced. all `True` values except the first and until the button is released are turned to `False`. Therefore get_button_1 only returns `True` once for the switch from not pressed to pressed. button_1 is used to quit the game and only one `True` value is required for that.
    '''
    pressed = bool(self._sensor.get_value(self._toggle_button))

    if pressed and not self.__toggle_button_pressed:
      self.__toggle_button_pressed = True

      return True
    
    elif not pressed and self.__toggle_button_pressed:
      self.__toggle_button_pressed = False

    return False

  def get_button_2(self) -> bool:
    pressed = bool(self._sensor.get_value(self._terminate_button))

    return pressed
  
  def get_acceleration(self) -> dict[str, CapabilityValues]:
    for capability in self._capabilities:
      data = self._sensor.get_value(capability)

      if data is not None:
        self._state[capability]: dict[str, CapabilityValues] = data

    return self._state

  def terminate_sensor(self) -> None:
    self._sensor.disconnect()


class Application:

  PORT = 5700
  CURR_DIR = os.path.dirname(__file__)
  TOGGLE_BUTTON = "button_1"
  TERMINATE_BUTTON = "button_2"
  CSV_HEADER = "id,time_stamp,gesture,accelerometer_x,accelerometer_y,accelerometer_z\n"
  CAPABILITIES = ["accelerometer"]

  def __init__(self, gesture: Gesture, pps: int, file_location: str) -> None:
    self._input = Input(self.PORT, self.CAPABILITIES, self.TOGGLE_BUTTON, self.TERMINATE_BUTTON)

    self._gesture = gesture
    self._pps = 1 / pps #polls per second; callback mode averages around 77 per second; setting default to 50 to avoid too many double measurements;
    self._file_location = file_location

    self._running = True
    self._recording = False
    
    self._id = 0
    self._data: list[str] = []

    self._output_folder = self._check_output_folder()

  def _check_output_folder(self) -> str:
    strip_f_location = self._file_location.lstrip(".").lstrip("/").lstrip("\\") #remove trailing dot and/or slash because os.path.join automatically adds the correct separator between elements according to the underlying system
    path = os.path.join(self.CURR_DIR, strip_f_location)
    if not os.path.exists(path):
      raise Exception(f"output folder path is invalid -- {path}")
    
    return path

  def run(self) -> None:
    while self._running:
      if self._input.get_button_2():
        print("terminating app...")
        self._input.terminate_sensor()
        sys.exit()

      button_1_pressed = self._input.get_button_1()

      if not self._recording and button_1_pressed:
        print("* * * started recording data * * *")
        self._recording = True

      elif self._recording and button_1_pressed:
        self._write_csv_data()
        self._data = []
        self._id = 0
        print("* * * stopped recording data * * *")
        self._recording = False


      if self._recording:
        data = self._input.get_acceleration()
        self._process_sensor_data(data)

      '''
        m5stack polling needs to be limited as sensor values do not change as often as python can call get_state. this would lead to a lot of dublicate data.
      '''
      time.sleep(self._pps)

  def _process_sensor_data(self, data: dict[str, CapabilityValues]) -> None:
    meta_data = f"{self._id},{round(time.time() * 1000)},{self._gesture.name}"
    
    measurement_data = ""
    for sensor_name in data:
      for axis_name in data[sensor_name]:
        measurement_data += f",{data[sensor_name][axis_name]}"

    self._data.append(meta_data + measurement_data)
    self._id += 1

  def _write_csv_data(self) -> None:
    content = self.CSV_HEADER
    content += "\n".join(self._data)

    file_name = os.path.join(self._output_folder, f"{self._gesture.name}_{round(time.time() * 1000)}.csv")
    data_file = open(file_name, "w")
    data_file.write(content)
    data_file.close()
    print(f"file saved to {file_name}.")


def check_positive_int(value) -> bool:
  try:
    int_val = int(value)
    if int_val < 0:
      raise ArgumentTypeError(f"{value} is not a positive integer.")
    return int_val
  except Exception:
    raise ArgumentTypeError(f"{value} is not a positive integer.")


if __name__ == "__main__":
  parser = ArgumentParser(prog="Data Gatherer", description="this application gatheres gesture data from a M5Stack or an Android smartphone. data contains these values: id, gesture, acceleration(x,y,z) and timestamp. data will be saved to a csv file.")
  parser.add_argument("gesture", type=str, choices=list(Gesture.__members__), help=f"provide a gesture that you want to measure. gestures are: {list(Gesture.__members__)}.")

  parser.add_argument("-pps", "--pollspersecond", default=50, type=check_positive_int, help="[default: 50, unit: per second] determine the frequency that the DIPPID device is polled for sensor data.")
  parser.add_argument("-f", "--file_location", default="data", type=str, help="[default: ./data] folder location where to save files.")

  args = parser.parse_args()

  application = Application(Gesture[args.gesture.upper()], args.pollspersecond, args.file_location)
  application.run()