import github
import logging
import os
import requests
import shutil
import subprocess
from packaging.version import Version
from platformdirs import PlatformDirs

import tqdm


class Installer2:
    """
    Methods for downloading and configuring a Slippi installation for
    use with MESS.
    "...2" because I am weirdly decision-paralyzed about the previous
    work and prefer to start again, apparently.

    NOT portable or general. This installs on Linux only. It also
    targets `vladfi1`'s fork of Ishiirkua Dolphin:
    https://github.com/vladfi1/slippi-Ishiiruka/releases/tag/exi-ai-0.2.0
    """

    PLAYBACK_REPO = "vladfi1/slippi-Ishiiruka"

    def __init__(self):
        self.dirs = PlatformDirs(appauthor=None, appname="MESS")
        self.github_client = None
        self.dolphin_repo = None
        self.remote_latest = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel("DEBUG")

    def _query_github(self):
        if self.remote_latest is None:
            self.github_client = github.Github()
            try:
                self.dolphin_repo = self.github_client.get_repo(self.PLAYBACK_REPO)
            except requests.exceptions.ConnectionError:
                self.logger.error(
                    "Error connecting to GitHub to check for Dolphin updates."
                )
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
        return True
        # return Version(self.remote_latest.tag_name) <= Version(installed_version_str)

    def _install_latest_release(self):
        os.makedirs(self.dirs.user_data_path, exist_ok=True)
        self._query_github()
        remote_assets = self.remote_latest.assets
        # TODO: fixup, theres only one asset in these builds now
        asset = [a for a in remote_assets if "Slippi_Online" in a.name][0]
        correct_asset_url = asset.browser_download_url
        self.logger.info("starting download of latest Slippi Playback release...")
        response = requests.get(correct_asset_url, stream=True, allow_redirects=True)

        if not response.ok:
            self.logger.error("download from Ishiruuka-Playback GitHub failed.")
            return

        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024

        appimage_path = self.dirs.user_data_path / asset.name

        with tqdm.tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
            with open(appimage_path, "wb") as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)

        with open(self.dirs.user_data_path / ".version", "w") as f:
            f.write(self.remote_latest.tag_name)

        # Additionally, perform a "appimage-extract" to expose config files
        current_permissions = os.stat(appimage_path)
        os.chmod(appimage_path, current_permissions.st_mode | 0o111)
        subprocess.Popen(
            [f"./{asset.name}", "--appimage-extract"], cwd=self.dirs.user_data_path
        )

    def uninstall(self):
        if self._check_current_installation():
            print("about to uninstall local slippi installation! are you sure?")
            user_input = input().lower()
            if user_input == "y":
                shutil.rmtree(self.dirs.user_data_path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    Inst = Installer2()
    Inst.uninstall()
    Inst._install_latest_release()
