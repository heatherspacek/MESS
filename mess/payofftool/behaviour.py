import dearpygui.dearpygui as dpg
import numpy as np
from melee.enums import Character, Stage

from ..messlib.data_structures.classes import (
    Drift,
    FacingDirection,
)
from ..messlib.data_structures.situation import Situation
from ..messlib.interfaces.host import Host
from .solver import PayoffSolver
from .structures import ParamAxis, PayoffReplayFrame


def parse_from_window_settings() -> Situation:
    def bracket_extract(in_str: str):
        leftbracky = in_str.find("(")
        rightbracky = in_str.find(")")
        return in_str[leftbracky + 1 : rightbracky]

    stg_idx = int(bracket_extract(dpg.get_value("stg")))
    p1c_idx = int(bracket_extract(dpg.get_value("p1c")))
    p2c_idx = int(bracket_extract(dpg.get_value("p2c")))

    return Situation(
        stage=Stage(stg_idx),
        p1_character=Character(p1c_idx),
        p1_percent=int(dpg.get_value("p1p")),
        p1_platform=dpg.get_value("p1plat"),
        p1_facing=dpg.get_value("p1facing"),
        p1_x_position=dpg.get_value("p1x"),
        p2_character=Character(p2c_idx),
        p2_percent=int(dpg.get_value("p2p")),
        p2_platform=dpg.get_value("p1plat"),
        p2_facing=dpg.get_value("p2facing"),
        p2_x_position=dpg.get_value("p2x"),
    )


def varybox_ticked(checkbox_identifier, unused1, unused2):
    grp = dpg.get_item_parent(checkbox_identifier)
    ch = [dpg.get_item_alias(i) for i in dpg.get_item_children(grp, 1)]
    vary_item = [i for i in ch if "vary" in i][0]
    set_value_item = [i for i in ch if "value" in i][0]

    if dpg.get_value(checkbox_identifier):
        # Became checked
        dpg.hide_item(set_value_item)
        dpg.show_item(vary_item)
    else:
        # Became UN-checked
        dpg.hide_item(vary_item)
        dpg.show_item(set_value_item)


def select_action(dispatcher_uid, selection, user_data):
    # ** `user_data` contains either "p1" or "p2".
    import inspect

    from ..messlib.data_structures.move_definitions import Actions

    non_parameterizable = ["character", "direction"]
    add_to: str = user_data + "act_dynamicgroup"

    selected_function_handle = getattr(Actions, selection)
    func_sig = inspect.signature(selected_function_handle)

    dpg.delete_item(item=add_to, children_only=True)
    for param_name, param_info in func_sig.parameters.items():
        if param_name in non_parameterizable:
            continue
        with dpg.group(
            horizontal=True, parent=add_to, tag=f"{user_data}_group_{param_name}"
        ):
            # keep in mind this is (only) the TYPE HINT!
            if param_info.annotation is float:
                # dpg.add_input_float(label=param_name, parent=add_to)
                ...
            if param_info.annotation is int:
                dpg.add_text("vary?")
                dpg.add_checkbox(
                    tag=f"{user_data}_checkbox_{param_name}", callback=varybox_ticked
                )
                dpg.add_input_int(
                    label=param_name, tag=f"{user_data}_value_{param_name}"
                )
                dpg.add_input_intx(
                    size=2,
                    label=param_name,
                    callback=range_check,
                    tag=f"{user_data}_varyrange_{param_name}",
                    show=False,
                )
            if param_info.annotation is Drift:
                dpg.add_text("vary?")
                dpg.add_checkbox(
                    tag=f"{user_data}_checkbox_{param_name}", callback=varybox_ticked
                )
                dpg.add_combo(
                    [d.value for d in Drift],
                    label=param_name,
                    default_value=Drift.NEUTRAL,
                    tag=f"{user_data}_value_{param_name}",
                )
                dpg.add_input_intx(
                    size=3,
                    label=param_name,
                    max_value=1,
                    min_value=0,
                    tag=f"{user_data}_varycombo_{param_name}",
                    show=False,
                )


