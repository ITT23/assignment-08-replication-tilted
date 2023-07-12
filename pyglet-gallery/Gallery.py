import os
import random
import pyglet
import math


#AnimatedSprite class with help of chatGpt
class AnimatedSprite(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x_offset = 0
        self.total_x_offset = 0
        self.target_scale = self.scale
        self.scale_speed = 0.1

    def update(self, dt):
        self.x += self.x_offset * dt 
        self.total_x_offset += self.x_offset * dt
        if abs(self.total_x_offset) >= 700: # make dependent on img sizes
            self.x_offset = 0 
            self.total_x_offset = 0

        if 100 < self.x < 500: 
            self.target_scale = 0.55
            if self.target_scale > self.scale:
                scale_change = self.scale_speed * dt
                self.scale += scale_change
        else: 
            self.target_scale = 0.5
            if self.target_scale < self.scale:
                scale_change = self.scale_speed * dt * -1
                self.scale += scale_change

class Gallery:
    def __init__(self):
        self.sprite_corners = []
        self.images = []

        x_pos = -300
        y_pos = 200 
        spacing = 100

        img_folder = os.path.join(os.path.dirname(__file__), "img")
        img_files = os.listdir(img_folder)

        for filename in img_files:
            img_path = os.path.normpath(os.path.join(img_folder, filename))
            img_path = os.path.normpath(os.path.join(img_folder, filename))
            sprite = AnimatedSprite(img=pyglet.image.load(img_path), x=x_pos, y=y_pos)
            sprite.scale = 0.5
            self.images.append(sprite)
            x_pos += sprite.width + spacing

    def draw(self):
        for image in self.images:
            image.draw()

    def move_sprites(self, x_offset):
        for image in self.images:
            image.x_offset = -x_offset
    
    