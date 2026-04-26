from ..messlib.interfaces.host import Host
from ..messlib.data_structures.situation import Situation
import itertools
import functools

from tqdm import tqdm

# Legacy (?) imports
from ..messlib.data_structures.classes import Input, Action, FacingDirection
from ..messlib.data_structures.move_definitions import Inputs, Actions

# debug imports
from ..messlib.interfaces.vis import print_gamestate
from melee.enums import Character
from melee.enums import Action as MeleeAction



class PayoffSolver:
    """
    """
    def __init__(self, host: Host, situation: Situation):
        self.host = host
        self.situation = situation
        self.results = None

    def _debug_solve(self):
        self.host.situation_setup(self.situation)
        gs_init = self.host.save_savestate()
        # ^ what is this useful for?
        dash_timings = range(2, 4)
        aerial_timings = range(3, 6)
        n_sims = len(list(itertools.product(dash_timings, aerial_timings)))
        input_sets = self.compose_sims(dash_timings, aerial_timings)
        self.results = self.run_sims(input_sets)

    def run_sims(self, input_sets):
        results = {}
        for keys, sim_data in tqdm(input_sets.items()):
            print(keys)
            gs_loaded = self.host.load_last_savestate()
            p1_action: Action = sim_data[0]
            p2_action: Action = sim_data[1]
            p1_action.sequence_position = 0
            p2_action.sequence_position = 0
            res = "Whiff"
            for frame_cnt in range(60):
                p1_action.send_next_input(self.host.p1)
                p2_action.send_next_input(self.host.p2)
                gs = self.host.console.step()  # someday, replace with the host-step.
                print_gamestate(gs)

                if "DAMAGE" in str(gs.players[1].action):
                    res = "Falco win"
                    break
                if "DAMAGE" in str(gs.players[2].action):
                    res = "Fox win"
                    break
            results[keys] = res
        return results

    def compose_sims(self, dash_timings, aerial_timings):
        fox_partial = functools.partial(
            Actions.jump_cancelled_upsmash,
            character=Character.FOX,
            direction=FacingDirection.RIGHT,
        )
        falco_partial = functools.partial(
            Actions.sh_back_air,
            character=Character.FALCO,
            direction=FacingDirection.RIGHT,
            angle=0.0,
            drift=0.0,
            ff_frame=22,
        )

        return {
            (t1, t2):
            (fox_partial(frames_dashing=t1), falco_partial(slack_frames=t2))
            for t1, t2 in itertools.product(dash_timings, aerial_timings)
        }


"""
let's do something "trivial":

fox aim jc up smash,
falco AC bair.

for fox, parameters are:
 - AIM: how far to run
 - TIGHTNESS: which frame to input JCUS

for falco, parameters are:
 - AIM: jump angle
 - TIGHTNESS: aerial frame
 - TIGHTNESS: ff frame
"""


class ParameterizedAction:
    """
    data and visibility type. no ability to "send to game"

    scope is tbd, i did not whiteboard this yet
    """
    def __init__(self, *args):
        self.highlevel_seq = []
        for arg in args:
            self.highlevel_seq.append(arg)
        self.frame_seq = self._determine_frames(self.highlevel_seq)

    def _determine_frames(self, highlevel_sequence):
        ...
