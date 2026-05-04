from ..messlib.interfaces.host import Host
from ..messlib.data_structures.situation import Situation
import itertools
import functools

from melee.enums import Character
from ..messlib.data_structures.classes import Input, Action, FacingDirection
from ..messlib.data_structures.move_definitions import Inputs, Actions

from .structures import PayoffReplayFrame, gs_to_replayframe


class PayoffSolver:
    """ """

    def __init__(self, host: Host, situation: Situation):
        self.host = host
        self.situation = situation
        self.results = None

    # def _debug_solve(self):
    #     self.host.situation_setup(self.situation)
    #     _ = self.host.save_savestate()
    #     # ^ what could the value be useful for?
    #     dash_timings = range(1, 8)
    #     aerial_timings = range(1, 8)
    #     # n_sims = len(list(itertools.product(dash_timings, aerial_timings)))
    #     input_sets = self.compose_sims(dash_timings, aerial_timings)
    #     self.results = self.run_sims(input_sets)
    #     self.host.console.stop()

    def run_sims(self, input_sets, cbk_text=None, cbk_bar=None):
        results = {}
        for i, (keys, sim_data) in enumerate(input_sets.items()):
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
            results[keys] = (res, framelist)
        return results

    def compose_sims(self, dash_timings, aerial_timings):
        from ..messlib.data_structures.classes import Drift

        fox_partial = functools.partial(
            Actions.jump_cancelled_upsmash,
            character=Character.FOX,
            direction=FacingDirection.RIGHT,
        )
        falco_partial = functools.partial(
            Actions.sh_back_air,
            character=Character.FALCO,
            direction=FacingDirection.RIGHT,
            jump_angle=Drift.FULLBACK,
            drift=Drift.NEUTRAL,
            ff_frame=22,
        )

        return {
            (t1, t2): (fox_partial(frames_dashing=t1), falco_partial(slack_frames=t2))
            for t1, t2 in itertools.product(dash_timings, aerial_timings)
        }
