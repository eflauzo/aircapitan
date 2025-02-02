from aircapitan.sim.planesim import PlaneSim
from aircapitan.instruments.base_instrument import BaseInstrument
from collections import defaultdict
import pandas as pd


class DataRecorderChannel:
    def __init__(self):
        self.ts = []
        self.values = []

    def append(self, ts, value):
        if len(self.ts) > 0:
            if self.ts[-1] > ts:
                raise RuntimeError('index out of order')
        self.ts.append(ts)
        self.values.append(value)


class DataRecorder(BaseInstrument):
    def __init__(self, cycle_interval: float, sim: PlaneSim):
        super().__init__(cycle_interval=cycle_interval)
        self.sim = sim
        self.dataset = defaultdict(DataRecorderChannel)

        # self.

    def as_df(self):
        all_channels = list(self.dataset.keys())
        if len(all_channels) == 0:
            raise RuntimeError('No data')
        first_ch = all_channels[0]
        for ch in all_channels:
            assert len(self.dataset[ch].ts) == len(self.dataset[ch].values)
            assert len(self.dataset[ch].ts) == len(self.dataset[first_ch].ts)
        # index = self.dataset[first_ch].ts
        as_dict = {}
        for ch, ch_data in self.dataset.items():
            as_dict[ch] = ch_data.values
        df = pd.DataFrame(as_dict, index=self.dataset[first_ch].ts)
        return df

    def on_cycle(self, timestamp):
        data = self.sim.dump_all_properties()
        for k, v in data.items():
            self.dataset[k].append(timestamp, v)
