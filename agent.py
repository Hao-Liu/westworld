from __future__ import division

import random
import math
import utils

class Agent(object):
    def __init__(self, world):
        self.world = world

        self.x = random.random() * world.width
        self.y = random.random() * world.height
        self.v = random.random()
        self.direction = random.random() * math.pi * 2.0
        self.size = random.random() * 100.0
        self.tile = None
        self.n_cell = 10
        self.aov = 120 * math.pi / 180
        self.sight = 100.0
        self.update()

    def to_dict(self):
        keys = "x", "y", "v", "direction", "size", "sight", "vision", "n_cell", "aov"
        return {key: self.__dict__[key] for key in keys}


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
        agents = set()
        for tile in self.tile.neighbors(self.sight):
            agents.update(tile.agents)
        agents.remove(self)

        vision = []
        for sight_dir in utils.linspace(- self.aov / 2, self.aov / 2, self.n_cell):
            sight_dir = self.direction + sight_dir
            min_sight = 1.0
            for agent in agents:
                sight = utils.intersect(self.x, self.y, self.sight, sight_dir, agent.x, agent.y, agent.size / 2)
                min_sight = min(sight, min_sight)
            vision.append(min_sight)
        self.vision = vision

    def update(self):
        self.update_tile()
        self.update_vision()

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

        self.vx = self.v * math.cos(self.direction)
        self.vy = self.v * math.sin(self.direction)
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
        self.update()
