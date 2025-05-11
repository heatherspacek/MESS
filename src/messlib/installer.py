from platformdirs import PlatformDirs
import github
from packaging.version import Version
import io
import requests
import sys
import zipfile


class Installer:
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

    def _query_github(self):
        self.github_client = github.Github()
        try:
            self.dolphin_repo = self.github_client.get_repo("project-slippi/Ishiiruka-Playback")
        except requests.exceptions.ConnectionError:
            print("Error connecting to GitHub to check for Dolphin updates.")
            ...
            return
        self.remote_latest = self.dolphin_repo.get_latest_release()

    def _check_current_installation(self):
        ...

    def _get_latest_release(self):
        self._query_github()
        Version(self.remote_latest.tag_name)  # do checking on this to compare current installation

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
            with open(self.dirs.user_data_path / "VERSION", 'w') as f:
                f.write(self.remote_latest.tag_name)

            # --- end windows handling ---
        elif sys.platform == "darwin":
            ...  # idk how to install a dmg lol
        elif sys.platform == "linux":
            ...  # zip contains an "appimage". ill look into it later
        else:
            ...
            # log an error about not recognizing the current platform.

    def _check_installation(self) -> int:
        ...

    def install(self):
        install_status = self._check_installation()
        ...

    def update(self):
        if not self._check_installation():
            # All is well!
            ...
        


# Expose instance (singleton)
Installer = Installer()
