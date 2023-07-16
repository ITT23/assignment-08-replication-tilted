import pyglet
import sys
import time
import requests
import base64
from threading import Thread


WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800

phone_ip = '192.168.0.72'
if len(sys.argv) > 1:
    phone_ip = sys.argv[1]

window = pyglet.window.Window(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
image = pyglet.image.load('nothing.png')
sprite = pyglet.sprite.Sprite(image, x=50, y=50)


def receive_data():
    r = requests.get(url = f'http://{phone_ip}:8080/')
    result = r.json()
    filename = result['filename']
    filedata = result['data']
    with open(filename, "wb") as fh:
        fh.write(base64.b64decode(filedata))
    image = pyglet.image.load(filename)
    sprite.image = image
    sprite.scale = WINDOW_WIDTH / image.width 
    

@window.event
def on_draw():
    window.clear()
    sprite.draw()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.T:
        print("throw gesture performed")
        thread = Thread(target=receive_data)
        thread.run()
    if symbol == pyglet.window.key.Q:
        sys.exit(0)


if __name__ == '__main__':
    pyglet.app.run()
    
