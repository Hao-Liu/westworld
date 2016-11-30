import random

class Agent(object):
    def __init__(self, world):
        self.world = world
        self.x = random.random() * world.width
        self.y = random.random() * world.height
        self.vx = random.random() * 4.0 - 2.0
        self.vy = random.random() * 4.0 - 2.0
        self.size = random.random()

    def step(self):
        self.vx = random.random() * 4.0 - 2.0
        self.vy = random.random() * 4.0 - 2.0
        self.x += self.vx
        self.y += self.vy
        if self.x > self.world.width:
            self.x = 0
        if self.x < 0:
            self.x = self.world.width
        if self.y > self.world.height:
            self.y = 0
        if self.y < 0:
            self.y = self.world.height
