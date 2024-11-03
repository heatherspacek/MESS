import dearpygui.dearpygui as dpg
import ctypes  # for Windows high-dpi text rendering "fuzziness" fix
import melee
import os  # for os.path.join
# --
import strategyplayer_tool_callbacks as cbx
from MESSaux import ConsoleInterface, StrategyPlayer


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
        dpg.add_separator()
        dpg.add_checkbox(label="Don't ask me next time")
        with dpg.group(horizontal=True):
            dpg.add_button(label="OK", width=75,
                           callback=lambda: dpg.configure_item(
                               "modal_misc", show=False))
            dpg.add_button(label="Cancel", width=75,
                           callback=lambda: dpg.configure_item(
                               "modal_misc", show=False))

    with dpg.window(label="START HERE", no_close=True) as top_level_wnd:
        # give out the reference to the top level window
        dpg.set_item_user_data("strategy_fileselect", top_level_wnd)

        dpg.set_item_width(top_level_wnd, 600)
        dpg.set_item_height(top_level_wnd, 600)
        with dpg.tab_bar():
            with dpg.tab(label=tab1str) as tab1:  # 1P 1CPU mode
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
                    with dpg.tab(label=tab1_1str) as tab1_1:  # SP Setup
                        strategy_setup_section()

                    with dpg.tab(label=tab1_2str) as tab1_2:  # Situation setup
                        pass

                dpg.add_button(label="LAUNCH MELEE (test)",
                               callback=Interface.setup)
            # -----
            with dpg.tab(label=tab2str) as tab2:
                dpg.add_button(label="\nTest two\nStrategyPlayers\n")
            #
        dpg.add_text("=====")
        dpg.add_button(label="Export Strategy",
                       callback=cbx.callback_strategy_export)

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
        # bold_font = dpg.add_font(os.path.join(
        #     "res", "NotoSans-Bold.ttf"), 20)

    dpg.bind_font(default_font)

    import dearpygui.demo as demo
    demo.show_demo()

    if os.name == 'nt':
        # Windows-specific "high-DPI" bugfix for blurry text.
        # before showing the viewport/calling `show_viewport`:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)

    dpg.show_viewport()


def strategy_setup_section():
    dpg.add_combo(list(melee.enums.Character), label="Chr")
    dpg.add_combo([2, 3, 4], label="SP controller port")
    dpg.add_separator()
    with dpg.collapsing_header(label="Triggers", default_open=True) as head1:
        dpg.add_button(label="(+) Add Trigger",
                       callback=cbx.callback_add_trigger,
                       user_data=head1)
    with dpg.collapsing_header(label="Responses", default_open=True) as head2:
        dpg.add_button(label="(+) Add Response",
                       callback=cbx.callback_add_trigger,  # change this later
                       user_data=head2)
