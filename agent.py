import random
import math

def intersect(x, y, l, direct, x0, y0, r):
    x -= x0
    y -= y0
    a = x**2 + y**2 - r**2
    b = 2 * l * (x * math.sin(direct) + y * math.cos(direct))
    c = l**2
    disc = b**2 - 4 * a * c;
    if disc <= 0:
        return False
    sqrtdisc = math.sqrt(disc)
    t1 = (-b + sqrtdisc) / (2 * a);
    t2 = (-b - sqrtdisc) / (2 * a);
    if 0 < t1 < 1 and 0 < t2 < 1:
        return True
    return False

class Agent(object):
    def __init__(self, world):
        self.world = world

        self.x = random.random() * world.width
        self.y = random.random() * world.height
        self.v = random.random()
        self.direction = random.random() * math.pi * 2.0
        self.size = 50.0
        self.tile = None
        self.sight = 100.0
        self.update()


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
        for idx in range(-5, 6):
            sight_dir = self.direction + idx * math.pi / 15
            see = False
            for agent in agents:
                if intersect(self.x, self.y, self.sight, sight_dir, agent.x, agent.y, agent.size):
                    see = True
                    break
            vision.append(see)
        self.vision = vision

    def update(self):
        self.update_tile()
        self.update_vision()

    def to_dict(self):
        return {
                "x": self.x,
                "y": self.y,
                "v": self.v,
                "direction": self.direction,
                "size": self.size,
                "sight": self.sight,
                "vision": self.vision,
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
        self.update()
