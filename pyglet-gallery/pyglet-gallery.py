import os
import pyglet
from pyglet import clock
from Gallery import Gallery
import sys
import time
import requests
import base64
from threading import Thread
from DIPPID import SensorUDP
#sys.path.append("../gesture_recognition/")
from recogniser import Recogniser
from collections import deque
from gestures import Gesture
import numpy as np
import statistics

recognizer = Recogniser()
deque_list = deque([], maxlen=50)
port = 5700
sensor = SensorUDP(port)

recent_predictions = deque([], maxlen=15)
mode_counter = 0

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800

img_folder = os.path.join(os.path.dirname(__file__), "img")

phone_ip = '192.168.2.116'

if len(sys.argv) > 1:
    phone_ip = sys.argv[1]
#from pynput.keyboard import Key, Controller

window = pyglet.window.Window(1080, 720)


gallery = Gallery()
#keyboard = Controller()
received_img = None

def receive_data():
    global received_img
    try:
        r = requests.get(url = f'http://{phone_ip}:8080/')
        result = r.json()
        filename = result['filename']
        filedata = result['data']
        with open(os.path.normpath(os.path.join(img_folder, filename)), "wb") as fh:
            fh.write(base64.b64decode(filedata))
        received_image = pyglet.image.load(filename)
    except:
        pass

    

def transform_data(data: dict) -> tuple:
    x = data["x"]
    y = data["y"]
    z = data["z"]

    return [x,y,z]


@window.event
def on_draw():
    global mode_counter
    mode_counter += 1
    window.clear()
    data = sensor.get_value("accelerometer")
    if data:
        deque_list.append(transform_data(data))
      
    if len(deque_list) == 50:
        result = recognizer.predict(list(deque_list))
        recent_predictions.append(result)
        #apply_input(result)
    if mode_counter == 20:
        print(recent_predictions)
        if recent_predictions and len(recent_predictions) > 0:
            mode = statistics.mode(recent_predictions)
            apply_input(mode)
        mode_counter = 0

    gallery.draw()



def update(dt):
    for image in gallery.images:
        image.update(dt)


@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.T:
        print("throw gesture performed")
        thread = Thread(target=receive_data)
        thread.run()
    if symbol == pyglet.window.key.Q:
        sys.exit(0)


@window.event
def on_key_press(symbol, modifiers):
    shift = 500
    for image in gallery.images:
        if image.scale >= 0.55:
            shift = image.width
    print(shift)
    if symbol == pyglet.window.key.LEFT:
        if gallery.images[0].x < 0:
            gallery.move_sprites(-(shift + 100))
    elif symbol == pyglet.window.key.RIGHT:
        if gallery.images[-1].x > 500:
            gallery.move_sprites(shift + 100)  

# for predicted gestures

def apply_input(input_condition):
    print(input_condition)
    shift = 500
    for image in gallery.images:
        if image.scale >= 0.55:
            shift = image.width
    print(shift)

    if input_condition == Gesture.TILT_RIGHT: # tilt left
        print("tilt left")
        #if gallery.images[0].x < 0:
        gallery.move_sprites(-(shift + 100))
    elif input_condition == Gesture.TILT_LEFT: # tilt right
        print("tilt right")
        #f gallery.images[-1].x > 500:
        gallery.move_sprites(shift + 100)
    elif input_condition == Gesture.THROW: # throw
        print(receive_data())
        #append_picture()
        print("throw")
    elif input_condition == 3: # neutral
        print("neutral")


def append_picture():
    # append picture to current image position
    print("fwfwf")


pyglet.clock.schedule_interval(update, 1/60)

pyglet.app.run()
