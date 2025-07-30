import logging
import multiprocessing as mp
import queue

import dearpygui.dearpygui as dpg
import dearpygui.demo as dpgdemo

# -
import messtool.tool_layout as app_layout
import messtool.tool_classes as app_classes
from messtool.singletons import GuiController

# -
from messlib.data_structures.classes import Strategy
from messlib.interfaces.uilogging import MESSHandler
from messlib.interfaces.strategy_player import StrategyPlayer
from messlib.interfaces.engine import Engine


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
    from messlib.interfaces.console_interface import Interface
    from messlib.interfaces.engine import Engine
    def testing_button():
        Interface.setup_oneplayer()
        Engine.start_bg_run()

    app_layout.layout_setup()
    dpg.add_button(label="testing button!",
                   parent="gamewnd",
                   callback=lambda _: testing_button()
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
    import time
    while dpg.is_dearpygui_running():
        # insert here any code you would like to run in the render loop
        # you can manually stop by using stop_dearpygui()
        # # # print("this will run every frame")
        t1 = time.perf_counter()
        dpg.render_dearpygui_frame()
        t2 = time.perf_counter()
        print(
            f"\nElapsed frame time: {t2-t1} sec "
            f"\nEngine ticks: {Engine.i}"
            )

    dpg.destroy_context()
