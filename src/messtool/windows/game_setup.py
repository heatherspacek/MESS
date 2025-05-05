import dearpygui.dearpygui as dpg

from messlib.console_interface import Interface
# from messtool.singletons import GuiController


def game_setup_window():
    with dpg.window(
        label="---",
        tag="gamewnd",
        width=300,
        height=400,
        min_size=(300, 400),
        pos=(500, 25),
    ):
        dpg.add_text(
            """Welcome to MESS!
To get started, load a strategy or situation from file,
or start editing your own!"""
        )
        dpg.add_separator()
        dpg.add_image("zelda")

        with dpg.group(horizontal=True):
            with dpg.group():
                # P1
                dpg.add_image("placeholder")
                dpg.add_combo(
                    ["strategyplayer", "human input"],
                    default_value="strategyplayer",
                    width=135,
                )

                dpg.add_text("[No strategy loaded.]", tag="status_p1")
            with dpg.group():
                # P2
                dpg.add_image("placeholder")
                dpg.add_combo(
                    ["strategyplayer"], default_value="strategyplayer", width=135
                )

                dpg.add_text("[No strategy loaded.]", tag="status_p2")

        # Make this button say "start analysis" when in SP vs SP mode.
        dpg.add_button(label="Start game", tag="startbutton",
                       callback=Interface.setup_oneplayer)
