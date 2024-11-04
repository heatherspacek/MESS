import melee
from MESSaux import character_go_to_x
from MESSabstract import TrivialStrategy

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

situation_initialized = False
arrived1 = False
arrived2 = False
savestate_initialized = False
save_frame_counter = 15; 

# Later, this struct will come from the setup UI.
init_struct = {
    "p1_pos_x": -45.0,
    "p2_pos_x": 15.0,
    "p1_facing": "R",
    "p2_facing": "L"

}

Strategy1 = TrivialStrategy("pepis")
Strategy2 = TrivialStrategy("spamm")

while True:
    gamestate = console.step()
    
    if gamestate.menu_state in [melee.Menu.IN_GAME, melee.Menu.SUDDEN_DEATH]:
        # Let's determine some inputs :]

        if not situation_initialized:
            # Code adapted from libmelee/melee/techskill.py
            if not arrived1: 
                if character_go_to_x(init_struct["p1_pos_x"], init_struct["p1_facing"], gamestate.players[1], controller1):
                    arrived1 = True
            else:
                controller1.release_all()
                controller1.tilt_analog(melee.enums.Button.BUTTON_MAIN, 0.5, 0.5)

            if not arrived2:
                if character_go_to_x(init_struct["p2_pos_x"], init_struct["p2_facing"], gamestate.players[2], controller2):
                    arrived2 = True
            else:
                controller2.release_all()
                controller2.tilt_analog(melee.enums.Button.BUTTON_MAIN, 0.5, 0.5)
            situation_initialized = arrived1 and arrived2
            continue
        #
        if situation_initialized and not savestate_initialized:
            # first frame(s) after init. allow for shield-release frames and then set savestate
            save_frame_counter -= 1
            controller1.release_all()
            controller2.release_all()
            if save_frame_counter == 0:
                controller1.press_button(melee.enums.Button.BUTTON_D_RIGHT)
                savestate_initialized = True
            continue
        #
        "Ready to iterate!"
        "TODO: consult MESS manager to see whether the situation has resolved, and see whether to update or switch to a new S1/S2."
        "Consult strategy1 and strategy2."
        actions1 = Strategy1.consult()
        actions2 = Strategy2.consult()

        controller1.release_all()
        controller1.tilt_analog(melee.enums.Button.BUTTON_MAIN, 0.5, 0.5)
        controller2.release_all()
        controller2.tilt_analog(melee.enums.Button.BUTTON_MAIN, 0.5, 0.5)
        #
    else:
        # should only occur on first boot?
        # Will probably execute any time "between" games too, but that shouldn't matter.
        melee.MenuHelper.menu_helper_simple(gamestate,
                                        controller1, 
                                        melee.Character.FOX, 
                                        melee.Stage.FINAL_DESTINATION,
                                        [], # connect code-- blank for VS
                                        0, # cpu level
                                        1, # costume
                                        False, # autostart
                                        False # swag
                                        )
        melee.MenuHelper.menu_helper_simple(gamestate,
                                        controller2, 
                                        melee.Character.CPTFALCON, 
                                        melee.Stage.FINAL_DESTINATION,
                                        [], # connect code-- blank for VS
                                        0, # cpu level
                                        1, # costume
                                        True, # autostart
                                        False # swag
                                        )