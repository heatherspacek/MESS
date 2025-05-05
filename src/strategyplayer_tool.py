import dearpygui.dearpygui as dpg
import dearpygui.demo as dpgdemo

# -
import messtool.tool_layout as app_layout
import messtool.tool_classes as app_classes
from messtool.singletons import GuiController

# -
from messlib.classes_functional import StrategyPlayer
from messlib.classes_abstract import Strategy

"""
===============================================================================
app entry point.
===============================================================================
"""

if __name__ == "__main__":
    # Model
    EmptyStrategy = Strategy()
    Player1 = StrategyPlayer()
    Player2 = StrategyPlayer()
    Player2.loaded_strategy = EmptyStrategy

    # Controller (in the M-V-C sense, not game-controller)
    GuiController.loaded_strategy = EmptyStrategy

    # View
    app_layout.layout_setup()

    # ###### dpgdemo.show_demo()

    dpg.start_dearpygui()
    dpg.destroy_context()
