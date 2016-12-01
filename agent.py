import random
import math

class Agent(object):
    def __init__(self, world):
        self.world = world

        self.x = random.random() * world.width
        self.y = random.random() * world.height
        self.tile = None
        self.sight = 100.0
        self.update_tile()

        self.v = random.random()
        self.direction = random.random() * math.pi * 2.0
        self.size = 1.0

    def update_tile(self):
        tile_x = int(self.x / self.world.tile_size)
        tile_y = int(self.y / self.world.tile_size)
        tile = self.world.tiles[tile_x][tile_y]
        if tile != self.tile:
            last_tile = self.tile
            if last_tile:
                last_tile.agents.remove(self)
            tile.agents.add(self)
            self.tile = tile

    def update_vision(self):
        for tile in self.tile.neighbors(self.sight):
            pass

    def to_dict(self):
        return {
                "x": self.x,
                "y": self.y,
                "v": self.v,
                "direction": self.direction,
                "size": self.size,
                }

    def step(self):
        self.direction += (random.random() - 0.5) * 0.1
        if self.direction > math.pi * 2:
            self.direction -= math.pi * 2

        self.dv = (random.random() - 0.5) * 0.1
        self.v += self.dv
        if self.v < 0.0:
            self.v = 0.0
        if self.v > 1.0:
            self.v = 1.0

        self.vx = self.v * math.sin(self.direction)
        self.vy = self.v * math.cos(self.direction)
        self.x += self.vx
        self.y += self.vy
        if self.x >= self.world.width:
            self.x = 1e-6
        if self.x <= 0:
            self.x = self.world.width - 1e-6
        if self.y >= self.world.height:
            self.y = 1e-6
        if self.y <= 0:
            self.y = self.world.height - 1e-6
        self.update_tile()

        self.update_vision()
