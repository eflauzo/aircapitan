import math
from aircapitan.sim.planesim import PlaneSim

from aircapitan.instruments.base_instrument import BaseInstrument


class RoboPilot(BaseInstrument):
    def __init__(self, cycle_interval: float, sim: PlaneSim):
        super().__init__(cycle_interval=cycle_interval)
        self.sim = sim

    def on_cycle(self, timestamp):
        self.sim.set_cmd_thrust(1.0)
        print("act")
        plane_roll_deg = math.degrees(self.sim.plane_roll_rad)
        if plane_roll_deg > 15:
            self.output_aileron = -1
            print('left aileron')
        elif plane_roll_deg < -15:
            self.output_aileron = 1
            print('right aileron')
        else:
            self.output_aileron = 0
        self.sim.set_cmd_aileron(self.output_aileron)


'''
class RoboPilot:
    def __init__(self):
        self.act_interval = 0.5
        self.last_time_acted = 0
        self.output_aileron = 0

    def process_inputs(self, sim: PlaneSim):
        time_now = sim.fdm_time_s

        if (time_now - self.last_time_acted) > self.act_interval:
            # act
            sim.set_cmd_thrust(1.0)
            print("act")
            plane_roll_deg = math.degrees(sim.plane_roll_rad)
            if plane_roll_deg > 15:
                self.output_aileron = -1
            elif plane_roll_deg < -15:
                self.output_aileron = 1
            else:
                self.output_aileron = 0

            sim.set_cmd_aileron(self.output_aileron)
            self.last_time_acted = time_now
        # if last_time_acted + self.
'''
