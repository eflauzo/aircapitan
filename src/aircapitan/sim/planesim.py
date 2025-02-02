import jsbsim
import math
import os

sim_root = os.path.dirname(os.path.realpath(__file__))


def limit(v, min_v, max_v):
    return max(min_v, min(v, max_v))


def limit_neg_pos_one(v):
    return limit(v, -1.0, 1.0)


class PlaneSim(object):

    def __init__(self):
        self.sim_time_s = 0.0
        self.position_m = 0

        # cmd
        self.cmd_thrust_level = 0.0
        self.cmd_elevator = 0.0
        self.cmd_rudder = 0.0
        self.cmd_aileron = 0.0

        # size
        self.height_m = 11.76
        self.length_m = 37.57
        self.crashed = False

        self.fdm = jsbsim.FGFDMExec(
            os.path.join(sim_root, 'jsbsim')
        )

        self.fdm.load_model("c172p")
        jsbsim.FGJSBBase().debug_lvl = 1

        self.fdm['propulsion/starter_cmd'] = 1
        self.fdm['fcs/throttle-cmd-norm[0]'] = 0.0
        # todo check is this both magnetos
        self.fdm['propulsion/magneto_cmd'] = 1

        self.fdm['ic/h-agl-ft'] = 500.0
        self.fdm['ic/vc-kts'] = 60

        self.all_properties = []
        for property_raw in self.fdm.query_property_catalog('').split('\n'):
            if ' (W)' in property_raw:
                # ignore write only properies
                continue
            property_name = property_raw.replace(
                ' (RW)', '').replace(' (R)', '')
            self.all_properties.append(property_name)

        self.fdm.run_ic()

    def dump_all_properties(self):
        result = {}
        for property_name in self.all_properties:
            # print('>>>', property_name)
            result[property_name] = self.fdm[property_name]
        return result

    @property
    def fdm_time_s(self):
        return self.fdm['simulation/sim-time-sec']

    @property
    def altitude_m(self):
        return self.fdm['position/h-agl-km'] * 1000

    @property
    def vertical_speed_mps(self):
        return self.fdm['velocities/v-down-fps'] * 0.3048

    @property
    def ground_speed_mps(self):
        return self.fdm['velocities/vg-fps'] * 0.3048

    @property
    def airspeed_mps(self):
        return self.fdm['velocities/vtrue-fps'] * 0.3048

    @property
    def plane_pitch_rad(self):
        return self.fdm['attitude/pitch-rad']

    @property
    def plane_heading_rad(self):
        return self.fdm['attitude/heading-true-rad']

    @property
    def plane_roll_rad(self):
        return self.fdm['attitude/roll-rad']

    @property
    def engine_rpm(self):
        return self.fdm['propulsion/engine/engine-rpm']

    def set_cmd_elevator(self, v):
        # jsbsim is unique (negative elevator is a positive pitch)
        # -1 is yoke pulled all the way and +1 is when yoke pushed all
        # the way

        norm_pitch = limit_neg_pos_one(v)
        self.cmd_elevator = norm_pitch
        self.fdm['fcs/elevator-cmd-norm'] = norm_pitch

    def get_cmd_elevator(self):
        return self.cmd_elevator

    def set_cmd_rudder(self, v):
        norm_rudder = limit_neg_pos_one(v)
        self.cmd_rudder = norm_rudder
        self.fdm['fcs/rudder-cmd-norm'] = norm_rudder

    def get_cmd_rudder(self):
        return self.cmd_rudder

    def set_cmd_aileron(self, v):
        norm_aileron = limit_neg_pos_one(v)
        self.cmd_aileron = norm_aileron
        self.fdm['fcs/aileron-cmd-norm'] = norm_aileron

    def get_cmd_aileron(self):
        return self.cmd_aileron

    def set_cmd_thrust(self, v):
        norm_thrust = limit_neg_pos_one(v)
        self.cmd_thrust_level = norm_thrust
        self.fdm['fcs/throttle-cmd-norm'] = self.cmd_thrust_level
        self.fdm['fcs/mixture-cmd-norm'] = 1.0

    def get_cmd_thrust(self):
        return self.cmd_thrust_level

    def propagate(self, dt):
        self.sim_time_s += dt
        self.fdm.set_dt(dt)
        self.fdm.run()
        self.position_m += dt * (self.fdm['velocities/vg-fps'] * 0.3048)
