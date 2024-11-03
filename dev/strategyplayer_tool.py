import dearpygui.dearpygui as dpg
import melee
import os  # for os.path.join
from dataclasses import dataclass
# -
import strategyplayer_tool_layout as layout
# -
# from MESSaux import jumpsquat  # not actually useful. placeholder
from MESSabstract import Strategy
from MESSaux import ConsoleInterface, StrategyPlayer

# #######look up "blinker" package; do i need this type of inter-object comms?


@dataclass
class GlobalState():
    """
    storage for useful global states"""
    pass


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

    S1 = Strategy()

    Player1 = StrategyPlayer()
    Player1.loaded_strategy = S1

    Player2 = StrategyPlayer()

    layout.window_layout(Interface, Player1, Player2)

    # below replaces start_dearpygui()
    while dpg.is_dearpygui_running():
        # insert here any code you would like to run in the render loop
        # you can manually stop by using stop_dearpygui()
        # ##print("this will run every frame")
        dpg.render_dearpygui_frame()

    dpg.destroy_context()
