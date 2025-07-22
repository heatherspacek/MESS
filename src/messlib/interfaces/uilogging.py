import logging
import dearpygui.dearpygui as dpg
from dearpygui_ext import logger


class MESSHandler(logging.Handler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        "necessary hack, or else is_dearpygui_running fails catastrophically"
        dpg.create_context()

    def emit(self, record):
        if dpg.is_dearpygui_running(): 
            if dpg.does_item_exist("logging_container"):
                # Log to the GUI window
                Logger_ref: logger.mvLogger = dpg.get_item_user_data("logging_container")
                if record.levelname == "ERROR":
                    Logger_ref.log_error(record.msg)
                elif record.levelname == "WARNING":
                    Logger_ref.log_warning(record.msg)
                elif record.levelname == "CRITICAL":
                    Logger_ref.log_critical(record.msg)
                elif record.levelname == "INFO":
                    Logger_ref.log_info(record.msg)
                elif record.levelname == "DEBUG":
                    Logger_ref.log_debug(record.msg)
                # TODO: add a formatter to the above..?
            if dpg.does_item_exist("status_bar_text") and record.levelname == "INFO":
                dpg.set_value("status_bar_text", record.msg)
        else:
            print(self.format(record))
