import dearpygui.dearpygui as dpg
import melee
from messtool.singletons import GuiController


def strategy_editor_window():
    with dpg.window(
        label="MESS Strategy Editor",
        tag="editorwnd",
        width=500,
        height=550,
        min_size=(500, 550),
    ):
        GuiController.strat_name_ref = dpg.add_input_text(
            label="Strategy Name"
        )
        GuiController.character_combo_ref = dpg.add_combo(
            list(melee.enums.Character), label="Character"
        )

        dpg.add_separator()
        with dpg.collapsing_header(label="Triggers", default_open=True) as H_T:
            dpg.bind_item_theme(H_T, "theme1")
            with dpg.group(horizontal=True, horizontal_spacing=-1):
                dpg.add_button(
                    label="(+) Add Trigger",
                    height=35,
                    width=150,
                    callback=GuiController.add_trigger,
                )
                dpg.add_spacer(width=50)
                dpg.add_button(
                    label="Collapse All",
                    width=125,
                    callback=GuiController.collapse_all,
                    user_data="triggers",
                )
                dpg.add_button(
                    label="Expand All",
                    width=125,
                    callback=GuiController.collapse_all,
                )
            with dpg.group() as triggers_group:
                # Register this (empty) group with the Controller.
                GuiController.triggers_group_ref = triggers_group

        with dpg.collapsing_header(
            label="Responses", default_open=True
        ) as head2:
            dpg.bind_item_theme(head2, "theme2")
            with dpg.group(horizontal=True, horizontal_spacing=-1):
                dpg.add_button(
                    label="(+) Add Response",
                    height=35,
                    width=150,
                    callback=GuiController.add_response,
                )
                dpg.add_spacer(width=50)
                dpg.add_button(
                    label="Collapse All",
                    width=125,
                    callback=GuiController.collapse_all,
                    user_data="responses",
                )
                dpg.add_button(
                    label="Expand All",
                    width=150,
                    callback=GuiController.expand_all,
                )
            with dpg.group() as responses_group:
                # Register this group with the Controller.
                GuiController.responses_group_ref = responses_group
