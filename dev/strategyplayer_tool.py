import dearpygui.dearpygui as dpg
import melee
import os
import ctypes
# - 
import strategyplayer_tool_callbacks as cbx

class ConsoleInterface():

    console = None

    def testfunc1(self, a,b,c):
        slippi_playback_path = os.path.join(os.environ["APPDATA"], "Slippi Launcher", "playback")
        console = melee.Console(path=slippi_playback_path)
        console.run()

if __name__ == "__main__":
        
    slippi_playback_path = os.path.join(os.environ["APPDATA"], "Slippi Launcher", "playback")
    console = melee.Console(path=slippi_playback_path)

    Interface = ConsoleInterface()

    dpg.create_context()

    #=====
    # the "start panel"...

    with dpg.window(label="START HERE") as top_level_wnd:
        dpg.set_item_width(top_level_wnd, 350)
        dpg.set_item_height(top_level_wnd, 350)
        with dpg.tab_bar():
            with dpg.tab(label="[1P, 1CPU] Play against a StrategyPlayer") as tab1:
                dpg.add_button(label="\nPlay against a\nStrategyPlayer\n")
                dpg.add_button(label="LAUNCH MELEE (test)", callback=Interface.testfunc1)
            with dpg.tab(label="[0P, 2CPU] Init two StrategyPlayers") as tab2:
                dpg.add_button(label="\nTest two\nStrategyPlayers\n")

    # user data and callback set when button is created
    dpg.add_button(label="Apply", callback=cbx.button_callback, user_data=tab1, parent=tab1)

    # user data and callback set any time after button has been created
    ##btn = dpg.add_button(label="Apply 2 \nmore lines", parent=group1)
    ##dpg.set_item_callback(btn, cbx.button_callback)
    ##dpg.set_item_user_data(btn, "Some Extra User Data")

    #===================

    # Viewport creation (the window)
    dpg.create_viewport(title='StrategyPlayer Invocation Tool', width=400, height=600)
    dpg.setup_dearpygui()

    '''
    dpg.add_font_registry()
    dpg.add_font("res/segoeui.ttf", 16)
    '''
    import dearpygui.demo as demo
    demo.show_demo()

    #dpg.show_font_manager()

    if os.name =='nt':
        # Windows-specific "high-DPI" bugfix for blurry text.
        # before showing the viewport/calling `dearpygui.dearpygui.show_viewport`:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)

    dpg.show_viewport()

    # below replaces start_dearpygui()
    while dpg.is_dearpygui_running():
        # insert here any code you would like to run in the render loop
        # you can manually stop by using stop_dearpygui()
        ###print("this will run every frame")
        dpg.render_dearpygui_frame()

    dpg.destroy_context()