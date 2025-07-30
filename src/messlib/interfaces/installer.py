import importlib.resources
from platformdirs import PlatformDirs
import github
from packaging.version import Version
import os
import io
import melee
import importlib
import logging
import requests
import shutil
import subprocess
import sys
import zipfile

from .uilogging import MESSHandler

# https://imgur.com/a/4EuIt
CHARACTER_HEX_IDS = {
    melee.enums.Character.MEWTWO:   "0A",
    melee.enums.Character.NESS:     "0B",
    melee.enums.Character.PEACH:    "0C",
    melee.enums.Character.PIKACHU:  "0D",
    melee.enums.Character.POPO:     "",
    melee.enums.Character.PEACH:    "0C",
    melee.enums.Character.PEACH:    "0C",

    melee.enums.Character.PEACH:    "0C",
    melee.enums.Character.PEACH:    "0C",
    melee.enums.Character.PEACH:    "0C",
    melee.enums.Character.PEACH:    "0C",
    melee.enums.Character.PEACH:    "0C",
    melee.enums.Character.PEACH:    "0C",
    melee.enums.Character.PEACH:    "0C",
    melee.enums.Character.PEACH:    "0C",
    melee.enums.Character.PEACH:    "0C",
    melee.enums.Character.PEACH:    "0C",
    melee.enums.Character.PEACH:    "0C",
    melee.enums.Character.PEACH:    "0C",
    melee.enums.Character.PEACH:    "0C",
}

STAGE_HEX_IDS = {
    melee.enums.Stage.FOUNTAIN_OF_DREAMS:   "02",
    melee.enums.Stage.POKEMON_STADIUM:      "03",
    melee.enums.Stage.YOSHIS_STORY:         "08",
    melee.enums.Stage.DREAMLAND:            "1C",
    melee.enums.Stage.BATTLEFIELD:          "1F",
    melee.enums.Stage.FINAL_DESTINATION:    "20",
}

CONFIG_CODE = """\
$MESS: Boot to Game [UnclePunch]
*Check Player and Stage IDs for Custom Match to boot into.
041a45c0 3860000E #Boot to In Game
C21B148C 00000025
3C608048 60630530
48000021 7C8802A6
38A000F0 3D808000
618C31F4 7D8903A6
4E800421 480000F8
4E800021 2A08024C
20000000 000000FF
000000{0} 000001E0
00000000 00000000
00000000 FFFFFFFF
FFFFFFFF 00000000
3F800000 3F800000
3F800000 00000000
00000000 00000000
00000000 00000000
00000000 00000000
00000000 00000000
00000000 {1}000400#character 1
00FF0000 09007800
40000401 00{2}0000#starting percent
00000000 3F800000
3F800000 3F800000
{3}000400 00FF0000#character 2
09007800 40000401
00{4}0000 00000000#starting percent
3F800000 3F800000
3F800000 09030400
00FF0000 09007800
40000401 00000000
00000000 3F800000
3F800000 3F800000
09030400 00FF0000
09007800 40000401
00000000 00000000
3F800000 3F800000
3F800000 BB610014
60000000 00000000
"""

"""
04480590 {0}0000{1} #0 = P1 Character / 1 = P1 Color
044805b4 {2}0000{3} #2 = P2 Character / 3 = P2 Color
0416e7f4 386000{4} #4 = Stage ID
0446db68 3201864c
0416d904 38800004
0416ddb4 380001E0
0446db6c 83000000
C216DD6C 00000005
3DC08046 61CEDB68
3C603200 6063864C
906E0000 3C60C300
906E0004 887F24C8
60000000 00000000\
"""

