import melee
import numpy as np


def jumpsquat(character: melee.enums.Character):
    match character:
        case (
            melee.enums.Character.LINK
            | melee.enums.Character.GANONDORF
            | melee.enums.Character.ZELDA
        ):
            return 6
        case (
            melee.enums.Character.DK
            | melee.enums.Character.FALCO
            | melee.enums.Character.PEACH
            | melee.enums.Character.JIGGLYPUFF
            | melee.enums.Character.ROY
            | melee.enums.Character.MEWTWO
            | melee.enums.Character.YOSHI
        ):
            return 5
        case (
            melee.enums.Character.CPTFALCON
            | melee.enums.Character.DOC
            | melee.enums.Character.GAMEANDWATCH
            | melee.enums.Character.LUIGI
            | melee.enums.Character.MARIO
            | melee.enums.Character.MARTH
            | melee.enums.Character.NESS
            | melee.enums.Character.YLINK
        ):
            return 4
        case (
            melee.enums.Character.FOX
            | melee.enums.Character.KIRBY
            | melee.enums.Character.PICHU
            | melee.enums.Character.PIKACHU
            | melee.enums.Character.POPO
            | melee.enums.Character.SAMUS
            | melee.enums.Character.SHEIK
        ):
            return 3


def angle_to_meleecircle(angle: int, quadrant: str):
    """returns an X and Y that are on the rim of the unit circle.
    input in degrees. intended for use with DI and WDs"""
    if (angle > 90.0) or (angle < 0.0):
        print("error in angle_to_meleecircle: need 0<angle<90 for clarity")
        raise
    # numpy likes radians...
    angle_radians = np.pi * angle / 180.0
    xc_u = np.cos(angle_radians)
    yc_u = np.sin(angle_radians)

    "next, map 0..1 to 0.5..1"
    match quadrant:
        case "UL":
            xc = 0.5 - xc_u / 2
            yc = 0.5 + yc_u / 2
        case "UR":
            xc = 0.5 + xc_u / 2
            yc = 0.5 + yc_u / 2
        case "BL":
            xc = 0.5 - xc_u / 2
            yc = 0.5 - yc_u / 2
        case "BR":
            xc = 0.5 + xc_u / 2
            yc = 0.5 - yc_u / 2
        case _:
            raise RuntimeError(
                "error in angle_to_meleecircle: " + "specified an invalid quadrant"
            )
    return (xc, yc)
