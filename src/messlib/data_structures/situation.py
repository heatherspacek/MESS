from dataclasses import dataclass
from melee.enums import Stage, Character


@dataclass
class Situation:
    """
    Represents a user-specified initial condition: stage, characters,
    and positions.
    In a later revision, more complex parameters may be added.

    TODO later: is a typeddict or namedtuple sufficient?
    dataclasses are not overhead per se but I've been bit before by...
    something. IDR what.
    oh god i remembver, DEFAULT FACTORIES
    TODO later: is this a good use of "pydantic"? probably overkill
    """

    stage: Stage

    p1_character: Character
    p1_percent: float
    p1_x_position: float
    p1_platform: bool

    p2_character: Character
    p2_percent: float
    p2_x_position: float
    p2_platform: bool


def sample_situation():
    return Situation(
        stage=Stage.YOSHIS_STORY,
        p1_character=Character.FOX,
        p1_percent=20.0,
        p1_x_position=5.7,
        p1_platform=False,
        p2_character=Character.FALCO,
        p2_percent=5.0,
        p2_x_position=-20.6,
        p2_platform=False,
    )
