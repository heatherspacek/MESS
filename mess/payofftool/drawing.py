import dearpygui.dearpygui as dpg
from melee.enums import Action
from mess.animations.data import (
    HurtBoxProcessed,
    retrieve_character_data,
    retrieve_move_data,
)
from mess.animations.vis import lerp_2d

from ..messlib.data_structures.translations import best_match_anim
from .structures import FacingDirection, PayoffReplayFrame


def dpg_draw_capsule(y1, z1, y2, z2, size, parent="canvas", color=(255, 255, 255, 255)):
    for t in [a / 9 for a in range(10)]:
        x, y = lerp_2d((y1, z1), (y2, z2), t)
        dpg.draw_circle([x, y], size, parent=parent, color=color)


def draw_preview_frame():
    def bracket_extract(in_str: str):
        leftbracky = in_str.find("(")
        rightbracky = in_str.find(")")
        return in_str[leftbracky + 1 : rightbracky]

    p1x = dpg.get_value("p1x")
    p1f = dpg.get_value("p1facing")
    p2x = dpg.get_value("p2x")
    p2f = dpg.get_value("p2facing")
    p1color = (200, 200, 255, 255)
    p2color = (200, 255, 200, 255)

    isopath = dpg.get_value("loaded_iso_path")

    animations_list_ch1, _, _ = retrieve_character_data(
        isopath,
        int(bracket_extract(dpg.get_value("p1c"))),
    )
    idle1, _ = retrieve_move_data(
        isopath,
        int(bracket_extract(dpg.get_value("p1c"))),
        animations_list_ch1.index(
            best_match_anim(Action.STANDING, animations_list_ch1)
        ),
    )
    animations_list_ch2, _, _ = retrieve_character_data(
        isopath,
        int(bracket_extract(dpg.get_value("p2c"))),
    )
    idle2, _ = retrieve_move_data(
        isopath,
        int(bracket_extract(dpg.get_value("p2c"))),
        animations_list_ch2.index(
            best_match_anim(Action.STANDING, animations_list_ch2)
        ),
    )
    idle1_thisframe: list[HurtBoxProcessed] = idle1[dpg.get_frame_count() % len(idle1)]
    idle2_thisframe: list[HurtBoxProcessed] = idle2[dpg.get_frame_count() % len(idle2)]
    dpg.delete_item("preview_canvas", children_only=True)
    dpg.draw_rectangle(pmin=[10, 10], pmax=[290, 190], parent="preview_canvas")

    DRAW_SCALE = 4
    X_DRAW_OFFSET = 35
    Y_DRAW_OFFSET = 30

    def x_tform(x, world_x, facing: bool):
        x_faced = -x if facing else x
        return DRAW_SCALE * (X_DRAW_OFFSET + world_x + x_faced)

    def y_tform(y, world_y):
        return DRAW_SCALE * (Y_DRAW_OFFSET - (world_y + y))

    for hx in idle1_thisframe:
        x1, y1, z1 = hx.pos_a
        x2, y2, z2 = hx.pos_b
        scale = hx.size
        dpg_draw_capsule(
            x_tform(z1, p1x, p1f),
            y_tform(y1, 0),
            x_tform(z2, p1x, p1f),
            y_tform(y2, 0),
            scale * DRAW_SCALE,
            parent="preview_canvas",
            color=p1color,
        )
    for hx in idle2_thisframe:
        x1, y1, z1 = hx.pos_a
        x2, y2, z2 = hx.pos_b
        scale = hx.size
        dpg_draw_capsule(
            x_tform(z1, p2x, p2f),
            y_tform(y1, 0),
            x_tform(z2, p2x, p2f),
            y_tform(y2, 0),
            scale * DRAW_SCALE,
            parent="preview_canvas",
            color=p2color,
        )


