
from melee.enums import Character

from dataclasses import dataclass, field


@dataclass
class Action:
    sequence: list


@dataclass
class Trigger:
    pass


@dataclass
class Response:
    pass


@dataclass  # saves us from writing an __init__.
class Strategy:
    """
    A data structure that was specified through the builder UI.
    """
    name: str
    character: Character = Character.CPTFALCON  # from melee.enums
    triggers: list[Trigger] = field(default_factory=list)
    responses: list[Response] = field(default_factory=list)

    def add_trigger(self, trigger: Trigger):
        self.triggers.append(trigger)
