from ..messlib.interfaces.host import Host
from ..messlib.data_structures.situation import Situation
from melee.enums import Character
from ..messlib.data_structures.classes import (
    Action,
    FacingDirection,
)
from ..messlib.data_structures.move_definitions import Inputs, Actions

from .structures import gs_to_replayframe
import itertools


class PayoffSolver:
    """\
    ...
    """

    def __init__(self, host: Host, situation: Situation):
        self.host = host
        self.situation = situation
        self.results = None
        self.axes = None

    def run_sims(self, input_sets, cbk_text=None, cbk_bar=None):
        results = {}
        for i, sim_data in enumerate(input_sets):
            if cbk_text:
                cbk_text(f"{i}/{len(input_sets)}")
            if cbk_bar:
                cbk_bar(i / len(input_sets))
            gs_loaded = self.host.load_last_savestate()
            grid_coords: tuple[int] = sim_data[0]
            p1_action: Action = sim_data[1]
            p2_action: Action = sim_data[2]
            p1_action.sequence_position = 0
            p2_action.sequence_position = 0
            res = "Whiff"
            framelist = [gs_to_replayframe(gs_loaded)]
            for frame_cnt in range(60):
                p1_action.send_next_input(self.host.p1)
                p2_action.send_next_input(self.host.p2)
                gs = self.host.console.step()  # someday, replace with the host-step.
                framelist.append(gs_to_replayframe(gs))
                if "DAMAGE" in str(gs.players[1].action):
                    if "DAMAGE" in str(gs.players[2].action):
                        res = "Trade"
                        break
                    else:
                        res = "P2 win"
                        break
                if "DAMAGE" in str(gs.players[2].action):
                    res = "P1 win"
                    break
            results[grid_coords] = (res, framelist)
        return results

    def compose_sims(
        self,
        params_structs: tuple[dict],
        situation: Situation,
        p1_base_action: str,
        p2_base_action: str,
    ):
        variations, constants = params_structs
        from .structures import ParamAxis

        axes = []
        for pxx, var_list in variations.items():
            for var in var_list:
                axes.append(ParamAxis(pxx, var[0], var[1]))
        self.axes = axes

        product_iterator = itertools.product(*axes)

        def axestup_to_dict(inp, pxx):
            return {b: c for a, b, c in inp if a == pxx}

        return [
            (
                point,
                getattr(Actions, p1_base_action)(
                    character=situation.p1_character,
                    direction=situation.p1_facing,
                    **axestup_to_dict(point, "p1"),
                    **constants["p1"],
                ),
                getattr(Actions, p2_base_action)(
                    character=situation.p2_character,
                    direction=situation.p2_facing,
                    **axestup_to_dict(point, "p2"),
                    **constants["p2"],
                ),
            )
            for point in product_iterator
        ]

    def results_slice(self, ax_x: str, ax_y: str, **kwargs):
        if not self.results:
            raise ValueError("No results computed yet.")
        axis_names = [ax.param_name for ax in self.axes]
        if ax_x not in axis_names or ax_y not in axis_names:
            raise ValueError(
                "specified results-slice names do not match: "
                f"selecting {ax_x, ax_y} from {axis_names}"
            )
        # TODO: even more input validation here (on the kwargs).

        ax_x_full = [a for a in self.axes if a.param_name == ax_x][0]
        ax_y_full = [a for a in self.axes if a.param_name == ax_y][0]

        constants = []
        for add_k, add_v in kwargs.items():
            px, param = add_k.split("_", 1)
            constants.append((px, param, add_v))
        if not constants:
            # TODO: use "defaults" for slices when not enough params given
            raise NotImplementedError("woof")

        # REMINDER: we overloaded __iter__ for ParamAxis type. :)!!
        grid_iterator = itertools.product(ax_x_full, ax_y_full, constants)
        return [self.results[g] for g in grid_iterator]
