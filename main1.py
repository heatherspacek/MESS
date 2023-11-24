import melee
import pdb
from MESSaux import compose_codestring, character_go_to_x

relative_path = "../Slippi Install/squashfs-root/usr/bin/"

# Before starting the console, install the codeset that will make melee boot to match:
codes_relative_path = "../Slippi Install/squashfs-root/usr/bin/Sys/GameSettings/GALE01r2.ini"
#with open(codes_relative_path,"a") as fileobj:
#    fileobj.write(compose_codestring())

#pdb.set_trace()

console = melee.Console(path=relative_path)

controller1 = melee.Controller(console=console, port=1)
controller2 = melee.Controller(console=console, port=2)
#controller_human = melee.Controller(console=console,
#                                    port=2,
#                                    type=melee.ControllerType.STANDARD)

console.run()
console.connect()

controller1.connect()
controller2.connect()
#controller_human.connect()

situation_initialized = False

# Later, this struct will come from the setup UI.
init_struct = {
    "p1_pos_x": 0.0,
    "p2_pos_x": 0.0,

}

while True:
    gamestate = console.step()
    
    if gamestate.menu_state in [melee.Menu.IN_GAME, melee.Menu.SUDDEN_DEATH]:
        # Let's determine some inputs :]

        if situation_initialized == False:
            "Situation has not been initialized yet. We will set it up, save a savestate, and set the flag."
            # Code adapted from libmelee/melee/techskill.py
            #pdb.set_trace()
            character_go_to_x(-35.0, gamestate.players[1], controller1)
            character_go_to_x(40.0, gamestate.players[2], controller2)
            # TODO: how to set a facing direction?

        else:
            "Ready to iterate!"
            pass
        #
    else:
        # should only occur on first boot?
        # Will probably execute any time "between" games too, but that shouldn't matter.
        melee.MenuHelper.menu_helper_simple(gamestate,
                                        controller1, 
                                        melee.Character.FOX, 
                                        melee.Stage.BATTLEFIELD,
                                        [], # connect code-- blank for VS
                                        0, # cpu level
                                        1, # costume
                                        False, # autostart
                                        False # swag
                                        )
        melee.MenuHelper.menu_helper_simple(gamestate,
                                        controller2, 
                                        melee.Character.CPTFALCON, 
                                        melee.Stage.BATTLEFIELD,
                                        [], # connect code-- blank for VS
                                        0, # cpu level
                                        1, # costume
                                        True, # autostart
                                        False # swag
                                        )