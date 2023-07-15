import os
import random
import pyglet
import math

'''
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
'''

class Gallery:
    def __init__(self, window_w, window_h, folder):
        self.window_w = window_w
        self.window_h = window_h
        self.images = []
        self.image_paths = []
        self.folder_path = folder
        self.current_img_index = 0
        self.moving_left_active = False
        self.moving_right_active = False
        self.min_opacity = 64
        self.max_opacity = 255
        self.max_img_width = window_w // 3

        img_folder = os.path.join(os.path.dirname(__file__), "img")
        img_files = os.listdir(img_folder)

        for i, filename in enumerate(img_files):
            img_path = os.path.normpath(os.path.join(img_folder, filename))
            img = pyglet.image.load(img_path)
            img.anchor_x = img.width // 2
            img.anchor_y = img.height // 2
            sprite = pyglet.sprite.Sprite(img, x=window_w/2, y=window_h/2)
            scaling_factor = self.get_scale_factor(img.width, img.height)
            sprite.scale = scaling_factor
            sprite.opacity = self.min_opacity
            scaled_img_width = scaling_factor * img.width
            sprite.x = (i + 1) * (scaled_img_width + 25)
            self.images.append(sprite)
            self.image_paths.append(filename)
        self.images[self.current_img_index].opacity = self.max_opacity

    def draw(self):
        self.check_and_add_new_img()
        movement_active, moving_direction = self.update_movement()
        for i, image in enumerate(self.images):
            if movement_active:
                image.x += moving_direction * 5
            image.draw()

    def check_and_add_new_img(self):
        img_folder = os.path.join(os.path.dirname(__file__), "img")
        img_files = os.listdir(img_folder)
        if len(img_files) > len(self.images):
            print("new img found")

        new_filenames = []
        for filename in img_files:
            if filename not in self.image_paths:
                new_filenames.append(filename)

        for new_filename in new_filenames:
            img = pyglet.image.load(f'{self.folder_path}/{new_filename}')
            img.anchor_x = img.width // 2
            img.anchor_y = img.height // 2

            sprite = pyglet.sprite.Sprite(img, x=self.window_w // 2, y=self.window_h // 2)
            scaling_factor = self.get_scale_factor(img.width, img.height)
            sprite.scale = scaling_factor
            sprite.opacity = self.min_opacity
            scaled_img_width = scaling_factor * img.width
            for i, image in enumerate(self.images):
                # todo: fix placing
                if i < self.current_img_index:
                    image.x -= (scaled_img_width + 25)
                else:
                    image.x += (scaled_img_width + 25)
                image.opacity = self.min_opacity
            self.images.insert(self.current_img_index, sprite)
            self.image_paths.insert(self.current_img_index, new_filename)
            self.images[self.current_img_index].opacity = self.max_opacity

    def update_movement(self):
        movement_active = False
        moving_direction = 0
        # if left tilted move images to the left
        if self.moving_left_active:
            moving_direction = -1
            # update opacity for de-highlighting old target img
            if self.images[self.current_img_index-1].opacity >= self.min_opacity:
                self.images[self.current_img_index-1].opacity -= 2
        # if right tilted move images to the right
        elif self.moving_right_active:
            moving_direction = 1
            # update opacity for de-highlighting old target img
            if self.images[self.current_img_index+1].opacity >= self.min_opacity:
                self.images[self.current_img_index+1].opacity -= 2

        # if images are currently moving, check if target img is in center
        # if so: stop movement, if not: update opacity to highlight new target img
        if moving_direction != 0:
            if self.window_w / 2 - 5 < self.images[self.current_img_index].x < self.window_w / 2 + 5:
                movement_active = False
                self.moving_right_active = False
                self.moving_left_active = False
                self.images[self.current_img_index].opacity = self.max_opacity
            else:
                movement_active = True
                if self.images[self.current_img_index].opacity < self.max_opacity - 1:
                    self.images[self.current_img_index].opacity += 2
        return movement_active, moving_direction

    def on_tilt_left(self):
        if (not self.moving_right_active and not self.moving_left_active) and self.current_img_index < len(self.images) - 1:
            self.current_img_index += 1
            self.moving_left_active = True

    def on_tilt_right(self):
        if (not self.moving_left_active and not self.moving_right_active) and self.current_img_index > 0:
            self.current_img_index -= 1
            self.moving_right_active = True

    def get_scale_factor(self, sprite_width, sprite_height):
        x_scale = self.max_img_width / sprite_width
        # y_scale = self.window_h / sprite_height
        return x_scale


