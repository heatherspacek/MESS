import dearpygui.dearpygui as dpg
import ctypes  # for Windows high-dpi text rendering "fuzziness" fix
import melee
import os  # for os.path.join
import pdb
# --
import strategyplayer_tool_callbacks as cbx
import strategyplayer_tool_templates as tp8
from MESSaux import ConsoleInterface, StrategyPlayer
from MESSactions import Actions, Inputs


def window_layout(Interface: ConsoleInterface,
                  Player1: StrategyPlayer,
                  Player2: StrategyPlayer):
    dpg.create_context()

    # =====
    # the "start panel"...
    tab1str = "[1P, 1CPU] Play against a StrategyPlayer"
    tab2str = "[0P, 2CPU] Init two StrategyPlayers"
    tab1_1str = "Strategy Setup"
    tab1_2str = "Situation Setup"

    # =====
    # themes. (Defined below)
    window_themes()

    # =====
    # not-shown-until-needed windows.
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
        callback=cbx.callback_situation_load_ok,
        tag="situation_fileselect",
        cancel_callback=cbx.callback_situation_load_cancel,
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
        dpg.add_separator(tag="holder0", user_data=Interface)
        dpg.add_separator(tag="holder1", user_data=Player1)
        dpg.add_separator(tag="holder2", user_data=Player2)
        dpg.add_checkbox(label="Don't ask me next time")
        with dpg.group(horizontal=True):
            dpg.add_button(label="OK", width=75,
                           callback=lambda: dpg.configure_item(
                               "modal_misc", show=False))
            dpg.add_button(label="Cancel", width=75,
                           callback=lambda: dpg.configure_item(
                               "modal_misc", show=False))

    """ Top-level strategy composition window. ===== """

    with dpg.window(label="START HERE", no_close=True) as top_level_wnd:
        dpg.set_item_width(top_level_wnd, 600)
        dpg.set_item_height(top_level_wnd, 600)
        with dpg.group(horizontal=True):
            dpg.add_loading_indicator(circle_count=6, radius=1, height=48)
            dpg.add_text("Welcome to MESS! Status messages will show up here.")
            dpg.add_button(label="debug console",
                           callback=lambda: pdb.set_trace())
        with dpg.tab_bar():
            with dpg.tab(label=tab1str):  # 1P 1CPU mode
                with dpg.group(horizontal=True):
                    dpg.add_button(
                        label="Import Strategy...",
                        callback=cbx.callback_strategy_import
                        )
                    dpg.add_button(
                        label="Import Situation...",
                        callback=lambda: dpg.show_item("situation_fileselect")
                        )

                with dpg.tab_bar():
                    with dpg.tab(label=tab1_1str):  # SP Setup
                        strategy_setup_section(Player2)

                    with dpg.tab(label=tab1_2str):  # Situation setup
                        pass

                dpg.add_button(label="LAUNCH MELEE (test)",
                               callback=Interface.setup_oneplayer)
            # -----
            with dpg.tab(label=tab2str):
                dpg.add_button(label="\nTest two\nStrategyPlayers\n")
            #
        dpg.add_text("=====")
        dpg.add_button(label="Export Strategy",
                       callback=cbx.callback_strategy_export,
                       tag="importantbutton",
                       user_data=Player1)
        dpg.add_button(label="connect p2",
                       callback=cbx.callback_TEST,
                       tag="testingbutton",
                       user_data=Player2)

    # Viewport creation (the window)
    dpg.create_viewport(
        title='StrategyPlayer Invocation Tool',
        width=700, height=600
        )
    dpg.setup_dearpygui()

    # add a font registry
    with dpg.font_registry():
        # first argument ids the path to the .ttf or .otf file
        default_font = dpg.add_font(os.path.join(
            "res", "NotoSans-Regular.ttf"), 20)
        bold_font = dpg.add_font(os.path.join(
            "res", "NotoSans-Bold.ttf"), 20)

    dpg.bind_font(default_font)

    if os.name == 'nt':
        # Windows-specific "high-DPI" bugfix for blurry text.
        # before showing the viewport/calling `show_viewport`:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)

    dpg.show_viewport()


def strategy_setup_section(Player2: StrategyPlayer):
    dpg.add_input_text(label="Strategy Name", default_value="New Strategy 1")
    dpg.add_combo(list(melee.enums.Character), label="Chr")
    # dpg.add_combo([2, 3, 4], label="SP controller port")
    dpg.add_separator()
    with dpg.collapsing_header(label="Triggers", default_open=True) as H_T:
        dpg.bind_item_theme(H_T, "theme1")
        dpg.add_button(label="(+) Add Trigger",
                       callback=cbx.callback_add_trigger,
                       user_data=Player2)

    with dpg.collapsing_header(label="Responses", default_open=True) as head2:
        dpg.add_button(label="(+) Add Response",
                       callback=cbx.callback_add_trigger,  # change this later
                       user_data=head2)


def window_themes():
    with dpg.theme(tag="theme1"):
        with dpg.theme_component(dpg.mvCollapsingHeader):
            dpg.add_theme_color(dpg.mvThemeCol_Header, [98, 48, 67])
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, [119, 61, 84])
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, [119, 44, 74])
            dpg.add_theme_color(dpg.mvThemeCol_Text, [211, 211, 211])