class _Installer:
    """
    Methods for downloading and configuring a Slippi installation for use with
    MESS. It seems too inconvenient/intrusive to just tack on to users'
    Slippi Launcher Playback installations."""
    def __init__(self):
        self.dirs = PlatformDirs(appauthor=None, appname="MESS")
        """
        https://github.com/project-slippi/Ishiiruka-Playback/
        """
        self.github_client = None
        self.dolphin_repo = None
        self.remote_latest = None

        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(MESSHandler())
        self.logger.setLevel("DEBUG")

    def _query_github(self):
        if self.remote_latest is None:
            self.github_client = github.Github()
            try:
                self.dolphin_repo = self.github_client.get_repo("project-slippi/Ishiiruka-Playback")
            except requests.exceptions.ConnectionError:
                self.logger.error("Error connecting to GitHub to check for Dolphin updates.")
                return
            self.remote_latest = self.dolphin_repo.get_latest_release()

    def _check_current_installation(self) -> bool:
        """Returns True if installation is OK"""
        try:
            with open(self.dirs.user_data_path / ".version", "r") as f:
                installed_version_str = f.readline()
        except FileNotFoundError:
            return False
        self._query_github()
        return Version(self.remote_latest.tag_name) <= Version(installed_version_str)

    def _install_latest_release(self):
        self._query_github()
        remote_assets = self.remote_latest.assets
        if sys.platform == "win32":
            correct_asset = [a for a in remote_assets if "Win" in a.name]
            if not any(correct_asset):
                # Don't `raise`, we can just log these.
                # raise RuntimeError("Can't find a valid Slippi version on the remote. Aborting")
                return
            correct_asset_url = correct_asset[0].browser_download_url
            response = requests.get(correct_asset_url, allow_redirects=True)
            if not response.ok:
                # Don't `raise`, we can just log these.
                # raise RuntimeError("Attempt to download Slippi from remote failed.")
                return
            zip_file = zipfile.ZipFile(io.BytesIO(response.content))
            zip_file.extractall(self.dirs.user_data_dir)
            # ... log: extraction complete/successful!
            with open(self.dirs.user_data_path / ".version", 'w') as f:
                f.write(self.remote_latest.tag_name)

            # --- end windows handling ---
        elif sys.platform == "darwin":
            ...  # idk how to install a dmg lol
        elif sys.platform == "linux":
            correct_asset = [a for a in remote_assets if "Linux" in a.name]
            if not any(correct_asset):
                self.logger.error("no matching release asset found on Ishiruuka-Playback GitHub.")
                return
            correct_asset_url = correct_asset[0].browser_download_url
            self.logger.info("starting download of latest Slippi Playback release...")
            response = requests.get(correct_asset_url, allow_redirects=True)
            if not response.ok:
                self.logger.error("download from Ishiruuka-Playback GitHub failed.")
                return
            zip_file = zipfile.ZipFile(io.BytesIO(response.content))
            zip_file.extractall(self.dirs.user_data_dir)
            with open(self.dirs.user_data_path / ".version", 'w') as f:
                f.write(self.remote_latest.tag_name)
            appimage_path = self.dirs.user_data_path / "Slippi_Playback-x86_64.AppImage"
            current_permissions = os.stat(appimage_path)
            os.chmod(appimage_path, current_permissions.st_mode | 0o111)
            # Additionally, perform a "appimage-extract" to expose config files
            subprocess.Popen(["./Slippi_Playback-x86_64.AppImage", "--appimage-extract"],
                             cwd=self.dirs.user_data_path)
        else:
            ...
            # log an error about not recognizing the current platform.
        self.logger.info("Slippi Playback download complete.")

    def install(self):
        """check for an existing installation, and if it is not found, install"""
        if not self._check_current_installation():
            self._install_latest_release()
            self._configure_slippi()

    def _configure_slippi(self):
        """note for later:
        immediately after install (on linux),
        squashfs-root/usr/bin/Sys/GameSettings/GALE01r2.ini DOES exist.
        This is definitely platform-dependent, and may not be present
        immediately after install on some systems. TODO"""
        gecko_ini_path = (
            self.dirs.user_data_path
            / "squashfs-root"
            / "usr"
            / "bin"
            / "Sys"
            / "GameSettings"
            / "GALE01r2.ini"
        )
        custom_ini_res = importlib.resources.files() / ".." / "res" / "GALE01r2.ini"
        shutil.copyfile(custom_ini_res, gecko_ini_path)
        dummy_options = (
            "02", #stage
            "00", #ch
            "2A", # %
            "01", #ch
            "2A" # %
        )
        with open(gecko_ini_path, "a") as append_stream:
            append_stream.write(CONFIG_CODE.format(*dummy_options))

    def uninstall(self):
        if self._check_current_installation():
            print("about to uninstall local slippi installation! are you sure?")
            user_input = input().lower()
            if user_input == "y":
                shutil.rmtree(self.dirs.user_data_path)


# Expose instance (singleton)
Installer = _Installer()

if __name__ == "__main__":
    Installer.uninstall()
    Installer.install()
