import dearpygui.dearpygui as dpg
import melee
import os  # for os.path.join
# -
import messtool.strategyplayer_tool_layout as layout
import dearpygui.demo as demo
# -
from messlib.classes_functional import ConsoleInterface, StrategyPlayer
from messlib.classes_abstract import Strategy

"""
===============================================================================
app entry point.
===============================================================================
"""

if __name__ == "__main__":

    slippi_playback_path = os.path.join(os.environ["APPDATA"],
                                        "Slippi Launcher", "playback")
    Console = melee.Console(path=slippi_playback_path)

    Interface = ConsoleInterface(Console)

    EmptyStrategy = Strategy()

    Player1 = StrategyPlayer()
    Player2 = StrategyPlayer()
    Player2.loaded_strategy = EmptyStrategy

    layout.window_layout(Interface, Player1, Player2)

    if True:
        demo.show_demo()

    dpg.start_dearpygui()

    dpg.destroy_context()
