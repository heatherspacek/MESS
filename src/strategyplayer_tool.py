import logging
import multiprocessing as mp
import queue

import dearpygui.dearpygui as dpg
import dearpygui.demo as dpgdemo

# -
import messtool.tool_layout as app_layout
import messtool.tool_classes as app_classes
from messtool.singletons import GuiController
from messlib.uilogging import MESSHandler

# -
from messlib.classes_functional import StrategyPlayer
from messlib.classes_abstract import Strategy
from messlib.engine import Engine


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

    dpg.create_context()

    # Set up logging
    logger = logging.getLogger(__name__)
    logger.addHandler(MESSHandler())
    logger.setLevel("DEBUG")

    # View
    import messlib.installer
    app_layout.layout_setup()
    dpg.add_button(label="install",
                   parent="gamewnd",
                   callback=lambda _: messlib.installer.Installer.install()
                   )

    # logger.error("error!!!")
    # logger.info("info.")
    # logger.debug("debug~~")
    # logger.warning("waaarninggggg")
    # logger.critical("CRITICAL!")

    # dpgdemo.show_demo() ############################# DEMO WINDOW #####

    # dpg.set_exit_callback(...)

    # dpg.start_dearpygui()

    # below replaces, start_dearpygui()
    while dpg.is_dearpygui_running():
        # insert here any code you would like to run in the render loop
        # you can manually stop by using stop_dearpygui()
        # # # print("this will run every frame")
        dpg.render_dearpygui_frame()

    dpg.destroy_context()
