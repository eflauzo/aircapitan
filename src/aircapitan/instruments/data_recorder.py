from aircapitan.sim.planesim import PlaneSim


class DataRecorder:
    def __init__(self, sim: PlaneSim, sampling_interval=0.01):
        self.sim = sim
        self.sampling_interval = sampling_interval
        self.last_time_recorded = 0

    def on_cycle():
        self.sim.dump