def go_callback():
    # compose Situation Struct from the window contents:
    sitch = parse_from_window_settings()
    host: Host = dpg.get_item_user_data("host_dummy")
    slvr: PayoffSolver = dpg.get_item_user_data("solver_dummy")
    input_sets = slvr.compose_sims(
        params_structs=dpg.get_item_user_data("win_actions"),
        situation=sitch,
        p1_base_action=dpg.get_value("p1_base_action_choice"),
        p2_base_action=dpg.get_value("p2_base_action_choice"),
    )
    slvr.host.situation_setup(sitch)
    slvr.host.save_savestate()
    # ^ surely this can go in situation_setup someday.

    dpg.show_item("win_progress")
    slvr.results = slvr.run_sims(
        input_sets,
        lambda x: dpg.set_value("progress_text", x),
        lambda x: dpg.set_value("progress_bar", x),
    )
    slvr.host.console.stop()
    dpg.hide_item("win_progress")
    dpg.configure_item("win_setup", collapsed=True)
    dpg.show_item("win_res")

    # Configure which axes to show and which to collapse-to-slider.
    solver_axes = slvr.axes
    # Just pick the first two plot axes...
    # TODO: account for when there is only ONE axis!!
    ax0_init: ParamAxis = solver_axes[0]
    dpg.set_item_user_data("paramaxis_x", ax0_init)
    if len(solver_axes) == 1:
        ax1_init = ParamAxis("", "", [0])
    else:
        ax1_init: ParamAxis = solver_axes[1]
    dpg.set_item_user_data("paramaxis_y", ax1_init)
    remaining_axes: list[ParamAxis] = solver_axes[2:]
    dpg.set_item_user_data("paramaxis_rem", remaining_axes)
    make_axis_sliders()
    display_results()


def hide_actions_and_lock_variations():
    dpg.hide_item("win_actions")
    """
    wip here: commit the sets of actions to p1_set_action_name and 
    p2_set_action_vary_count
    """
    dpg.set_value("p1_set_action_name", dpg.get_value("p1_base_action_choice"))
    dpg.set_value("p2_set_action_name", dpg.get_value("p2_base_action_choice"))
    dpg.set_value("p1_set_action_vary_count", 1)
    dpg.set_value("p2_set_action_vary_count", 1)

    variations_store = {"p1": [], "p2": []}
    constants_store = {"p1": {}, "p2": {}}

    for pxx in ["p1", "p2"]:
        for row in dpg.get_item_children(f"{pxx}act_dynamicgroup", 1):
            row_widgets = dpg.get_item_children(row, 1)
            for widget in row_widgets:
                if "checkbox" in dpg.get_item_alias(widget):
                    is_varying = dpg.get_value(widget)
                    break
            if is_varying:
                for widget in row_widgets:
                    # TODO: ***this only works for the integer flavour rn.
                    if "vary" in dpg.get_item_alias(widget):
                        varyvals = dpg.get_value(widget)
                        thisvar = (
                            dpg.get_item_label(widget),
                            [r for r in range(varyvals[0], varyvals[1] + 1)],
                        )
                        variations_store[pxx].append(thisvar)

                prev_count = int(dpg.get_value(f"{pxx}_set_action_vary_count"))
                vary_range = (varyvals[1] + 1) - varyvals[0]
                dpg.set_value(f"{pxx}_set_action_vary_count", prev_count * vary_range)
            else:
                for widget in row_widgets:
                    if "value" in dpg.get_item_alias(widget):
                        constants_store[pxx][dpg.get_item_label(widget)] = (
                            dpg.get_value(widget)
                        )
    dpg.set_item_user_data("win_actions", (variations_store, constants_store))


def swap_x(dispatcher, unused1, unused2):
    rem_axes_list: list[ParamAxis] = dpg.get_item_user_data("paramaxis_rem")
    par = dpg.get_item_parent(dispatcher)
    for ch in dpg.get_item_children(par, 1):
        if "_" in dpg.get_item_label(ch):  # stupid
            param_data = [
                r
                for r in rem_axes_list
                if f"{r.player}_{r.param_name}" == dpg.get_item_label(ch)
            ][0]
            break

    last_x = dpg.get_item_user_data("paramaxis_x")
    rem_axes_list.remove(param_data)
    rem_axes_list.append(last_x)
    dpg.set_item_user_data("paramaxis_rem", rem_axes_list)
    dpg.set_item_user_data("paramaxis_x", param_data)

    make_axis_sliders()
    display_results()


def swap_y(dispatcher, unused1, unused2):
    rem_axes_list: list[ParamAxis] = dpg.get_item_user_data("paramaxis_rem")
    par = dpg.get_item_parent(dispatcher)
    for ch in dpg.get_item_children(par, 1):
        if "_" in dpg.get_item_label(ch):  # stupid
            param_data = [
                r
                for r in rem_axes_list
                if f"{r.player}_{r.param_name}" == dpg.get_item_label(ch)
            ][0]
            break

    last_y = dpg.get_item_user_data("paramaxis_y")
    rem_axes_list.remove(param_data)
    rem_axes_list.append(last_y)
    dpg.set_item_user_data("paramaxis_rem", rem_axes_list)
    dpg.set_item_user_data("paramaxis_y", param_data)

    make_axis_sliders()
    display_results()


