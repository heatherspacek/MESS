import dearpygui.dearpygui as dpg
import strategyplayer_tool_callbacks as cbx


def trigger_template(parent, trigger):
    with dpg.collapsing_header(label="Trigger N", user_data=trigger,
                               parent=parent, indent=20):
        def trigger_type_select_callback(sender, value, user_data):
            # Based on box selection, change the state of the template, and
            # also

            if value == "TimeTrigger":
                dpg.configure_item("_timegroup", show=True)
                dpg.configure_item("_distgroup", show=False)
                dpg.configure_item("_actiongroup", show=False)
            elif value == "DistanceTrigger":
                dpg.configure_item("_timegroup", show=False)
                dpg.configure_item("_distgroup", show=True)
                dpg.configure_item("_actiongroup", show=False)
            elif value == "ActionTrigger":
                dpg.configure_item("_timegroup", show=False)
                dpg.configure_item("_distgroup", show=False)
                dpg.configure_item("_actiongroup", show=True)
            else:
                pass

        with dpg.group(horizontal=True):
            dpg.add_combo(
                    ["TimeTrigger", "DistanceTrigger", "ActionTrigger"],
                    label="Trigger Type",
                    callback=trigger_type_select_callback
                    )
            dpg.add_button(label=" × ", callback=cbx.callback_delete_trigger,
                           user_data=trigger)
        with dpg.group(show=False, tag="_timegroup"):
            dpg.add_input_int(label="time value")
        with dpg.group(show=False, tag="_distgroup"):
            dpg.add_input_int(label="distance value")
        with dpg.group(show=False, tag="_actiongroup"):
            dpg.add_input_int(label="frame value")

