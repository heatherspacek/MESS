from ..messlib.interfaces.host import Host
from ..messlib.data_structures.situation import Situation


class PayoffSolver:
    """
    """
    def __init__(self, host: Host, situation: Situation):
        self.host = host
        self.situation = situation

