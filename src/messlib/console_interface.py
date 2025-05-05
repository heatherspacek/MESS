import melee
import os

# Elements needed to launch/interact with melee
_slippi_playback_path = os.path.join(
    os.environ["APPDATA"], "Slippi Launcher", "playback"
)


class ConsoleInterface:
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
        self.controller1 = melee.Controller(
            console=console, port=1, type=melee.ControllerType.GCN_ADAPTER
        )
        self.controller2 = melee.Controller(
            console=console, port=2, type=melee.ControllerType.STANDARD
        )

    def setup_oneplayer(self):
        self.console.run()
        print("Connecting to console...")
        if not self.console.connect():
            print("ERROR: Failed to connect to the console.")
            raise RuntimeError
        print("Console connected.")
        if not self.controller2.connect():
            print("ERROR: CPU controller failed to connect.")
            raise RuntimeError
        print("CPU controller connected.")
        self.running = True

    def step(self):
        if self.running:
            # Trying to ask for a step before setup has occurred can cause
            # unpredictable behaviour.
            self.gamestate = self.console.step()


_console = melee.Console(path=_slippi_playback_path)
Interface = ConsoleInterface(console=_console)
