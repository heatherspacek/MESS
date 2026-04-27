from dataclasses import dataclass
from ..messlib.data_structures.classes import FacingDirection
import melee


@dataclass
class PayoffReplayFrame:
    p1_game_action: melee.enums.Action
    p1_game_action_frame: int
    p1_pos: tuple[int]
    p1_facing: FacingDirection
    p2_game_action: melee.enums.Action
    p2_game_action_frame: int
    p2_pos: tuple[int]
    p2_facing: FacingDirection


def gs_to_replayframe(gs: melee.GameState) -> PayoffReplayFrame:
    p1 = gs.players[1]
    p2 = gs.players[2]
    return PayoffReplayFrame(
        p1_facing=FacingDirection("RIGHT" if p1.facing else "LEFT"),
        p2_facing=FacingDirection("RIGHT" if p2.facing else "LEFT"),
        p1_game_action=p1.action,
        p2_game_action=p2.action,
        p1_game_action_frame=p1.action_frame,
        p2_game_action_frame=p2.action_frame,
        p1_pos=p1.position,
        p2_pos=p2.position,
    )