def draw_replay_frame():
    PLAYBACK_SPEED = 2

    def bracket_extract(in_str: str):
        leftbracky = in_str.find("(")
        rightbracky = in_str.find(")")
        return in_str[leftbracky + 1 : rightbracky]

    res = dpg.get_item_user_data("solver_dummy").results
    if res is None:
        return  # no results yet.

    hovered_data = dpg.get_item_user_data("resultsprint")
    if hovered_data is None:
        dummy_index = list(res.keys())[0]
        frame_seq = res[dummy_index][1]
    else:
        outcome_label, frame_seq = hovered_data

    indices_loop = list(range(len(frame_seq)))
    for _ in range(7):
        indices_loop.append(indices_loop[-1])

    frame_loop_i = indices_loop[
        (dpg.get_frame_count() // PLAYBACK_SPEED) % len(indices_loop)
    ]
    repl_frame_to_draw: PayoffReplayFrame = frame_seq[frame_loop_i]

    p1x = repl_frame_to_draw.p1_pos.x
    p1y = repl_frame_to_draw.p1_pos.y
    p1f = repl_frame_to_draw.p1_facing
    p2x = repl_frame_to_draw.p2_pos.x
    p2y = repl_frame_to_draw.p2_pos.y
    p2f = repl_frame_to_draw.p2_facing

    p1color = (200, 200, 255, 255)
    p2color = (200, 255, 200, 255)
    if "DAMAGE" in repl_frame_to_draw.p1_game_action.name:
        p1color = (200, 200 / 1.3, 255 / 1.3, 255)
    if "DAMAGE" in repl_frame_to_draw.p2_game_action.name:
        p2color = (200, 255 / 1.3, 200 / 1.3, 255)

    from mess.animations.data import retrieve_character_data

    isopath = dpg.get_value("loaded_iso_path")

    animations_list_ch1, _, _ = retrieve_character_data(
        isopath,
        int(bracket_extract(dpg.get_value("p1c"))),
    )
    animations_list_ch2, _, _ = retrieve_character_data(
        isopath,
        int(bracket_extract(dpg.get_value("p2c"))),
    )
    hurts1, hits1 = retrieve_move_data(
        isopath,
        int(bracket_extract(dpg.get_value("p1c"))),
        animations_list_ch1.index(
            best_match_anim(repl_frame_to_draw.p1_game_action, animations_list_ch1)
        ),
    )
    hurts2, hits2 = retrieve_move_data(
        isopath,
        int(bracket_extract(dpg.get_value("p2c"))),
        animations_list_ch2.index(
            best_match_anim(repl_frame_to_draw.p2_game_action, animations_list_ch2)
        ),
    )

    hurts1_thisframe: list[HurtBoxProcessed] = hurts1[
        (repl_frame_to_draw.p1_game_action_frame) % len(hurts1)
    ]
    hurts2_thisframe: list[HurtBoxProcessed] = hurts2[
        (repl_frame_to_draw.p2_game_action_frame) % len(hurts2)
    ]
    hits1_thisframe = [
        h for h in hits1 if h.frame_i == repl_frame_to_draw.p1_game_action_frame
    ]
    hits2_thisframe = [
        h for h in hits2 if h.frame_i == repl_frame_to_draw.p2_game_action_frame
    ]

    dpg.delete_item("canvas", children_only=True)
    dpg.draw_rectangle(pmin=[10, 10], pmax=[290, 190], parent="canvas")

    DRAW_SCALE = 4
    X_DRAW_OFFSET = 35
    Y_DRAW_OFFSET = 30

    def x_tform(x, world_x, facing: FacingDirection):
        x_faced = -x if facing == "LEFT" else x
        return DRAW_SCALE * (X_DRAW_OFFSET + world_x + x_faced)

    def y_tform(y, world_y):
        return DRAW_SCALE * (Y_DRAW_OFFSET - (world_y + y))

    for hx in hurts1_thisframe:
        x1, y1, z1 = hx.pos_a
        x2, y2, z2 = hx.pos_b
        scale = hx.size
        dpg_draw_capsule(
            x_tform(z1, p1x, p1f),
            y_tform(y1, p1y),
            x_tform(z2, p1x, p1f),
            y_tform(y2, p1y),
            scale * DRAW_SCALE,
            color=p1color,
        )
    for hx in hurts2_thisframe:
        x1, y1, z1 = hx.pos_a
        x2, y2, z2 = hx.pos_b
        scale = hx.size
        dpg_draw_capsule(
            x_tform(z1, p2x, p2f),
            y_tform(y1, p2y),
            x_tform(z2, p2x, p2f),
            y_tform(y2, p2y),
            scale * DRAW_SCALE,
            color=p2color,
        )
    for htx in hits1_thisframe:
        _, y, z = htx.pos
        dpg.draw_circle(
            (
                x_tform(z, p1x, p1f),
                y_tform(y, p1y),
            ),
            htx.size * DRAW_SCALE,
            parent="canvas",
            color=(255, 0, 0, 255),
        )
    for htx in hits2_thisframe:
        _, y, z = htx.pos
        dpg.draw_circle(
            (
                x_tform(z, p2x, p2f),
                y_tform(y, p2y),
            ),
            htx.size * DRAW_SCALE,
            parent="canvas",
            color=(255, 0, 0, 255),
        )
