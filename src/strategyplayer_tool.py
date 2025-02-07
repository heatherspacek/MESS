import dearpygui.dearpygui as dpg
import dearpygui.demo as dpgdemo
import melee
import os  # for os.path.join
# -
import messtool.strategyplayer_tool_layout as app_layout
import messtool.strategyplayer_tool_classes as app_classes
# -
from messlib.classes_functional import ConsoleInterface, StrategyPlayer
from messlib.classes_abstract import Strategy

"""
===============================================================================
app entry point.
===============================================================================
"""

if __name__ == "__main__":

    # Elements needed to launch/interact with melee
    slippi_playback_path = os.path.join(os.environ["APPDATA"],
                                        "Slippi Launcher", "playback")
    Console = melee.Console(path=slippi_playback_path)
    Interface = ConsoleInterface(Console)

    # Model
    EmptyStrategy = Strategy()
    Player1 = StrategyPlayer()
    Player2 = StrategyPlayer()
    Player2.loaded_strategy = EmptyStrategy

    # Controller (in the M-V-C sense, not game-controller)
    GuiController = app_classes.GuiController()
    GuiController.loaded_strategy = EmptyStrategy

    # View
    app_layout.layout_setup(GuiController)

    dpgdemo.show_demo()

    dpg.start_dearpygui()
    dpg.destroy_context()
