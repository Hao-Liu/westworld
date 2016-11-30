import pyglet
import time
import xmlrpc.client

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
        self.proxy = xmlrpc.client.ServerProxy('http://localhost:8000')

    def render(self):
        self.clear()
        agents = self.proxy.get_agents()
        for x, y, size in agents:
            circle = pyglet.sprite.Sprite(
                    img=self.circle_img,
                    x=x, y=y)
            circle.scale = size * 0.01
            circle.draw()

        #self.label.draw()
        self.flip()

    def on_draw(self):
        self.render()

    def run(self):
        i = 0
        while self.alive:
            i += 1
            time.sleep(0.01)
            event = self.dispatch_events()
            self.render()
