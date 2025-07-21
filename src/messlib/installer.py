import importlib.resources
from platformdirs import PlatformDirs
import github
from packaging.version import Version
import os
import io
import importlib
import logging
import requests
import shutil
import subprocess
import sys
import zipfile

from .uilogging import MESSHandler


class _Installer:
    """
    Methods for downloading and configuring a Slippi installation for use with
    MESS. It seems too inconvenient/intrusive to just tack on to users'
    Slippi Launcher Playback installations."""
    def __init__(self):
        self.dirs = PlatformDirs(appauthor=None, appname="MESS")
        """ exposes:
        Installer.dirs.user_data_dir
                    ...user_config_dir
                    ...user_cache_dir
                    ...user_documents_dir
                    ...user_log_dir
        ...more: https://github.com/tox-dev/platformdirs
        """

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
        custom_ini_res = importlib.resources.files() / "res" / "GALE01r2.ini"
        shutil.copyfile(custom_ini_res, gecko_ini_path)

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
