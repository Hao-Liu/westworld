from __future__ import division

import random
import math
import utils
import time

import numpy as np

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
        self.vision = [0.0 for _ in range(self.n_cell)]
        self.reward = 0

        self.t = 0
        self.y_batch = []
        self.a_batch = []
        self.s_batch = []

        self.step()

    def to_dict(self):
        keys = ("x", "y", "v", "direction", "size", "sight", "vision",
                "n_cell", "aov", "reward")
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

        self.reward = 0
        for agent in agents:
            if self.is_collide_with(agent):
                self.reward -= 1

    def is_collide_with(self, agent):
        dx = self.x - agent.x
        dy = self.y - agent.y
        if 4 * (dx**2 + dy**2) < (self.size + agent.size)**2:
            return True
        return False

    def update_position(self, accel, steer):
        if accel > 0.05:
            accel = 0.05
        elif accel < -0.05:
            accel = -0.05
        if steer > 0.05:
            steer = 0.05
        elif steer < -0.05:
            steer = -0.05

        self.direction += steer
        self.v += accel

        if self.direction > math.pi * 2:
            self.direction -= math.pi * 2

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

    def get_action(self):
        if random.random() < 0.5000:
            action = self.world.brain.get_action(self.vision)
        else:
            action = [(random.random() - 0.5) * 0.1 for _ in range(2)]
        return action

    def step(self, gamma=0.99, i_update=5):
        s_t = self.vision
        a_t = self.get_action()

        self.update_position(*a_t)
        self.update_tile()
        self.update_vision()

        s_t1 = self.vision
        r_t = np.clip(self.reward, -1, 1)

        q_t1 = self.world.brain.get_target_action(s_t1)
        self.y_batch.append(r_t + gamma * q_t1)
        self.a_batch.append(a_t)
        self.s_batch.append(s_t)
        if len(self.s_batch) % i_update:
            self.world.brain.session.run(
                self.world.brain.grad_update,
                feed_dict={
                    self.world.brain.y: self.y_batch,
                    self.world.brain.a: self.a_batch,
                    self.world.brain.s: self.s_batch
                }
            )
            self.y_batch = []
            self.a_batch = []
            self.s_batch = []


    def run(self):
        while self.world.running:
            time.sleep(0.002)
            self.step()
