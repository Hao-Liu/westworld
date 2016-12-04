#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools
import math
import threading
import time
from xmlrpc.server import SimpleXMLRPCServer

from agent import Agent
from tile import Tile
from brain import Brain


class World(object):
    tile_size = 50
    def __init__(self, n_agents=10, width=800, height=600):
        self.running = False
        self.width = width
        self.height = height
        self.brain = Brain()

        self.server = SimpleXMLRPCServer(("localhost", 8000), logRequests=False, allow_none=True)
        self.server.register_introspection_functions()
        self.server.register_function(self.get_agents)
        self.server.register_function(self.get_tiles)
        self.server.register_function(self.stop)
        self.server_thread = threading.Thread(target=self.server.serve_forever)

        self.tiles_x = math.ceil(self.width / self.tile_size)
        self.tiles_y = math.ceil(self.height / self.tile_size)

        self.tiles = [[
            Tile(self,
                 x*self.tile_size,
                 y*self.tile_size,
                 self.tile_size,
                 self.tile_size,
                 self.tile_size)
            for y in range(self.tiles_y)]
            for x in range(self.tiles_x)]

        self.agents = []
        for i in range(n_agents):
            agent = Agent(self)
            self.agents.append(agent)
        self.agent_threads = [
            threading.Thread(target=agent.run)
            for agent in self.agents
        ]

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

    def run(self):
        self.server_thread.start()
        try:
            self.running = True
            for t in self.agent_threads:
                t.start()

            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Canceled by user")
            self.running = False
        finally:
            self.server.shutdown()
            self.server.server_close()
            self.server_thread.join()
            for t in self.agent_threads:
                t.join()

    def stop(self):
        self.running = False

if __name__ == '__main__':
    World().run()
