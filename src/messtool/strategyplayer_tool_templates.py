import dearpygui.dearpygui as dpg
import messtool.strategyplayer_tool_callbacks as cbx


def trigger_template(parent):
    with dpg.collapsing_header(label="[placeholder]",
                               parent=parent,
                               indent=20,
                               default_open=True) as H1:
        header_id = str(H1)

        with dpg.group(horizontal=True):
            dpg.add_combo(
                    ["TimeTrigger", "DistanceTrigger", "ActionTrigger"],
                    label="Trigger Type",
                    callback=cbx.callback_trigger_type_select
                    )
            dpg.add_button(label=" × ", callback=cbx.callback_delete_trigger)
        with dpg.group(show=False, tag="timegroup_"+header_id):
            dpg.add_input_int(label="time value")
        with dpg.group(show=False, tag="distgroup_"+header_id):
            dpg.add_input_int(label="distance value")
        with dpg.group(show=False, tag="actiongroup_"+header_id):
            dpg.add_input_int(label="frame value")
    return H1
