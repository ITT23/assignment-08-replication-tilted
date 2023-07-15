import os
import pyglet
from Gallery import Gallery
import sys
import requests
import base64
import time
from threading import Thread
from DIPPID import SensorUDP
#sys.path.append("../gesture_recognition/")
from recogniser import Recogniser
from collections import deque
from gestures import Gesture
import statistics


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500

img_folder = os.path.join(os.path.dirname(__file__), "img")
phone_ip = '192.168.2.116'

if len(sys.argv) > 1:
    phone_ip = sys.argv[1]
if len(sys.argv) > 2:
    img_folder = sys.argv[2]

recognizer = Recogniser()
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
gallery = Gallery(WINDOW_WIDTH, WINDOW_HEIGHT, img_folder)
thread_running = False


deque_list = deque([], maxlen=50)
port = 5700
sensor = SensorUDP(port)
recent_predictions = deque([], maxlen=15)
mode_counter = 0




def handle_sensor_data():
    global mode_counter
    data = sensor.get_value("accelerometer")
    if data:
        deque_list.append(transform_data(data))
    if len(deque_list) == 50:
        result = recognizer.predict(list(deque_list))
        recent_predictions.append(result)
        apply_input(result)
    if mode_counter == 20:
        print(recent_predictions)
        if recent_predictions and len(recent_predictions) > 0:
            mode = statistics.mode(recent_predictions)
            apply_input(mode)
        mode_counter = 0


def transform_data(data: dict) -> tuple:
    x = data["x"]
    y = data["y"]
    z = data["z"]
    return [x,y,z]


def apply_input(input_condition):
    print(input_condition)
    if input_condition == Gesture.TILT_RIGHT: # tilt left
        gallery.on_tilt_right()
    elif input_condition == Gesture.TILT_LEFT: # tilt right
        gallery.on_tilt_left()
    elif input_condition == Gesture.THROW: # throw
        thread = Thread(target=receive_data)
        thread.daemon = True
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
    global mode_counter
    mode_counter += 1
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
        print("throw gesture performed")
        thread = Thread(target=receive_data)
        thread.run()
    elif symbol == pyglet.window.key.Q:
        sys.exit(0)


pyglet.app.run()

