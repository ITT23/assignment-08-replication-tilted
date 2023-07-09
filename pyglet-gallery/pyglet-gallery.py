import pyglet
from pyglet import clock
from Gallery import Gallery
#from pynput.keyboard import Key, Controller

window = pyglet.window.Window(1080, 720)


gallery = Gallery()
#keyboard = Controller()

@window.event
def on_draw():
    window.clear()
    gallery.draw()


def update(dt):
    for image in gallery.images:
        image.update(dt)


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
'''
def apply_input():

    input_result = recog.recognize(points)
    input_condition = input_result.Name
    if input_condition == 0: # tilt left
        keyboard.press(Key.left)
        keyboard.release(Key.left)
        print("tilt left")
    elif input_condition == 1: # tilt right
        keyboard.press(Key.right)
        keyboard.release(Key.right)
        print("tilt right")
    elif input_condition == 2: # throw
        append_picture()
        print("throw")
    elif input_condition == 3: # neutral
        print("neutral")


def append_picture():
    # append picture to current image position
'''
pyglet.clock.schedule_interval(update, 1/60)

pyglet.app.run()
