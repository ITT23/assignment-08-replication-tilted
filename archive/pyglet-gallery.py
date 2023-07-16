import os
import pyglet
from Gallery import Gallery
import sys
import requests
import base64
from threading import Thread
from DIPPID import SensorUDP
from recogniser import Recogniser
from collections import deque
from gestures import Gesture


WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 800
DEQUE_LENGTH = 100
PORT = 5700
SENSOR = SensorUDP(PORT)


img_folder = os.path.join(os.path.dirname(__file__), "img")
phone_ip = '192.168.2.116'

if len(sys.argv) > 1:
    phone_ip = sys.argv[1]
if len(sys.argv) > 2:
    img_folder = sys.argv[2]


recognizer = Recogniser()
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
gallery = Gallery(WINDOW_WIDTH, WINDOW_HEIGHT, img_folder)
deque_list = deque([], maxlen=DEQUE_LENGTH)


def handle_sensor_data():
    data = SENSOR.get_value("accelerometer")
    if data:
        deque_list.append(transform_data(data))
    if len(deque_list) == DEQUE_LENGTH:
        result = recognizer.predict(list(deque_list))
        deque_list.clear()
        apply_input(result)


def transform_data(data: dict) -> tuple:
    x = data["x"]
    y = data["y"]
    z = data["z"]
    return [x, y, z]


def apply_input(input_condition):
    print(input_condition)
    if input_condition == Gesture.TILT_RIGHT:
        gallery.on_tilt_right()
    elif input_condition == Gesture.TILT_LEFT:
        gallery.on_tilt_left()
    elif input_condition == Gesture.THROW:
        thread = Thread(target=receive_data, daemon=True)
        thread.start()
        thread.join()


def receive_data():
    try:
        r = requests.get(url=f'http://{phone_ip}:8080/')
        result = r.json()
        filename = result['filename']
        filedata = result['data']
        with open(os.path.normpath(os.path.join(img_folder, filename)), "wb") as fh:
            fh.write(base64.b64decode(filedata))
    except:
        pass


@window.event
def on_draw():
    window.clear()
    handle_sensor_data()
    gallery.draw()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.LEFT:
        gallery.on_tilt_left()
    elif symbol == pyglet.window.key.RIGHT:
        gallery.on_tilt_right()
    elif symbol == pyglet.window.key.T:
        thread = Thread(target=receive_data, daemon=True)
        thread.start()
        thread.join()
    elif symbol == pyglet.window.key.Q:
        sys.exit(0)


pyglet.app.run()

