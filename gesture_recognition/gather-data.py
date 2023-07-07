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

  def __init__(self, port: int, capabilities: list[str], button_key: str) -> None:
    self._port = port
    self._sensor = SensorUDP(self._port)
    
    self._capabilities = capabilities
    self._state: dict[str, CapabilityValues] = {}

    #handle button_1 events separately so that we do not have to split it from the rest of the sensor data later
    self._button_key = button_key
    self._button_pressed = False
  
  def get_button_state(self) -> bool:
    '''
      returns boolean value that indicates if button_1 from M5Stack was pressed. M5Stack should only return `True` once in the application cylce as the start is depending on the button press and the stop is depending on a time function (duration).
    '''
    pressed = self._sensor.get_value(self._button_key)

    if pressed and pressed == 1 and not self._button_pressed:
      self._button_pressed = True

      return True

    return False
  
  def get_state(self) -> dict[str, CapabilityValues]:
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
  BUTTON_KEY = "button_1"
  CSV_HEADER = "id,time_stamp,gesture,accelerometer_x,accelerometer_y,accelerometer_z\n"
  CAPABILITIES = ["accelerometer"]

  def __init__(self, gesture: Gesture, duration: int, pps: int, wait: int, file_location: str) -> None:
    self._input = Input(self.PORT, self.CAPABILITIES, self.BUTTON_KEY)

    self._gesture = gesture
    self._duration =  duration
    self._pps = 1 / pps #polls per second; callback mode averages around 77 per second; setting default to 50 to avoid too many double measurements;
    self._wait = wait
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
    start_time = None
    print("waiting for button_1 press to start recording...\n")

    while self._running:
      if self._input.get_button_state():
        print(f"* * * recording starts in {self._wait} seconds. * * *\n")
        time.sleep(self._wait)
        self._recording = True
        start_time = time.time()
        print(f"* * * recording has started at unix time {time.ctime(start_time)}. * * *\n")

      if self._recording:
        data = self._input.get_state()
        self._process_sensor_data(data)

        if start_time + self._duration < time.time():
          self._recording = False
          print(f"* * * recording has stopped at unix time {time.ctime(time.time())}. * * *\n")
          self._input.terminate_sensor()
          self._write_csv_data()
          sys.exit()

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

  parser.add_argument("-d", "--duration", default=10, type=check_positive_int, help="[default: 10, unit: seconds] provide a duration in seconds that you want to measure your activity. the application automatically stops the recording and creates a csv file.")
  parser.add_argument("-pps", "--pollspersecond", default=50, type=check_positive_int, help="[default: 50, unit: per second] determine the frequency that the DIPPID device is polled for sensor data.")
  parser.add_argument("-w", "--wait", default=5, type=check_positive_int, help="[default: 5, unit: seconds] when pressing button_1 to start recording, the application waits X second so that the user can put the device inside his pocket and get ready for the activity.")
  parser.add_argument("-f", "--file_location", default="data", type=str, help="[default: ./data] folder location where to save files.")

  args = parser.parse_args()

  application = Application(Gesture[args.gesture.upper()], args.duration, args.pollspersecond, args.wait, args.file_location)
  application.run()