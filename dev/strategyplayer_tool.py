import dearpygui.dearpygui as dpg
import melee
import os  # for os.path.join
from dataclasses import dataclass
# -
import strategyplayer_tool_layout as layout
import dearpygui.demo as demo
# -
from MESSaux import ConsoleInterface, StrategyPlayer


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
    Console = melee.Console(path=slippi_playback_path)

    Interface = ConsoleInterface(Console)
    Gsm = GlobalState()

    Player1 = StrategyPlayer()
    Player2 = StrategyPlayer()

    layout.window_layout(Interface, Player1, Player2)

    demo.show_demo()

    dpg.start_dearpygui()

    dpg.destroy_context()