def make_axis_sliders():
    dpg.delete_item("sliders_dyngroup", children_only=True)
    for ax in dpg.get_item_user_data("paramaxis_rem"):
        with dpg.group(horizontal=True, parent="sliders_dyngroup"):
            dpg.add_button(label="swap X", width=65, callback=swap_x)
            dpg.add_button(label="swap Y", width=65, callback=swap_y)
            dpg.add_slider_int(
                min_value=min(ax.values),
                max_value=max(ax.values),
                default_value=min(ax.values),
                label=f"{ax.player}_{ax.param_name}",
                callback=display_results,
                width=170,
            )


def display_results():
    """
    Set the currently-selected results slice onto the axes.
    """
    solver: PayoffSolver = dpg.get_item_user_data("solver_dummy")
    x_par: ParamAxis = dpg.get_item_user_data("paramaxis_x")
    y_par: ParamAxis = dpg.get_item_user_data("paramaxis_y")
    axis_values = {}
    for widg_grp in dpg.get_item_children("sliders_dyngroup", 1):
        for widg in dpg.get_item_children(widg_grp, 1):
            if "_" in dpg.get_item_label(widg):
                axis_values[dpg.get_item_label(widg)] = dpg.get_value(widg)

    if not y_par.param_name:
        # 1D slice! results_slice cannot elegantly support it...
        slice_ = [solver.results[(i,)] for i in iter(x_par)]
    else:
        slice_ = solver.results_slice(
            x_par.param_name,
            y_par.param_name,
            **axis_values,
        )
    OUTCOME_MAPPING = {"P1 win": 0.0, "P2 win": 1.0, "Whiff": 0.4, "Trade": 0.6}
    outcomes_numeric = [OUTCOME_MAPPING[v[0]] for v in slice_]

    dpg.configure_item(
        "plt_series",
        cols=len(x_par),
        rows=len(y_par),
        x=outcomes_numeric,
    )
    dpg.set_item_user_data("plt_series", slice_)
    dpg.set_item_user_data("plt_xdata_container", outcomes_numeric)

    autoticks_x = np.arange(0, 1, 0.5 / (len(x_par)))[1::2]
    tickmap_x = tuple((str(k), v) for k, v in zip(x_par.values, autoticks_x))
    dpg.set_axis_ticks("plt_xaxis", label_pairs=tickmap_x)
    dpg.configure_item("plt_xaxis", label=f"{x_par.player} {x_par.param_name}")
    dpg.set_item_user_data("plt_xaxis", tickmap_x)
    autoticks_y = np.arange(0, 1, 0.5 / (len(y_par)))[1::2]
    tickmap_y = tuple((str(k), v) for k, v in zip(y_par.values, autoticks_y))
    dpg.set_axis_ticks("plt_yaxis", label_pairs=tickmap_y)
    dpg.configure_item("plt_yaxis", label=f"{y_par.player} {y_par.param_name}")
    dpg.set_item_user_data("plt_yaxis", tickmap_y)


def mouseover_plot_react(mouse_coords):
    sliced_results = dpg.get_item_user_data("plt_series")
    plt_x = np.array([xi[1] for xi in dpg.get_item_user_data("plt_xaxis")])
    bound_x = plt_x - plt_x[0]
    plt_y = np.array([yi[1] for yi in dpg.get_item_user_data("plt_yaxis")])
    bound_y = plt_y - plt_y[0]
    sel_x = np.argmax(bound_x > mouse_coords[0]) - 1
    sel_y = np.argmax(bound_y > mouse_coords[1]) - 1

    # unshaped = dpg.get_value("plt_series")[0]
    unshaped = dpg.get_item_user_data("plt_xdata_container")
    shaped = np.reshape(unshaped, (len(plt_x), len(plt_y)))
    # dorky ass sentinel value approach. no judgy
    shaped[sel_x, -sel_y - 1] = 0.27
    dpg.configure_item("plt_series", x=shaped.flatten().tolist())
    # its getting bad. lol
    hover_ind = np.argmax(((shaped * 10) - 0.7) % 1 < 1e-8)

    dpg.set_value("tooltext", sliced_results[hover_ind][0])
    dpg.set_value("resultsprint", "this label under construction.")
    dpg.set_item_user_data("resultsprint", sliced_results[hover_ind])
    # REMEMBER: this ^ is what is used to decide WHICH REPLAY TO SHOW


def range_check(sender, unused1, unused2):
    ...
    print(f"triggered range correction for {sender}")
