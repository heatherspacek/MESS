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

    def analog_jump(self, angle: float):
        return Input(button=Button.BUTTON_X, coordinates=(0.5, 0.7))

    def back_air(self, direction: FacingDirection):
        backwards = (
            (0.5, 0.0) if direction == FacingDirection.LEFT
            else (0.5, 1.0)
        )
        return Input(c_coordinates=backwards)

    down_air = Input(c_coordinates=(0.0, 0.0))

    fastfall = Input(coordinates=(0.5, 0.0))

    def forward_air(self, direction: FacingDirection):
        forwards = (
            (0.5, 0.0) if direction == FacingDirection.RIGHT
            else (0.5, 1.0)
        )
        return Input(c_coordinates=forwards)

    def jump(self, angle: int | float = 90, quadrant: str = "UR"):
        return Input(button=Button.BUTTON_X)

    laser = Input(button=Button.BUTTON_B, coordinates=(0.5, 0.5))

    nair = Input(button=Button.BUTTON_A, coordinates=(0.5, 0.5))

    null = Input()  # No input

    up_air = Input(c_coordinates=(0.0, 1.0))


class Actions:
    """organizing class used so elements can be accessed with e.g.
    `Actions.wavedash_shallow`."""

    def all_actions():
        all_attributes = dir(Actions)
        return [attr for attr in all_attributes
                if not (attr.startswith("__") or attr == "all_actions")]

    def early_nair(
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

    def falco_laser(
        direction: FacingDirection,
        angle: int | float,
        height: int
    ):
        sequence = [Inputs.jump()] * jumpsquat(Character.FALCO)
        sequence.extend(Inputs.null * 10)
        sequence.append(Inputs.laser)
        sequence.append(Inputs.fastfall)
        return Action(sequence=sequence)

    def wavedash(
            character: Character,
            direction: FacingDirection, 
            angle: int | float
            ):
        sequence = [Inputs.jump()] * jumpsquat(character)
        sequence.append(
            Inputs.airdodge(
                angle,
                "BL" if direction == FacingDirection.LEFT else "BR"
                )
            )
        return Action(sequence=sequence)
