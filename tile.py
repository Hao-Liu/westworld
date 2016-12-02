import random
import math

class Tile(object):
    def __init__(self, world, x, y, width, height, size):
        self.world = world
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.size = size
        self.nutrition = random.random()
        self.agents = set()

    def to_dict(self):
        keys = "x", "y", "width", "height", "nutrition"
        result = {key: self.__dict__[key] for key in keys}
        result['n_agents'] = len(self.agents)
        return result

    def neighbors(self, distance):
        nblk = math.ceil(distance / self.size)
        x = int(self.x / self.size)
        y = int(self.y / self.size)

        tiles = []
        for dx in range(-nblk, nblk+1):
            for dy in range(-nblk, nblk+1):
                nx = x + dx
                ny = y + dy
                if nx >= self.world.tiles_x:
                    nx -= self.world.tiles_x
                if ny >= self.world.tiles_y:
                    ny -= self.world.tiles_y
                tiles.append(self.world.tiles[nx][ny])
        return tiles
