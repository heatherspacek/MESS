from MESSabstract import Input, StochasticInput, Action
from melee.enums import Button, Character
from MESSaux import angle_to_meleecircle, jumpsquat, FacingDirection


class Inputs:
    """Organizing class used so elements can be accessed with e.g.
    `Inputs.jump`.
    Character is always assumed to be facing RIGHT"""

    def airdodge(self, angle: int | float, quadrant: str):
        return Input(
            button=Button.BUTTON_R,
            coordinates=angle_to_meleecircle(angle, quadrant)
            )

    def analog_jump(self, direction_ratio: float):
        return Input(button=Button.BUTTON_X, coordinates=(0.5, direction_ratio))

    back_air = Input(
        c_coordinates=()
    )

    fastfall = Input(coordinates=(0.5, 0.0))

    def jump(self, angle: int | float = 90, quadrant: str = "UR"):
        return Input(button=Button.BUTTON_X)

    nair = Input(button=Button.BUTTON_A, coordinates=(0.5, 0.5))

    null = Input()  # Serves to hold last input


class Actions:
    """organizing class used so elements can be accessed with e.g.
    `Actions.wavedash_shallow`."""

    def early_nair(
            self,
            character: Character,
            direction: FacingDirection,
            angle: int | float
            ):
        # Jump with a direction and angle specified by input arguments...
        sequence = [Inputs.jump()] * jumpsquat(character)
        sequence.append(Inputs.nair)
        # Put a spacer in here-- a StochasticInput
        sequence.append(StochasticInput())
        sequence.append(Inputs.fastfall)
        return Action(sequence=sequence)

    def wavedash_shallow(
            self,
            character: Character,
            direction: FacingDirection
            ):
        sequence = [Inputs.jump()] * jumpsquat(character)
        sequence.append(
            Inputs.airdodge(
                23,
                "BL" if direction == FacingDirection.LEFT else "BR"
                )
            )
        return Action(sequence=sequence)
