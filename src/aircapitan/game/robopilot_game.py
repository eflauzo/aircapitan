import pygame
import sys
import os
import math
from aircapitan.sim.planesim import PlaneSim
from aircapitan.game import game


if __name__ == '__main__':
    sim = PlaneSim()
    robo_pilot = RoboPilot()
    g = game.AirPlaneGame(sim, robo_pilot)
    g.run()
