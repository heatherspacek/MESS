import dearpygui.dearpygui as dpg
import strategyplayer_tool_callbacks as cbx


def trigger_template(parent, trigger):
    with dpg.collapsing_header(label="Trigger N", user_data=trigger,
                               parent=parent, indent=20) as H1:
        header_id = str(H1)

        def trigger_type_select_callback(sender, value, user_data):
            # Based on box selection, change the state of the template, and
            # also
            sender_header_id = str(
                    dpg.get_item_parent(dpg.get_item_parent(sender))
                )

            if value == "TimeTrigger":
                dpg.configure_item("timegroup_"+sender_header_id, show=True)
                dpg.configure_item("distgroup_"+sender_header_id, show=False)
                dpg.configure_item("actiongroup_"+sender_header_id, show=False)
            elif value == "DistanceTrigger":
                dpg.configure_item("timegroup_"+sender_header_id, show=False)
                dpg.configure_item("distgroup_"+sender_header_id, show=True)
                dpg.configure_item("actiongroup_"+sender_header_id, show=False)
            elif value == "ActionTrigger":
                dpg.configure_item("timegroup_"+sender_header_id, show=False)
                dpg.configure_item("distgroup_"+sender_header_id, show=False)
                dpg.configure_item("actiongroup_"+sender_header_id, show=True)
            else:
                pass

        with dpg.group(horizontal=True):
            dpg.add_combo(
                    ["TimeTrigger", "DistanceTrigger", "ActionTrigger"],
                    label="Trigger Type",
                    callback=trigger_type_select_callback,
                    user_data=()
                    )
            dpg.add_button(label=" × ", callback=cbx.callback_delete_trigger,
                           user_data=trigger)
        with dpg.group(show=False, tag="timegroup_"+header_id):
            dpg.add_input_int(label="time value")
        with dpg.group(show=False, tag="distgroup_"+header_id):
            dpg.add_input_int(label="distance value")
        with dpg.group(show=False, tag="actiongroup_"+header_id):
            dpg.add_input_int(label="frame value")

