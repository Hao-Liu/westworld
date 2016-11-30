#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing

from world import World
from window import Window


if __name__ == '__main__':

    window = Window()
    window_proc = multiprocessing.Process(target=window.run)
    window_proc.start()

    world = World()
    world.run()
    window_proc.join()
