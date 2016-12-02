#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing

from world import World
from window import Window


if __name__ == '__main__':
    world = World()
    world_proc = multiprocessing.Process(target=world.run)
    world_proc.start()
    window = Window()
    try:
        window.run()
    finally:
        world_proc.join()
