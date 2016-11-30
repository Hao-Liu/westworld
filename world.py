import threading
import time
from xmlrpc.server import SimpleXMLRPCServer

from agent import Agent


class World(object):
    def __init__(self, n_agents=100, width=800, height=600):
        self.alive = True
        self.width = width
        self.height = height

        self.server = SimpleXMLRPCServer(("localhost", 8000), logRequests=False)
        self.server.register_introspection_functions()
        self.server.register_function(pow)
        self.server.register_function(self.get_agents)
        self.server_thread = threading.Thread(target=self.server.serve_forever)

        self.agents = []
        for i in range(n_agents):
            agent = self.spawn_agent()
            self.agents.append(agent)

    def get_agents(self):
        agents = []
        for agent in self.agents:
            agents.append((agent.x, agent.y, agent.size))
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

    def spawn_agent(self):
        return Agent(self)
