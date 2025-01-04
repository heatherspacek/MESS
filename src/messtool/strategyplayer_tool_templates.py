import dearpygui.dearpygui as dpg
from messlib.classes_abstract import (Trigger, TimeTrigger, DistanceTrigger,
                                      ActionTrigger)


def trigger_template(GuiController, label, parent, trigger):
    # based on the type of trigger, configure the template differently.
    with dpg.collapsing_header(label=label,
                               parent=parent,
                               indent=20,
                               default_open=True) as H1:

        with dpg.group(horizontal=True):
            dpg.add_combo(
                    ["TimeTrigger", "DistanceTrigger", "ActionTrigger"],
                    label="Trigger Type",
                    callback=GuiController.trigger_type_select,
                    user_data=trigger
                    )
            if type(trigger) is Trigger:
                dpg.set_value(dpg.last_item(), "")
            else:
                dpg.set_value(dpg.last_item(), type(trigger))
            dpg.add_spacer(width=30)
            dpg.add_button(label="×",
                           width=30,
                           height=30,
                           callback=GuiController.delete_trigger,
                           user_data=trigger
                           )
        if type(trigger) is TimeTrigger:
            dpg.add_input_int(
                label="time value (frames)",
                callback=lambda s, a, u: setattr(u, "time_value", a),
                user_data=trigger
                )
            dpg.set_value(dpg.last_item(), trigger.time_value)
        if type(trigger) is DistanceTrigger:
            dpg.add_input_int(
                label="distance value",
                callback=lambda s, a, u: setattr(u, "distance_value", a),
                user_data=trigger
                )
            dpg.set_value(dpg.last_item(), trigger.distance_value)
        if type(trigger) is ActionTrigger:
            dpg.add_input_int(
                label="frame value",
                callback=lambda s, a, u: setattr(u, "frame_value", a),
                user_data=trigger
                )
            dpg.set_value(dpg.last_item(), trigger.frame_value)
        if type(trigger) is not Trigger:
            dpg.add_combo(
                ["placeholder."]
            )
    return H1
