import dearpygui.dearpygui as dpg
import ctypes  # for Windows high-dpi text rendering "fuzziness" fix
import melee
import os  # for os.path.join
import pdb
# --
import messtool.strategyplayer_tool_classes as tool


def layout_setup(GuiController: tool.GuiController):
    dpg.create_context()
    window_themes()
    window_fonts()
    hidden_windows_setup()
    main_layout(GuiController)

    dpg.create_viewport(
        title="MESS Strategy Editor",
        width=700, height=600
        )
    dpg.setup_dearpygui()

    if os.name == 'nt':
        # Windows-specific "high-DPI" bugfix for blurry text.
        # before showing the viewport/calling `show_viewport`:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)

    dpg.show_viewport()


def main_layout(GuiController: tool.GuiController):

    tab1str = "[1P, 1CPU] Play against a StrategyPlayer"
    tab2str = "[0P, 2CPU] Init two StrategyPlayers"
    tab1_1str = "Strategy Setup"
    tab1_2str = "Situation Setup"

    with dpg.window(label="MESS Strategy Editor", tag="topwnd"):
        with dpg.group(horizontal=True):
            dpg.add_loading_indicator(circle_count=6, radius=2, height=48)
            dpg.add_text("Welcome to MESS! Status messages will show up here.")
            dpg.add_button(label="debug console [global]",
                           callback=lambda: pdb.set_trace())
        with dpg.tab_bar():
            with dpg.tab(label=tab1str):  # 1P 1CPU mode
                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="Import Strategy...",
                        callback=GuiController.load_strategy_from_file
                        )
                    dpg.add_button(
                        label="Import Situation...",
                        callback=lambda: dpg.show_item("situation_fileselect")
                        )

                with dpg.tab_bar():
                    with dpg.tab(label=tab1_1str):  # SP Setup
                        strategy_setup_section(GuiController)

                    with dpg.tab(label=tab1_2str):  # Situation setup
                        pass

                dpg.add_button(label="LAUNCH MELEE (test)",
                               callback=lambda: GuiController.setup_and_launch)
            # -----
            with dpg.tab(label=tab2str):
                dpg.add_button(label="\nTest two\nStrategyPlayers\n")
            #
        dpg.add_text("=====")
        dpg.add_button(label="Export Strategy",
                       callback=GuiController.save_strategy_to_file,
                       tag="importantbutton",
                       )
        dpg.add_button(label="connect p2",
                       callback=(),
                       tag="testingbutton",
                       )

    dpg.set_primary_window("topwnd", True)


def strategy_setup_section(GuiController: tool.GuiController):
    GuiController.strat_name_ref = dpg.add_input_text(label="Strategy Name")
    GuiController.character_combo_ref = dpg.add_combo(
        list(melee.enums.Character), label="Character")

    dpg.add_separator()
    with dpg.collapsing_header(label="Triggers", default_open=True) as H_T:
        dpg.bind_item_theme(H_T, "theme1")
        with dpg.group(horizontal=True, horizontal_spacing=-1):
            dpg.add_button(label="(+) Add Trigger",
                           height=35,
                           width=150,
                           callback=GuiController.add_trigger)
            dpg.add_spacer(width=150)
            dpg.add_button(label="Collapse All",
                           width=150,
                           callback=GuiController.collapse_all)
            dpg.add_button(label="Expand All",
                           width=150,
                           callback=GuiController.collapse_all)
        with dpg.group() as triggers_group:
            # Register this (empty) group with the Controller.
            GuiController.triggers_group_ref = triggers_group

    with dpg.collapsing_header(label="Responses", default_open=True) as head2:
        dpg.bind_item_theme(head2, "theme2")
        with dpg.group(horizontal=True, horizontal_spacing=-1):
            dpg.add_button(label="(+) Add Response",
                           height=35,
                           width=150,
                           callback=GuiController.add_response)
            dpg.add_spacer(width=150)
            dpg.add_button(label="Collapse All",
                           width=150,
                           callback=GuiController.collapse_all)
            dpg.add_button(label="Expand All",
                           width=150,
                           callback=GuiController.collapse_all)
        with dpg.group() as responses_group:
            # Register this group with the Controller.
            GuiController.responses_group_ref = responses_group


def hidden_windows_setup():
    dpg.add_file_dialog(
        directory_selector=False,
        show=False,
        tag="strategy_fileselect",
        file_count=1,
        width=500, height=400
        )
    dpg.add_file_extension(".yaml", parent="strategy_fileselect")
    dpg.add_file_dialog(
        directory_selector=False,
        show=False,
        callback=None,
        tag="situation_fileselect",
        cancel_callback=None,
        width=500, height=400
        )
    with dpg.window(label="[Placeholder Title]",
                    modal=True,
                    show=False,
                    tag="modal_misc",
                    no_title_bar=True):
        dpg.add_text(
            "File load failed.",
            tag="model_misc_text"
            )
        dpg.add_checkbox(label="Don't ask me next time")
        with dpg.group(horizontal=True):
            dpg.add_button(label="OK", width=75,
                           callback=lambda: dpg.configure_item(
                               "modal_misc", show=False))
            dpg.add_button(label="Cancel", width=75,
                           callback=lambda: dpg.configure_item(
                               "modal_misc", show=False))


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
        dpg.add_font(os.path.join("res", "NotoSans-Regular.ttf"),
                     20, tag="default_font")
        dpg.add_font(os.path.join("res", "NotoSans-Bold.ttf"),
                     20, tag="bold_font")

    dpg.bind_font("default_font")
