import dearpygui.dearpygui as dpg
import ctypes  # for Windows high-dpi text rendering "fuzziness" fix
import melee
import os  # for os.path.join and os.listdir

# --
import messtool.strategyplayer_tool_classes as tool


def layout_setup(GuiController: tool.GuiController):
    dpg.create_context()
    load_textures()
    window_themes()
    window_fonts()
    hidden_windows_setup()
    # Window 1- strategy editor
    strategy_editor_window(GuiController)
    # Window 2- situation editor
    situation_editor_window(GuiController)
    # Window 3- game setup
    game_setup_window(GuiController)

    dpg.create_viewport(title="MESS", width=1320, height=650)
    dpg.setup_dearpygui()

    if os.name == "nt":
        # Windows-specific "high-DPI" bugfix for blurry text.
        # before showing the viewport/calling `show_viewport`:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)

    dpg.show_viewport()


def strategy_editor_window(GuiController: tool.GuiController):
    with dpg.window(
        label="MESS Strategy Editor",
        tag="editorwnd",
        width=500,
        height=550,
        min_size=(500, 550),
    ):
        GuiController.strat_name_ref = dpg.add_input_text(label="Strategy Name")
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
                    user_data="triggers"
                )
                dpg.add_button(
                    label="Expand All", width=125, callback=GuiController.collapse_all
                )
            with dpg.group() as triggers_group:
                # Register this (empty) group with the Controller.
                GuiController.triggers_group_ref = triggers_group

        with dpg.collapsing_header(label="Responses", default_open=True) as head2:
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
                    user_data="responses"
                )
                dpg.add_button(
                    label="Expand All", width=150, callback=GuiController.expand_all
                )
            with dpg.group() as responses_group:
                # Register this group with the Controller.
                GuiController.responses_group_ref = responses_group


def situation_editor_window(GuiController: tool.GuiController):
    with dpg.window(
        label="Situation Setup",
        tag="situationwnd",
        width=500,
        height=550,
        min_size=(500, 550),
        pos=(800, 0),
        no_move=True
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
                dpg.add_checkbox(label="P1 is grabbed",
                                 tag="constraint_p1grab", default_value=True)
                dpg.add_checkbox(label="P2 is grabbed",
                                 tag="constraint_p2grab", default_value=True)
            with dpg.group(horizontal=True):
                dpg.add_checkbox(label="P1 is knocked down",
                                 tag="constraint_p1knock", default_value=True)
                dpg.add_checkbox(label="P2 is knocked down",
                                 tag="constraint_p2knock", default_value=True)
            with dpg.group():
                dpg.add_checkbox(label="Nothing has happened for N seconds",
                                 tag="constraint_idle", default_value=True)
                dpg.add_input_float(label="seconds", tag="constraint_idle_seconds",
                                  default_value=4)


def mouseclick_callback(sender, app_data):
    dpg.set_value("mouseclick_test", f"Mouse Button ID: {app_data}")


def mousemove_callback(sender, app_data):
    dpg.set_value("mousecoords", f"Mouse Position: {app_data}")


def change_stage(sender, value, user_data):

    match value:
        case "Battlefield": stage_texture_filename = "stage_bf"
        case "Final Destination": stage_texture_filename = "stage_fd"
        case "Yoshi's Story": stage_texture_filename = "stage_ys"
        case "Fountain of Dreams": stage_texture_filename = "stage_fo"
        case "Dream Land": stage_texture_filename = "stage_dl"
        case "Pokemon Stadium": stage_texture_filename = "stage_ps"
    dpg.configure_item("stage_image", texture_tag=stage_texture_filename)


def game_setup_window(GuiController: tool.GuiController):
    with dpg.window(
        label="---",
        tag="gamewnd",
        width=300,
        height=400,
        min_size=(300, 400),
        pos=(500, 25),
    ):
        dpg.add_text(
            """Welcome to MESS!
            To get started, load a strategy or situation from file, 
            or start editing your own!"""
        )
        dpg.add_separator()
        dpg.add_image("zelda")

        with dpg.group(horizontal=True):
            with dpg.group():
                # P1
                dpg.add_image("placeholder")
                dpg.add_combo(
                    ["strategyplayer", "human input"],
                    default_value="strategyplayer",
                    width=135,
                )

                dpg.add_text("[No strategy loaded.]", tag="status_p1")
            with dpg.group():
                # P2
                dpg.add_image("placeholder")
                dpg.add_combo(
                    ["strategyplayer"], default_value="strategyplayer", width=135
                )

                dpg.add_text("[No strategy loaded.]", tag="status_p2")

        # Make this button say "start analysis" when in SP vs SP mode.
        dpg.add_button(label="Start game", tag="startbutton")


def hidden_windows_setup():
    dpg.add_file_dialog(
        directory_selector=False,
        show=False,
        tag="strategy_fileselect",
        file_count=1,
        width=500,
        height=400,
    )
    dpg.add_file_extension(".yaml", parent="strategy_fileselect")
    dpg.add_file_dialog(
        directory_selector=False,
        show=False,
        callback=None,
        tag="situation_fileselect",
        cancel_callback=None,
        width=500,
        height=400,
    )
    with dpg.window(
        label="[Placeholder Title]",
        modal=True,
        show=False,
        tag="modal_misc",
        no_title_bar=True,
    ):
        dpg.add_text("File load failed.", tag="model_misc_text")
        dpg.add_checkbox(label="Don't ask me next time")
        with dpg.group(horizontal=True):
            dpg.add_button(
                label="OK",
                width=75,
                callback=lambda: dpg.configure_item("modal_misc", show=False),
            )
            dpg.add_button(
                label="Cancel",
                width=75,
                callback=lambda: dpg.configure_item("modal_misc", show=False),
            )


def window_themes():
    with dpg.theme(tag="theme1"):
        with dpg.theme_component(dpg.mvCollapsingHeader):
            dpg.add_theme_color(dpg.mvThemeCol_Header, [98, 48, 67])
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, [119, 61, 84])
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, [119, 44, 74])
            dpg.add_theme_color(dpg.mvThemeCol_Text, [211, 211, 211])

    with dpg.theme(tag="theme2"):
        with dpg.theme_component(dpg.mvCollapsingHeader):
            dpg.add_theme_color(dpg.mvThemeCol_Header, [28, 48, 97])
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, [48, 61, 184])
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, [48, 44, 174])
            dpg.add_theme_color(dpg.mvThemeCol_Text, [211, 211, 211])


def window_fonts():
    with dpg.font_registry():
        # first argument ids the path to the .ttf or .otf file
        # TODO: this is fragile!!! only works right now because VS Code sets
        # a specific cwd. Look more later!
        dpg.add_font(
            os.path.join("res", "NotoSans-Regular.ttf"), 20, tag="default_font"
        )
        dpg.add_font(os.path.join("res", "NotoSans-Bold.ttf"), 20, tag="bold_font")

    dpg.bind_font("default_font")


def load_textures():
    for png in os.listdir(os.path.join("res", "stock_icons")):
        with dpg.texture_registry():
            (w, h, c, d) = dpg.load_image(os.path.join("res", "stock_icons", png))
            dpg.add_static_texture(
                width=w, height=h, default_value=d, tag=png.split(".")[0]
            )

    for png in os.listdir(os.path.join("res", "stages")):
        with dpg.texture_registry():
            (w, h, c, d) = dpg.load_image(os.path.join("res", "stages", png))
            dpg.add_static_texture(
                width=w, height=h, default_value=d, tag="stage_" + png.split(".")[0]
            )
