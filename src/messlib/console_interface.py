import logging
import melee
from messlib.installer import Installer  # for installed Slippi path
from messlib.uilogging import MESSHandler

"""
ISSUES:
-- on a fresh install, there will not be a "User" folder yet, which causes a
problem with libmelee. (make the Installer module fix this?)
-- on a fresh install, there will also not be anything in AppData/Local/MESS!
make sure this is considered OK!!
"""


class ConsoleInterface:
    """
    object exposing callables to interface with the libmelee `console`.
    """

    running = False
    alive = False
    console: melee.Console | None = None
    controller1: melee.Controller | None = None
    controller2: melee.Controller | None = None
    gamestate: melee.GameState | None = None

    def __init__(self, console_path: str):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(MESSHandler())
        self.logger.setLevel("DEBUG")

        self.alive = self._attempt_open_console(console_path)

    def _attempt_open_console(self, console_path: str):
        try:
            self.console = melee.Console(path=console_path)
            self.controller1 = melee.Controller(
                console=self.console, port=1, type=melee.ControllerType.GCN_ADAPTER
            )
            self.controller2 = melee.Controller(
                console=self.console, port=2, type=melee.ControllerType.STANDARD
            )
            return True
        except FileNotFoundError:
            # Installation has not occurred yet.
            self.console = None
            # Installer.install()
            # self._attempt_open_console(self, console_path=console_path)
            return False

    def setup_oneplayer(self):
        if self.console is None:
            # TODO: should prompt this first
            Installer.install()
            self._attempt_open_console()
        self.console.run()

    def step(self):
        if self.running:
            # Trying to ask for a step before setup has occurred can cause
            # unpredictable behaviour.
            self.gamestate = self.console.step()


Interface = ConsoleInterface(console_path=str(Installer.dirs.user_data_path))
