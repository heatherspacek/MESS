import dearpygui.dearpygui as dpg
import melee
import os  # for os.path.join
import random
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

    # layout.window_layout(Interface, Player1, Player2)

    '''
    # below replaces start_dearpygui()
    while dpg.is_dearpygui_running():
        # insert here any code you would like to run in the render loop
        # you can manually stop by using stop_dearpygui()
        # ##print("this will run every frame")

        Interface.step()  # --> this updates Interface.gamestate
        # Player1.step(Interface.gamestate)
        # Player2.step(Interface.gamestate)
        if Interface.controller2 is not None:
            print("attempting to tilt")
            Interface.controller2.tilt_analog(melee.enums.Button.BUTTON_C, 0, 0)
        dpg.render_dearpygui_frame()

    dpg.destroy_context()

    '''

    ''' # Interface.setup()  # --> launches melee, '''
    # Interface.console.run()
    # Interface.console.connect()
    # !!!!!!!!!!!! controller instantiation must happen BEFORE console is run!
    controller2 = melee.Controller(console=console, port=2,
                                   type=melee.ControllerType.STANDARD)
    console.run()
    console.connect()

    controller2.connect()

    while True:
        controller2.tilt_analog(
                melee.enums.Button.BUTTON_C,
                random.random(),
                0.5
                )

    '''
    controller = melee.Controller(console=console,
                                  port=2,
                                  type=melee.ControllerType.STANDARD)

    console.run()
    print("Connecting to console...")
    if not console.connect():
        print("ERROR: Failed to connect to the console.")
        raise RuntimeError
    print("Console connected")

    print("Connecting controller to console...")
    if not controller.connect():
        print("ERROR: Failed to connect the controller.")
        raise RuntimeError
    print("Controller connected")

    while True:
        controller.tilt_analog(
                melee.enums.Button.BUTTON_C,
                random.random(),
                0.5
                )
    '''
