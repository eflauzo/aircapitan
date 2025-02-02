

from aircapitan.quick_run import quick_run
from aircapitan.sim.planesim import PlaneSim
from aircapitan.instruments.data_recorder import DataRecorder
from aircapitan.robo_pilots.RoboBangBangRoll import RoboPilot
# quick_run()
from aircapitan.instruments.learn_simple import Sim2AI
import matplotlib.pyplot as plt

# def quick_plot(data_rec, tracks):
#    for track_name, track


def quick_plot(data_rec, channels):
    fig, axes = plt.subplots(len(channels), 1, sharex=True)
    for channel_number, channel in enumerate(channels):
        ax = axes[channel_number]
        if channel not in data_rec.dataset:
            raise RuntimeError(f"No such channel {channel}")

        ch = data_rec.dataset[channel]
        ax.plot(ch.ts, ch.values)
    plt.show()


def check_roll(TControlComponent):
    sim = PlaneSim()
    dt = 0.010
    dur_s = 15
    cc = TControlComponent(dt, sim)
    data_rec = DataRecorder(dt, sim)
    # error =

    quick_run(sim, components=[
        cc,
        data_rec,
    ], duration_s=dur_s, dt=dt)

    # df = data_rec.as_df()
    # print(df)

    Sim2AI(
        data_rec, [
            ('attitude/roll-rad', (-3.1416, 3.1416)),
            ('velocities/vtrue-fps', (-500, 500)),
        ], [
            ('fcs/aileron-cmd-norm', (-1.0, 1.0)),
        ]
    )

    quick_plot(data_rec, [
        'fcs/aileron-cmd-norm',
        # 'fcs/rudder-cmd-norm',
        'attitude/roll-rad',
        'velocities/vtrue-fps',
    ])


if __name__ == '__main__':

    check_roll(RoboPilot)
