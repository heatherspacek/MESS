import melee.controller
from MESSabstract import Action
import melee

# ^ this seems like bad organization. will fix later.


class Actions:
    """organizing class used so they can be accessed with e.g.
    `Actions.wavedash_shallow`.
    """
    wavedash_shallow = Action(
        sequence=["jump", ]
        )
    
    short_hop = Action(
        sequence = []
    )
    
