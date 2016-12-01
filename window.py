import time
import xmlrpc.client
import math

import pyglet

class Window(pyglet.window.Window):
    def __init__(self, width=800, height=600):
        super(Window, self).__init__(width=width, height=height)
        self.alive = True
        self.label = pyglet.text.Label(
                'Hello, world',
                font_name='Times New Roman',
                font_size=36,
                x=self.width//2,
                y=self.height//2,
                anchor_x='center',
                anchor_y='center',
                )

        pyglet.resource.path = ['.']
        pyglet.resource.reindex()
        self.circle_img = pyglet.resource.image("circle.png")
        self.circle_img.anchor_x = self.circle_img.width / 2
        self.circle_img.anchor_y = self.circle_img.height / 2
        self.proxy = xmlrpc.client.ServerProxy('http://localhost:8000')

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
            keys = ['x', 'y', 'v', 'direction', 'size', 'sight']
            x, y, v, direction, size = (
                    agent.get(key) for key in keys)
            circle = pyglet.sprite.Sprite(
                    img=self.circle_img,
                    x=x, y=y)
            circle.scale = size * 0.1
            circle.draw()

            pyglet.gl.glColor4f(1.0, 0, 0, 1.0)
            pyglet.graphics.draw(
                    2,
                    pyglet.gl.GL_LINES,
                    ("v2f", (
                        x,
                        y,
                        x + circle.width * math.sin(direction),
                        y + circle.height * math.cos(direction))))

        #self.label.draw()
        self.flip()

    def on_draw(self):
        self.render()

    def run(self):
        while self.alive:
            time.sleep(0.01)
            event = self.dispatch_events()
            self.render()
