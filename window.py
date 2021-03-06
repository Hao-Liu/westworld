#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import xmlrpc.client
import math

import pyglet

import utils

class Window(pyglet.window.Window):
    def __init__(self, width=800, height=600):
        super(Window, self).__init__(width=width, height=height)

        pyglet.resource.path = ['.']
        pyglet.resource.reindex()
        self.circle_img = pyglet.resource.image("circle.png")
        self.circle_img.anchor_x = self.circle_img.width / 2
        self.circle_img.anchor_y = self.circle_img.height / 2
        self.proxy = xmlrpc.client.ServerProxy('http://localhost:8000')

    def render_no_connection(self):
        self.clear()
        label = pyglet.text.Label(
                'Cannot connect to server',
                font_name='Times New Roman',
                font_size=36,
                x=self.width//2,
                y=self.height//2,
                anchor_x='center',
                anchor_y='center',
                )
        label.draw()
        self.flip()

    def render(self):
        self.clear()
        tiles = self.proxy.get_tiles()
        pyglet.gl.glLineWidth(2.0)
        for tile in tiles:
            keys = ['x', 'y', 'width', 'height', 'nutrition', "n_agents"]
            x, y, width, height, nutrition, n_agents= (
                    tile.get(key) for key in keys)
            pyglet.gl.glColor4f(1.0, 1.0, 1.0, 1.0)
            pyglet.graphics.draw(
                    4,
                    pyglet.gl.GL_LINE_LOOP,
                    ("v2f", (
                        x, y,
                        x, y + height,
                        x + width, y + height,
                        x + width, y)))
            pyglet.gl.glColor4f(0.0, 0.0, n_agents / 3.0, 1.0)
            pyglet.graphics.draw(
                    4,
                    pyglet.gl.GL_QUADS,
                    ("v2f", (
                        x, y,
                        x, y + height,
                        x + width, y + height,
                        x + width, y)))

        agents = self.proxy.get_agents()
        for agent in agents:
            x = agent['x']
            y = agent['y']
            direction = agent['direction']
            sight = agent['sight']
            vision = agent['vision']
            n_cell = agent['n_cell']
            aov = agent['aov']
            for idx, sight_dir in enumerate(utils.linspace(- aov / 2, aov / 2, n_cell)):
                sight_dir = direction + sight_dir
                ratio = vision[idx]
                if ratio != 1.0:
                    color = (1, 0, 0, 1)
                else:
                    color = (0, 1, 0, 1)
                pyglet.gl.glColor4f(*color)
                pyglet.graphics.draw(
                        2,
                        pyglet.gl.GL_LINES,
                        ("v2f", (
                            x,
                            y,
                            x + sight * ratio * math.cos(sight_dir),
                            y + sight * ratio * math.sin(sight_dir))))

        for agent in agents:
            x = agent['x']
            y = agent['y']
            reward = agent['reward']
            size = agent['size']
            circle = pyglet.sprite.Sprite(
                    img=self.circle_img,
                    x=x, y=y,
            )
            if reward:
                circle.color = (255, 0, 0)
            else:
                circle.color = (255, 255, 255)
            circle.scale = size / self.circle_img.width * 1.3
            circle.draw()

        self.flip()

    def on_draw(self):
        self.render()

    def run(self):
        try:
            while True:
                time.sleep(0.02)
                event = self.dispatch_events()
                try:
                    self.render()
                except ConnectionRefusedError:
                    time.sleep(1)
                    self.render_no_connection()
        except KeyboardInterrupt:
            try:
                self.proxy.stop()
            except ConnectionRefusedError:
                pass


if __name__ == '__main__':
    Window().run()
