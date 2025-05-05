import dearpygui.dearpygui as dpg
# from messtool.singletons import GuiController


def situation_editor_window():
    with dpg.window(
        label="Situation Setup",
        tag="situationwnd",
        width=500,
        height=550,
        min_size=(500, 550),
        pos=(800, 0),
        no_move=True,
    ):
        with dpg.handler_registry():
            dpg.add_mouse_down_handler(callback=mouseclick_callback)
            dpg.add_mouse_move_handler(callback=mousemove_callback)

        dpg.add_image(texture_tag="stage_bf", tag="stage_image")
        dpg.add_combo(
            [
                "Battlefield",
                "Final Destination",
                "Yoshi's Story",
                "Fountain of Dreams",
                "Dream Land",
                "Pokemon Stadium",
            ],
            default_value="Battlefield",
            label="Stage",
            callback=change_stage,
        )

        dpg.add_text("testing...", tag="mouseclick_test")
        dpg.add_text("", tag="mousecoords")
        # dpg.bind_item_handler_registry("mouseclick_test", "handler")
        # dpg.bind_item_handler_registry("mousecoords", "handler")
        # ^ not needed cuz these are "global registry" things

        #####
        # CONSTRAINTS - When does the "situation" end?
        with dpg.collapsing_header(label="End situation when..."):
            with dpg.group(horizontal=True):
                dpg.add_checkbox(
                    label="P1 is grabbed",
                    tag="constraint_p1grab",
                    default_value=True,
                )
                dpg.add_checkbox(
                    label="P2 is grabbed",
                    tag="constraint_p2grab",
                    default_value=True,
                )
            with dpg.group(horizontal=True):
                dpg.add_checkbox(
                    label="P1 is knocked down",
                    tag="constraint_p1knock",
                    default_value=True,
                )
                dpg.add_checkbox(
                    label="P2 is knocked down",
                    tag="constraint_p2knock",
                    default_value=True,
                )
            with dpg.group():
                dpg.add_checkbox(
                    label="Nothing has happened for N seconds",
                    tag="constraint_idle",
                    default_value=True,
                )
                dpg.add_input_float(
                    label="seconds",
                    tag="constraint_idle_seconds",
                    default_value=4,
                )


def mouseclick_callback(sender, app_data):
    dpg.set_value("mouseclick_test", f"Mouse Button ID: {app_data}")


def mousemove_callback(sender, app_data):
    dpg.set_value("mousecoords", f"Mouse Position: {app_data}")


def change_stage(sender, value, user_data):

    match value:
        case "Battlefield":
            stage_texture_filename = "stage_bf"
        case "Final Destination":
            stage_texture_filename = "stage_fd"
        case "Yoshi's Story":
            stage_texture_filename = "stage_ys"
        case "Fountain of Dreams":
            stage_texture_filename = "stage_fo"
        case "Dream Land":
            stage_texture_filename = "stage_dl"
        case "Pokemon Stadium":
            stage_texture_filename = "stage_ps"
    dpg.configure_item("stage_image", texture_tag=stage_texture_filename)
