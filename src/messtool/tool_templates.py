from __future__ import annotations
import dearpygui.dearpygui as dpg
from messlib.data_structures.classes import (
    Trigger,
    TimeTrigger,
    DistanceTrigger,
    ActionTrigger,
    Response,
)
from messlib.data_structures.move_definitions import Actions  # for list of possible base Actions
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from messtool.tool_classes import GuiController


def trigger_template(
    GuiController: GuiController, label: str, parent: int, trigger: Trigger
):
    # based on the type of trigger, configure the template differently.
    with dpg.collapsing_header(
        label=label, parent=parent, indent=20, default_open=True
    ):

        with dpg.group(horizontal=True):
            dpg.add_combo(
                ["TimeTrigger", "DistanceTrigger", "ActionTrigger"],
                label="Trigger Type",
                callback=GuiController.trigger_type_select,
                user_data=trigger,
                width=300,
            )
            if type(trigger) is Trigger:
                dpg.set_value(dpg.last_item(), "")
            else:
                dpg.set_value(dpg.last_item(), type(trigger))
            dpg.add_spacer(width=30)
            dpg.add_button(
                label="×",
                width=30,
                height=30,
                callback=GuiController.delete_trigger,
                user_data=trigger,
            )

        # ### TIME TRIGGER ####
        if type(trigger) is TimeTrigger:
            dpg.add_input_int(
                label="time value (frames)",
                callback=lambda s, a, u: setattr(u, "time_value", a),
                user_data=trigger,
            )
            dpg.set_value(dpg.last_item(), trigger.time_value)

        # ### DISTANCE TRIGGER ####
        if type(trigger) is DistanceTrigger:
            with dpg.group(horizontal=True):
                dpg.add_combo(
                    ["<", ">"],
                    callback=lambda s, a, u: u.set_comparator(a),
                    user_data=trigger,
                    width=60,
                )
                dpg.set_value(dpg.last_item(), trigger.get_comparator_symbol())

                dpg.add_input_int(
                    label="distance value",
                    callback=lambda s, a, u: setattr(u, "distance_value", a),
                    user_data=trigger,
                )
                dpg.set_value(dpg.last_item(), trigger.distance_value)

        # ### ACTION TRIGGER ####
        if type(trigger) is ActionTrigger:
            dpg.add_input_int(
                label="frame value",
                callback=lambda s, a, u: setattr(u, "frame_value", a),
                user_data=trigger,
            )
            dpg.set_value(dpg.last_item(), trigger.frame_value)

        # ### COMMON ####
        if type(trigger) is not Trigger:
            with dpg.group(horizontal=True):
                dpg.add_checkbox(
                    label="conditional?",
                    callback=lambda s, a, u: setattr(u, "conditional", a),
                    user_data=trigger,
                )
                dpg.set_value(dpg.last_item(), trigger.conditional)
                if trigger.conditional:
                    dpg.add_combo(label="against what condition?", items=["pepis"])
            dpg.add_combo(
                items=GuiController.loaded_strategy.responses,
                label="associated response",
                callback=lambda s, a, u: setattr(u, "associated_response", a),
                user_data=trigger,
            )
            dpg.set_value(dpg.last_item(), trigger.associated_response)


def response_template(
    GuiController: GuiController, label: str, parent: int, response: Response
):
    with dpg.collapsing_header(
        label=label, parent=parent, indent=20, default_open=True
    ):
        # aim options?
        dpg.add_combo(label="base action", items=Actions.all_actions(), width=300)
