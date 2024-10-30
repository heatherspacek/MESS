import dearpygui.dearpygui as dpg
import melee
import os  # for os.path.join
import ctypes  # for Windows high-dpi text rendering "fuzziness" fix
from dataclasses import dataclass
# -
import strategyplayer_tool_callbacks as cbx
# -
# from MESSaux import jumpsquat  # not actually useful. placeholder
from MESSabstract import Response, Strategy

# #######look up "blinker" package; do i need this type of inter-object comms?


@dataclass
class GlobalState():
    """
    storage for useful global states"""
    pass


class StrategyPlayer():
    """
    Entity that interfaces with a Strategy, which is just a data-structure.
    """
    loaded_strategy: Strategy = None
    controller: melee.Controller = None
    # --
    current_response: Response = None

    def consult(self):
        pass


class ConsoleInterface():
    """
    object exposing callables to interface with the libmelee `console`.
    """
    running = False
    console = None
    controller1 = None
    controller2 = None
    gamestate = None

    def __init__(self, console: melee.Console):
        self.console = console

    def setup(self):
        self.console.run()
        # self.console.connect()
        print("Connecting to console...")
        if not self.console.connect():
            print("ERROR: Failed to connect to the console.")
            raise RuntimeError
        print("Console connected")
        self.controller1 = melee.Controller(console=self.console, port=1)
        self.controller2 = melee.Controller(console=self.console, port=2)
        self.controller1.connect()
        self.controller2.connect()
        self.running = True

    def step(self):
        if self.running:
            # Trying to ask for a step before setup has occurred can cause
            # unpredictable behaviour.
            self.gamestate = self.console.step()


"""
===============================================================================
app entry point.
===============================================================================
"""


def callback_ok(sender, app_data):
    print('OK was clicked.')
    print("Sender: ", sender)
    print("App Data: ", app_data)


def cancel_callback(sender, app_data):
    print('Cancel was clicked.')
    print("Sender: ", sender)
    print("App Data: ", app_data)


if __name__ == "__main__":

    slippi_playback_path = os.path.join(os.environ["APPDATA"],
                                        "Slippi Launcher", "playback")
    console = melee.Console(path=slippi_playback_path)

    Interface = ConsoleInterface(console)
    Gsm = GlobalState()

    S1 = Strategy()

    Player1 = StrategyPlayer()
    Player1.loaded_strategy = S1

    Player2 = StrategyPlayer()

    dpg.create_context()

    # =====
    # the "start panel"...
    tab1str = "[1P, 1CPU] Play against a StrategyPlayer"
    tab2str = "[0P, 2CPU] Init two StrategyPlayers"
    tab1_1str = "SP Setup"
    tab1_2str = "Situation Setup"

    dpg.add_file_dialog(
        directory_selector=True,
        show=False,
        callback=callback_ok,
        tag="strategy_fileselect",
        cancel_callback=cancel_callback,
        width=500, height=400
        )

    dpg.add_file_dialog(
        directory_selector=True,
        show=False,
        callback=callback_ok,
        tag="situation_fileselect",
        cancel_callback=cancel_callback,
        width=500, height=400
        )

    with dpg.window(label="START HERE", no_close=True) as top_level_wnd:
        dpg.set_item_width(top_level_wnd, 600)
        dpg.set_item_height(top_level_wnd, 600)
        with dpg.tab_bar():
            with dpg.tab(label=tab1str) as tab1:  # 1P 1CPU mode
                dpg.add_button(
                    label="Import Strategy...",
                    callback=lambda: dpg.show_item("strategy_fileselect")
                    )
                dpg.add_button(
                    label="Import Situation...",
                    callback=lambda: dpg.show_item("situation_fileselect")
                    )

                with dpg.tab_bar():
                    with dpg.tab(label=tab1_1str) as tab1_1:  # SP Setup
                        dpg.add_combo(list(melee.enums.Character), label="Chr")
                        dpg.add_combo([2, 3, 4], label="SP controller port")
                        dpg.add_separator()
                        with dpg.collapsing_header(label="Triggers", default_open=True) as head1:
                            dpg.add_button(label="(+) Add Trigger")
                        with dpg.collapsing_header(label="Responses", default_open=True) as head2:
                            dpg.add_button(label="(+) Add Response")

                    with dpg.tab(label=tab1_2str) as tab1_2:  # Situation setup
                        pass

                dpg.add_button(label="LAUNCH MELEE (test)",
                               callback=Interface.setup)
            # -----
            with dpg.tab(label=tab2str) as tab2:
                dpg.add_button(label="\nTest two\nStrategyPlayers\n")

    # user data and callback set when button is created
    dpg.add_button(label="Apply",
                   callback=cbx.button_callback,
                   user_data=tab1,
                   parent=tab1)

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

    import dearpygui.demo as demo
    demo.show_demo()

    if os.name == 'nt':
        # Windows-specific "high-DPI" bugfix for blurry text.
        # before showing the viewport/calling `show_viewport`:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)

    dpg.show_viewport()

    # below replaces start_dearpygui()
    while dpg.is_dearpygui_running():
        # insert here any code you would like to run in the render loop
        # you can manually stop by using stop_dearpygui()
        # ##print("this will run every frame")
        dpg.render_dearpygui_frame()

    dpg.destroy_context()
