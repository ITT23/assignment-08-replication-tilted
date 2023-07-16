import os, sys, base64
from argparse import ArgumentParser
from collections import deque
from threading import Thread

import requests
from pyglet import app, window

from pyglet_gallery.Gallery import Gallery
from gesture_recognition.DIPPID import SensorUDP
from gesture_recognition.recogniser import Recogniser
from gesture_recognition.gestures import Gesture


class Application:

  NAME = "Pyglet Gallery"
  WINDOW_WIDTH = 1500
  WINDOW_HEIGHT = 800
  DEQUE_LENGTH = 100
  SENSOR_KEY = "accelerometer"

  def __init__(self, dippid_port: int, phone_ip: str, phone_port: int, img_folder: str) -> None:
    self._dippid_port = dippid_port
    self._phone_ip = phone_ip
    self._phone_port = phone_port
    self._img_folder = img_folder

    self.window = window.Window(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, caption=self.NAME)
    self.on_draw = self.window.event(self.on_draw)
    self.on_key_release = self.window.event(self.on_key_release)
    
    self.sensor = SensorUDP(self._dippid_port)
    self.recognizer = Recogniser()
    self.gallery = Gallery(self.window.width, self.window.height, img_folder)
    
    self.deque_list = deque([], maxlen=self.DEQUE_LENGTH)

  def handle_sensor_data(self) -> None:
    data = self.sensor.get_value(self.SENSOR_KEY)
    
    if data:
      self.deque_list.append(self.transform_data(data))
    
    if len(self.deque_list) == self.DEQUE_LENGTH:
      result = self.recognizer.predict(list(self.deque_list))
      self.deque_list.clear()
      self.apply_input(result)

  def transform_data(self, data: dict) -> tuple:
    x = data["x"]
    y = data["y"]
    z = data["z"]
    
    return [x, y, z]

  def apply_input(self, input_condition: Gesture) -> None:
    if input_condition == Gesture.TILT_RIGHT:
      self.gallery.tilt_right()
    
    elif input_condition == Gesture.TILT_LEFT:
      self.gallery.tilt_left()
    
    elif input_condition == Gesture.THROW:
      thread = Thread(target=self.receive_data, daemon=True)
      thread.start()
      thread.join()

  def receive_data(self, *_) -> None:
    try:
      r = requests.get(url=f'http://{self._phone_ip}:{self._phone_port}/')
      result = r.json()
      filename = result['filename']
      filedata = result['data']
      with open(os.path.normpath(os.path.join(self.img_folder, filename)), "wb") as fh:
        fh.write(base64.b64decode(filedata))
    
    except:
      pass

  def on_draw(self) -> None:
    self.window.clear()
    self.handle_sensor_data()
    self.gallery.draw()

  def on_key_release(self, symbol: int, *_) -> None:
    if symbol == window.key.LEFT:
      self.gallery.tilt_left()
    
    elif symbol == window.key.RIGHT:
      self.gallery.tilt_right()
    
    elif symbol == window.key.T:
      thread = Thread(target=self.receive_data, daemon=True)
      thread.start()
      thread.join()
    
    elif symbol == window.key.Q:
      sys.exit(0)

  def run(self) -> None:
    app.run()

if __name__ == "__main__":
  parser = ArgumentParser(prog=f"{Application.NAME}", description="pyglet gallery that lets you swipe through with your smartphone using gestures.")
  parser.add_argument("-p", default=5700, type=int, help="dippid port")
  parser.add_argument("-pi", default="192.168.2.116", type=str, help="phone ip")
  parser.add_argument("-pp", default=8080, type=int, help="phone port")
  parser.add_argument("-f", default="/Users/micha/Projects/ITT/08_assignment/pyglet_gallery/img", type=str, help="add absolute path to a folder with preexisiting images")

  args = parser.parse_args()

  application = Application(dippid_port=args.p, phone_ip=args.pi, phone_port=args.pp, img_folder=args.f)

  application.run()