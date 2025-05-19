import dearpygui.dearpygui as dpg
import dearpygui_ext.logger as extlogger


def logging_window():
    with dpg.window(
        label="MESSAGE LOG",
        tag="logging_container",
        width=500,
        height=200,
        min_size=(300, 200),
        pos=(500, 300),
    ):
        Logger = extlogger.mvLogger(parent="logging_container")
        dpg.set_item_user_data("logging_container", Logger)
