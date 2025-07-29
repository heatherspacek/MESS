import logging
import melee
import configparser
import os
import shutil
import sys
from messlib.interfaces.installer import Installer  # for installed Slippi path
from messlib.interfaces.uilogging import MESSHandler

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
    iso_path: str | None = None
    console: melee.Console | None = None
    controller1: melee.Controller | None = None
    controller2: melee.Controller | None = None
    gamestate: melee.GameState | None = None

    def __init__(self, console_path: str):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(MESSHandler())
        self.logger.setLevel("DEBUG")

        self.alive = self._attempt_open_console(console_path)
        # --- replace later.
        self.iso_path = "/home/heather/Documents/Disk Images/Super Smash Bros. Melee (v1.02).iso"

    def _patch_dolphin_config(self):
        # TODO: this is only tested on Linux right now.
        os.makedirs(Installer.dirs.user_config_path, exist_ok=True)
        config = configparser.ConfigParser()
        dolphin_ini_path = (
            Installer.dirs.user_config_path / ".." / "SlippiPlayback"/ "Config"
            / "Dolphin.ini"
        )
        if not os.path.isfile(dolphin_ini_path):
            raise FileNotFoundError("dolphin.ini not found in the expected location."
                                    f" Tried looking in {dolphin_ini_path}")
        config.read(dolphin_ini_path)
        config.set("Display", "RenderToMain", "True")
        config.set("Input", "backgroundinput", "True")
        config.set("Display", "Fullscreen", "False")
        with open(dolphin_ini_path, "w") as dolphinfile:
            config.write(dolphinfile)

    def _attempt_open_console(self, console_path: str):
        try:
            self.console = melee.Console(
                path=console_path,
                dolphin_home_path=console_path,
                tmp_home_directory=False
                )
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
        self.console.run(iso_path=self.iso_path)

    def step(self):
        if self.running:
            # Trying to ask for a step before setup has occurred can cause
            # unpredictable behaviour.
            self.gamestate = self.console.step()


# On linux, the installation path is not exactly the user_data_path.
# We should actually ask the Installer what platform we are on, but doesnt hurt
# to re-do. 

_install_path = Installer.dirs.user_data_path
if sys.platform == "linux":
    _install_path = _install_path / "squashfs-root" / "usr" / "bin"

Interface = ConsoleInterface(console_path=str(_install_path))

if __name__ == "__main__":
    Interface.setup_oneplayer()
