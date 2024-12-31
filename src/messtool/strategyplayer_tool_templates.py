import dearpygui.dearpygui as dpg


def trigger_template(GuiController, label, parent):
    with dpg.collapsing_header(label=label,
                               parent=parent,
                               indent=20,
                               default_open=True) as H1:
        header_id = str(H1)

        with dpg.group(horizontal=True):
            dpg.add_combo(
                    ["TimeTrigger", "DistanceTrigger", "ActionTrigger"],
                    label="Trigger Type",
                    callback=GuiController.trigger_type_select
                    )
            dpg.add_spacer(width=30)
            dpg.add_button(label="×",
                           width=30,
                           height=30,
                           callback=GuiController.delete_trigger)
        with dpg.group(show=False, tag="timegroup_"+header_id):
            dpg.add_input_int(label="time value (frames)",
                              callback=GuiController.pull_values)
        with dpg.group(show=False, tag="distgroup_"+header_id):
            dpg.add_input_int(label="distance value",
                              callback=GuiController.pull_values)
        with dpg.group(show=False, tag="actiongroup_"+header_id):
            dpg.add_input_int(label="frame value",
                              callback=GuiController.pull_values)
        with dpg.group(show=False, tag="responseselect_"+header_id):
            dpg.add_combo(
                ["placeholder."]
            )
    return H1
