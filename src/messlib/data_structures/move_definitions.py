from melee.enums import Button, Character

from messlib.data_structures.classes import (Action, FacingDirection, Input,
                                             StochasticInput)
from messlib.data_structures.helpers import angle_to_meleecircle, jumpsquat


def _forwards(direction: FacingDirection) -> tuple[float]:
    return (1.0, 0.5) if direction == FacingDirection.LEFT else (0.0, 0.5)

def _backwards(direction: FacingDirection) -> tuple[float]:
    return (0.0, 0.5) if direction == FacingDirection.LEFT else (1.0, 0.5)


class Inputs:
    """Organizing class used so elements can be accessed with e.g.
    `Inputs.jump`.
    """

    def airdodge(angle: int | float, quadrant: str):
        return Input(
            button=Button.BUTTON_R, coordinates=angle_to_meleecircle(angle, quadrant)
        )

    def back_air(direction: FacingDirection):
        return Input(c_coordinates=_backwards(direction))

    def dash(direction: FacingDirection):
        return Input(coordinates=_forwards(direction))

    def down_air():
        return Input(c_coordinates=(0.5, 0.0))

    def fastfall():
        return Input(coordinates=(0.5, 0.0))

    def forward_air(direction: FacingDirection):
        return Input(c_coordinates=_forwards(direction))

    def jump(angle: int | float = 90, quadrant: str = "UR"):
        # TODO: analog angle(?)
        return Input(button=Button.BUTTON_X)

    def laser():
        return Input(button=Button.BUTTON_B, coordinates=(0.5, 0.5))

    def nair():
        return Input(button=Button.BUTTON_A, coordinates=(0.5, 0.5))

    def null():
        return Input()  # No input

    def up_air():
        return Input(c_coordinates=(0.5, 1.0))

    def up_smash():
        return Input(c_coordinates=(0.5, 1.0))


class Actions:
    """organizing class used so elements can be accessed with e.g.
    `Actions.wavedash_shallow`."""

    @staticmethod
    def all_actions():
        all_attributes = dir(Actions)
        return [
            attr
            for attr in all_attributes
            if not (attr.startswith("__") or attr == "all_actions")
        ]

    def early_dair(
        character: Character,
        direction: FacingDirection,
        angle: int | float,
        drift: float,
    ):
        # Jump with direction/angle specified:
        sequence = [Inputs.jump(angle=angle)] * jumpsquat(character) - 1
        # TODO: how do we fit drift in here????
        sequence.append(StochasticInput())
        sequence.append(Inputs.down_air())
        sequence.append(StochasticInput())
        sequence.append(Inputs.fastfall())
        return Action(sequence=sequence)

    def early_nair(
        character: Character, direction: FacingDirection, angle: int | float
    ):
        # Jump with a direction and angle specified by input arguments...
        sequence = [Inputs.jump()] * jumpsquat(character) - 1
        sequence.append(Inputs.nair())
        # Put a spacer in here-- a StochasticInput
        sequence.append(StochasticInput())
        sequence.append(Inputs.fastfall())
        return Action(sequence=sequence)

    def falco_laser(direction: FacingDirection, angle: int | float, height: int):
        sequence = [Inputs.jump()] * jumpsquat(Character.FALCO)
        sequence.extend(Inputs.null * 10)
        sequence.append(Inputs.laser)
        sequence.append(Inputs.fastfall)
        return Action(sequence=sequence)

    def jump_cancelled_upsmash(
        character: Character,
        direction: FacingDirection,
        frames_dashing: int
    ):
        sequence = [Inputs.dash(direction=direction) for _ in range(frames_dashing)]
        for _ in range(jumpsquat(character)):
            sequence.append(Inputs.jump)
        sequence.append(Inputs.up_smash)

    def wavedash(character: Character, direction: FacingDirection, angle: int | float):
        sequence = [Inputs.jump()] * jumpsquat(character)
        sequence.append(
            Inputs.airdodge(angle, "BL" if direction == FacingDirection.LEFT else "BR")
        )
        return Action(sequence=sequence)
