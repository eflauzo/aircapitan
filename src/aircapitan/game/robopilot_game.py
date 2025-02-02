import pygame
import sys
import os
import math
from aircapitan.sim.planesim import PlaneSim
from aircapitan.game import game
from aircapitan.robo_pilots.RoboBangBangRoll import RoboPilot
from aircapitan.instruments.dummy_event_poller import DummyEventPoller

if __name__ == '__main__':
    sim = PlaneSim()
    robo_pilot = RoboPilot(0.05, sim)
    event_poller = DummyEventPoller(0.5)
    g = game.AirPlaneGame(sim, [robo_pilot, event_poller])
    g.run()
