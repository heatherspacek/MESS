import melee
from melee.gamestate import GameState
from melee.enums import Button
from .patcher import patch_installation
from ..data_structures.situation import Situation


class Host:
    """
    libmelee console host.

    API surface:
    =====
    .p1, .p2, .console: libmelee objects.

    .console_setup(): Start a fresh console relationship. Kill any stale
    .step(): melee.console.step, but with a timeout in case something
        has gone wrong with the console interface. Returns the GameState
    .situation_setup(): Takes a Situation dataclass and attempts to
        implement it. Returns the GameState
    """
    iso_path = "/home/heather/Documents/Disk Images/Super Smash Bros. Melee (v1.02).iso"

    def __init__(self):
        self.p1 = None
        self.p2 = None
        self.console = None

    def console_setup(self) -> GameState:
        """
        TODO: add statefulness, e.g., in case a connection was already
        open
        """
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

        return self.console.step()

    def situation_setup(self, sitch: Situation) -> GameState:
        # <Check if console_setup has occurred...>
        if self.console is None:
            raise RuntimeError("Console was never initialized.")
        if not self.console.connected:
            raise RuntimeError("Console reports that it is not connected.")
        self._load_into_game(sitch)
        self._set_percents(sitch)
        self._goto(sitch)

    def _load_into_game(self, sitch: Situation):
        MAX_STEPS = 250
        menuhelper = melee.menuhelper.MenuHelper()
        gs = self.console.step()

        for _ in range(MAX_STEPS):
            if gs.menu_state == melee.enums.Menu.IN_GAME:
                return gs
            else:
                menuhelper.menu_helper_simple(
                    gs,
                    self.p1,
                    sitch.p1_character,
                    sitch.stage,
                    costume=1,
                    autostart=True,
                    swag=False,
                )
                menuhelper.menu_helper_simple(
                    gs,
                    self.p2,
                    sitch.p2_character,
                    sitch.stage,
                    costume=2,
                    autostart=True,
                    swag=False
                )
                gs = self.console.step()
        # Ran out of iterations
        raise TimeoutError(f"Failed to start game within {MAX_STEPS} console steps.")

    def _set_percents(self, sitch: Situation):
        # self.console is assumed alive.
        def clamp(i: int):
            if i > 999:
                return 999
            elif i < 0:
                return 0
            else:
                return i
        p1_target = clamp(int(sitch.p1_percent))
        p2_target = clamp(int(sitch.p2_percent))
        # TODO: replace this with step-with-timeout, once it exists
        gs = self.console.step()
        p1_current = int(gs.players[1].percent)
        p2_current = int(gs.players[2].percent)
        if p1_current > p1_target or p2_current > p2_target:
            raise ValueError(
                "Target percent is lower than players' current percent."
                "Codeset doesn't support this right now. Try resetting "
                "the console."
            )
        while (p1_target != p1_current) or (p2_target != p2_current):
            if gs.frame % 2 == 0:
                self.p1.release_all()
                self.p2.release_all()
                gs = self.console.step()
                continue
            if (p1_target != p1_current):
                self.p1.press_button(Button.BUTTON_D_DOWN)
            if (p2_target != p2_current):
                self.p2.press_button(Button.BUTTON_D_DOWN)
            gs = self.console.step()
            p1_current = int(gs.players[1].percent)
            p2_current = int(gs.players[2].percent)
        return gs

    def _goto(self, sitch: Situation):
        ...

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
    MeleeHost.console_setup()

    for _ in range(500):
        # Advance time to make sure we're off the respawn plat.
        MeleeHost.console.step()

    from ..data_structures.situation import sample_situation
    s1 = sample_situation()

    MeleeHost.situation_setup(s1)

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
