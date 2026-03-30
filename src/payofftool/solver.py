from ..messlib.interfaces.host import Host
from ..messlib.data_structures.situation import Situation
import itertools

# Legacy (?) imports
from ..messlib.data_structures.classes import Input, Action, FacingDirection
from ..messlib.data_structures.move_definitions import Inputs, Actions

# debug imports
from ..messlib.interfaces.vis import print_gamestate
from melee.enums import Character


class PayoffSolver:
    """
    """
    def __init__(self, host: Host, situation: Situation):
        self.host = host
        self.situation = situation

    def initial_setup(self):
        self.host.situation_setup(self.situation)
        gs_init = self.host.save_savestate()
        # ^ what is this useful for?
        self.compose_sims()

    def run_sims(self):
        ...

    def compose_sims(self):
        fox_action = Actions.jump_cancelled_upsmash(
            Character.FOX,
            FacingDirection.RIGHT,
            12
        )
        falco_action = Actions.sh_back_air(
            Character.FALCO,
            FacingDirection.RIGHT,
            0.0,  # dummy
            0.0,  # dummy,
            3,
            22,
        )
        breakpoint()


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
