import threading
import time
from xmlrpc.server import SimpleXMLRPCServer

from agent import Agent
from tile import Tile


class World(object):
    def __init__(self, n_agents=20, width=800, height=600):
        self.alive = True
        self.width = width
        self.height = height

        self.server = SimpleXMLRPCServer(("localhost", 8000), logRequests=False)
        self.server.register_introspection_functions()
        self.server.register_function(self.get_agents)
        self.server.register_function(self.get_tiles)
        self.server_thread = threading.Thread(target=self.server.serve_forever)

        self.tiles = []
        for i in range(8):
            for j in range(6):
                tile = Tile(self, i*100, j*100, 100, 100)
                self.tiles.append(tile)
        self.agents = []
        for i in range(n_agents):
            agent = Agent(self)
            self.agents.append(agent)

    def get_tiles(self):
        tiles = []
        for tile in self.tiles:
            tiles.append(tile.to_dict())
        return tiles

    def get_agents(self):
        agents = []
        for agent in self.agents:
            agents.append(agent.to_dict())
        return agents

    def run(self):
        print("Listening on port 8000...")
        self.server_thread.start()
        try:
            while True:
                time.sleep(0.01)
                for agent in self.agents:
                    agent.step()
        except KeyboardInterrupt:
            self.alive = False
            self.server.shutdown()
            self.server.server_close()
            self.server_thread.join()
