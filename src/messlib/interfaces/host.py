import melee
from .patcher import patch_installation


class Host:
    """
    libmelee console host.
    """

    def __init__(self):
        self.console = None
        # --- replace later.
        self.iso_path = "/home/heather/Documents/Disk Images/Super Smash Bros. Melee (v1.02).iso"

    def setup(self):
        self.console = melee.Console(
            path="/home/heather/.local/share/MESS/squashfs-root/usr/bin/dolphin-emu",
            gfx_backend="Null",
            disable_audio=True,
            use_exi_inputs=False,
            enable_ffw=False,
            blocking_input=True,
            dolphin_home_path="/home/heather/.local/share/MESS/squashfs-root/usr/bin/Sys"
        )

        # this libmelee fork does Gecko code insertion at constructor.
        # So, we need to patch HERE.
        patch_installation(dest_ini_path=self.console.dolphin_home_path + "/GameSettings/GALE01r2.ini")
        self.p1 = melee.Controller(
            console=self.console,
            port=1,
            type=melee.ControllerType.STANDARD,
            fix_analog_inputs=False
        )
        self.p2 = melee.Controller(
            console=self.console,
            port=2,
            type=melee.ControllerType.STANDARD,
            fix_analog_inputs=False
        )

        self.console.run(iso_path=self.iso_path)
        self.console.connect()

        self.p1.connect()
        self.p2.connect()

        menuhelper = melee.menuhelper.MenuHelper()
        gs = self.console.step()
        for _ in range(250):
            if gs.menu_state == melee.enums.Menu.IN_GAME:
                return
            else:
                for i, conch in enumerate((self.p1, self.p2)):
                    menuhelper.menu_helper_simple(
                        gs,
                        conch,
                        melee.Character.FOX,
                        melee.Stage.YOSHIS_STORY,
                        costume=i,
                        autostart=True,
                        swag=False
                    )
                gs = self.console.step()

        # Ran out of iterations
        raise RuntimeError("Failed to start game within 200 console steps. Sorry")

    def _debug_control(self):
        from .vis import print_gamestate
        while True:
            inp = input(">")
            if 'q' in inp:
                break
            x = 0.5
            y = 0.5
            self.p1.release_all()
            self.p2.release_all()
            if 'a' in inp:
                x -= 0.5
            if 's' in inp:
                y -= 0.5
            if 'd' in inp:
                x += 0.5
            if 'w' in inp:
                y += 0.5
            if 'r' in inp:
                self.p1.press_button(melee.enums.Button.BUTTON_R)
            if 'i' in inp:
                self.p1.press_button(melee.enums.Button.BUTTON_D_UP)
            if 'j' in inp:
                self.p1.press_button(melee.enums.Button.BUTTON_D_LEFT)
            if 'k' in inp:
                self.p1.press_button(melee.enums.Button.BUTTON_D_DOWN)
            if 'l' in inp:
                self.p1.press_button(melee.enums.Button.BUTTON_D_RIGHT)
            if 'z' in inp:
                self.p1.press_button(melee.enums.Button.BUTTON_A)
            if 'K' in inp:
                self.p2.press_button(melee.enums.Button.BUTTON_D_DOWN)
            self.p1.tilt_analog(melee.enums.Button.BUTTON_MAIN, x, y)
            self.p2.tilt_analog(melee.enums.Button.BUTTON_MAIN, x, y)
            self.p1.flush()
            self.p2.flush()
            gs = self.console.step()
            print_gamestate(gs)


if __name__ == "__main__":
    MeleeHost = Host()
    MeleeHost.setup()

    for _ in range(500):
        # Advance time to make sure we're off the respawn plat.
        MeleeHost.console.step()

    MeleeHost._debug_control()

    """
    import time
    t0 = time.perf_counter()
    for _ in range(1000):
        # Advance time to make sure we're off the respawn plat.
        MeleeHost.console.step()
    t1 = time.perf_counter()
    print((t1-t0), " seconds for 1000 frames,")
    print("(realtime would be 16.66.)", (16.66 / (t1-t0)), "x speedup")
    """

    """
    # Try various delays to see which ones cause the controller pipe to
    # break?

    import time
    for pause_dur in [a for a in range(5)]:
        print("pausing for ", pause_dur, "==========")
        time.sleep(pause_dur)
        # action check
        for i in [(i % 3)/2 for i in range(9, 0, -1)]:
            MeleeHost.p1.tilt_analog(
                melee.enums.Button.BUTTON_MAIN,
                i,
                0.5
            )
            # MeleeHost.p1.flush()
            gs = MeleeHost.console.step()
            print(gs.players[1].action, gs.players[1].action_frame)
            print(gs.players[1].position, gs.players[1].controller_state.main_stick)

    MeleeHost.console.stop()
    """


    """
    for _ in range(10):
        gs = MeleeHost.console.step()
        # print(gs.players[1].position)
        MeleeHost.p1.tilt_analog(melee.enums.Button.BUTTON_MAIN, 1.0, 0.5)
        MeleeHost.p1.flush()

    # Set the save state
    _ = MeleeHost.console.step()
    print("ATTEMPTING TO SAVE POSITION:")
    # MeleeHost.p1.simple_press(0, 0, melee.enums.Button.BUTTON_D_RIGHT)
    MeleeHost.p1.press_button(melee.enums.Button.BUTTON_D_RIGHT)
    MeleeHost.p1.flush()
    gs = MeleeHost.console.step()
    MeleeHost.p1.release_all()
    print(gs.frame, gs.players[1].position)

    # go run left
    print("MOVING!!! =====")
    for _ in range(10):
        gs = MeleeHost.console.step()
        print(gs.frame, gs.players[1].position)
        MeleeHost.p1.tilt_analog(melee.enums.Button.BUTTON_MAIN, 0.8, 0.5)
        MeleeHost.p1.flush()

    print("ATTEMPTING TO RESTORE POSITION")
    _ = MeleeHost.console.step()
    # MeleeHost.p1.simple_press(0, 0, melee.enums.Button.BUTTON_D_LEFT)
    MeleeHost.p1.press_button(melee.enums.Button.BUTTON_D_LEFT)
    MeleeHost.p1.flush()

    for _ in range(10):
        gs = MeleeHost.console.step()
        print(gs.frame, gs.players[1].position)

    import time

    t0 = time.time()

    for _ in range(1000):
        _ = MeleeHost.console.step()

    t_e = time.time() - t0  # seconds

    # one frame takes approx 0.0058 sec
    # we would expect 0.016 !!
    # with NO FFW code we still get 2.8x speedup?!

    breakpoint()

    # Position(x=np.float32(-42.0), y=np.float32(23.450098))
    """
