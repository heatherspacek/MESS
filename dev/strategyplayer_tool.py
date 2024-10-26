import dearpygui.dearpygui as dpg
import melee
import os  # for os.path.join
import ctypes
from dataclasses import dataclass
# -
import strategyplayer_tool_callbacks as cbx
# -
# from MESSaux import jumpsquat  # not actually useful. placeholder organization
from MESSabstract import Trigger, Response, Strategy

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
    loaded_strategy: Strategy


class ConsoleInterface():
    """
    object exposing callables to interface with the libmelee `console`.
    """
    running = False
    console = None
    controller1 = None
    controller2 = None

    def __init__(self, console: melee.Console):
        self.console = console

    def setup(self):
        self.console.run()
        self.console.connect()
        self.controller1 = melee.Controller(console=self.console, port=1)
        self.controller2 = melee.Controller(console=self.console, port=2)
        self.controller1.connect()
        self.controller2.connect()

    def step(self):
        gamestate = self.console.step()


"""
===============================================================================
app entry point.
===============================================================================
"""

if __name__ == "__main__":

    slippi_playback_path = os.path.join(os.environ["APPDATA"],
                                        "Slippi Launcher", "playback")
    console = melee.Console(path=slippi_playback_path)

    Interface = ConsoleInterface(console)
    Gsm = GlobalState()

    dpg.create_context()

    # =====
    # the "start panel"...
    tab1str = "[1P, 1CPU] Play against a StrategyPlayer"
    tab2str = "[0P, 2CPU] Init two StrategyPlayers"
    tab1_1str = "SP Setup"
    tab1_2str = "Situation Setup"

    with dpg.window(label="START HERE") as top_level_wnd:
        dpg.set_item_width(top_level_wnd, 350)
        dpg.set_item_height(top_level_wnd, 350)
        with dpg.tab_bar():
            with dpg.tab(label=tab1str) as tab1:
                with dpg.tab_bar():
                    with dpg.tab(label=tab1_1str) as tab1_1:
                        pass
                    with dpg.tab(label=tab1_2str) as tab1_2:
                        pass

                dpg.add_button(label="\nPlay against a\nStrategyPlayer\n")
                dpg.add_button(label="LAUNCH MELEE (test)",
                               callback=Interface.setup)
            with dpg.tab(label=tab2str) as tab2:
                dpg.add_button(label="\nTest two\nStrategyPlayers\n")

    # user data and callback set when button is created
    dpg.add_button(label="Apply",
                   callback=cbx.button_callback,
                   user_data=tab1,
                   parent=tab1)

    # user data and callback set any time after button has been created
    # #btn = dpg.add_button(label="Apply 2 \nmore lines", parent=group1)
    # #dpg.set_item_callback(btn, cbx.button_callback)
    # #dpg.set_item_user_data(btn, "Some Extra User Data")

    # Viewport creation (the window)
    dpg.create_viewport(title='StrategyPlayer Invocation Tool', width=400, height=600)
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

    # dpg.show_font_manager()

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
