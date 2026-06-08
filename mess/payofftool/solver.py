from ..messlib.interfaces.host import Host
from ..messlib.data_structures.situation import Situation
import itertools
import functools

from melee.enums import Character
from ..messlib.data_structures.classes import (
    Input,
    Action,
    FacingDirection,
    ParameterSpace,
    Variation,
)
from ..messlib.data_structures.move_definitions import Inputs, Actions

from .structures import PayoffReplayFrame, gs_to_replayframe


class PayoffSolver:
    """ """

    def __init__(self, host: Host, situation: Situation):
        self.host = host
        self.situation = situation
        self.results = None

    def run_sims(self, input_sets, cbk_text=None, cbk_bar=None):
        results = {}
        for i, sim_data in enumerate(input_sets):
            if cbk_text:
                cbk_text(f"{i}/{len(input_sets)}")
            if cbk_bar:
                cbk_bar(i / len(input_sets))
            gs_loaded = self.host.load_last_savestate()
            p1_action: Action = sim_data[0]
            p2_action: Action = sim_data[1]
            p1_action.sequence_position = 0
            p2_action.sequence_position = 0
            res = "Whiff"
            framelist = [gs_to_replayframe(gs_loaded)]
            for frame_cnt in range(60):
                p1_action.send_next_input(self.host.p1)
                p2_action.send_next_input(self.host.p2)
                gs = self.host.console.step()  # someday, replace with the host-step.
                # print_gamestate(gs)
                framelist.append(gs_to_replayframe(gs))
                if "DAMAGE" in str(gs.players[1].action):
                    if "DAMAGE" in str(gs.players[2].action):
                        res = "Trade"
                        break
                    else:
                        res = "Falco win"
                        break
                if "DAMAGE" in str(gs.players[2].action):
                    res = "Fox win"
                    break
            results[i] = (res, framelist)
        return results

    def compose_sims(
        self,
        params_structs: tuple[dict],
        situation: Situation,
        p1_base_action: str,
        p2_base_action: str,
    ):
        variations, constants = params_structs
        return [
            (
                getattr(Actions, p1_base_action)(
                    character=situation.p1_character,
                    direction=situation.p1_facing,
                    **variation["p1"],
                    **constants["p1"],
                ),
                getattr(Actions, p2_base_action)(
                    character=situation.p2_character,
                    direction=situation.p2_facing,
                    **variation["p2"],
                    **constants["p2"],
                ),
            )
            for variation in ParameterSpace(variations)
        ]
