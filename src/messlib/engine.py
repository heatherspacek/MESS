import logging
import queue
import threading
import time

from messlib.uilogging import MESSHandler
from messlib.console_interface import Interface


class _Engine:
    """
    Central engine to store various states (interface connection information),
    handles to threaded processes, and run-result/gamestate information."""
    def __init__(self):
        self._thread = None
        self._bg_running = False
        # logging
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(MESSHandler())
        self.logger.setLevel("DEBUG")
        self.i = 0

    def start_bg_run(self):
        """Start the worker if it's not already running."""
        if self._bg_running:
            return
        self._bg_running = True
        self._thread = threading.Thread(target=self._bg_run, daemon=True)
        self._thread.start()

    def _bg_run(self):
        self.logger.info("Background thread started.")
        self.i = 0
        try:
            while True:
                # START Background process loop -----vvvvv
                ...
                # END background process loop -----^^^^^

        except Exception as e:
            self.logger.error(f"exception from background thread: {e.__repr__()}")
        finally:
            self._bg_running = False


Engine = _Engine()
