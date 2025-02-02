

import math
from aircapitan.sim.planesim import PlaneSim

from aircapitan.instruments.base_instrument import BaseInstrument
import pygame
import sys


class DummyEventPoller(BaseInstrument):
    def __init__(self, cycle_interval: float):
        super().__init__(cycle_interval=cycle_interval)

    def on_cycle(self, timestamp):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
