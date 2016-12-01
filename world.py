import itertools
import math
import threading
import time
from xmlrpc.server import SimpleXMLRPCServer

from agent import Agent
from tile import Tile


class World(object):
    tile_size = 100
    def __init__(self, n_agents=20, width=800, height=600):
        self.alive = True
        self.width = width
        self.height = height

        self.server = SimpleXMLRPCServer(("localhost", 8000), logRequests=False)
        self.server.register_introspection_functions()
        self.server.register_function(self.get_agents)
        self.server.register_function(self.get_tiles)
        self.server_thread = threading.Thread(target=self.server.serve_forever)

        self.tiles_x = math.ceil(self.width / self.tile_size)
        self.tiles_y = math.ceil(self.height / self.tile_size)

        self.tiles = [[Tile(self, x*100, y*100, 100, 100, self.tile_size)
            for y in range(self.tiles_y)]
            for x in range(self.tiles_x)]

        self.agents = []
        for i in range(n_agents):
            agent = Agent(self)
            self.agents.append(agent)

    def get_tiles(self):
        tiles = []
        for tile in itertools.chain.from_iterable(self.tiles):
            tiles.append(tile.to_dict())
        return tiles

    def get_agents(self):
        agents = []
        for agent in self.agents:
            agents.append(agent.to_dict())
        return agents

    def step(self):
        time.sleep(0.002)
        for agent in self.agents:
            agent.step()

    def run(self):
        print("Listening on port 8000...")
        self.server_thread.start()
        try:
            while True:
                self.step()
        except KeyboardInterrupt:
            self.alive = False
            self.server.shutdown()
            self.server.server_close()
            self.server_thread.join()
