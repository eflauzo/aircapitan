
class BaseInstrument:

    def __init__(self, cycle_interval):
        self.cycle_interval = cycle_interval
        self.last_time_executed = None

    def poke(self, time_now):
        need_to_run = False
        if self.last_time_executed is None:
            need_to_run = True
        else:
            time_passed = abs(time_now - self.last_time_executed)
            if time_passed >= self.cycle_interval:
                need_to_run = True

        if need_to_run:
            self.last_time_executed = time_now
            self.on_cycle(time_now)

    def on_cycle(self, time_now):
        raise RuntimeError('Implement Me')
