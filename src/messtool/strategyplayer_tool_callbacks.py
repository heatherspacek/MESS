import dearpygui.dearpygui as dpg
import yaml  # serialization of `Strategy`s`
import os
from messlib.classes_abstract import Strategy, Trigger
from messlib.serialization import strat2dict, dict2strat
import messtool.strategyplayer_tool_templates as tp8


def callback_TEST(sender, app_data, user_data):
    interface = dpg.get_item_user_data("holder0")
    player2 = dpg.get_item_user_data("holder2")

    player2.connect_controller(interface.controller2)
    player2.controller.connect()


def callback_strategy_import(sender, app_data, user_data):
    dpg.show_item("strategy_fileselect")
    dpg.configure_item("strategy_fileselect",
                       callback=callback_strategy_load_ok,
                       cancel_callback=callback_strategy_load_cancel
                       )


def callback_strategy_export(sender, app_data, user_data):
    dpg.show_item("strategy_fileselect")
    dpg.configure_item("strategy_fileselect",
                       callback=callback_strategy_save_ok,
                       cancel_callback=callback_strategy_save_cancel
                       )


def callback_strategy_load_ok(sender, app_data, user_data):
    path_to_try_loading = os.path.join(
        app_data['file_path_name']
    )
    try:
        print(path_to_try_loading)
        with open(path_to_try_loading) as fstream:
            strategy_dict = yaml.safe_load(fstream)
            print(strategy_dict)
            print(dict2strat(strategy_dict))

            # player1 = dpg.get_item_user_data("load_strategy_button")
            # player1.loaded_strategy = Dict2Strat(strategy_dict)
    except FileNotFoundError:
        # user_data should be a reference to the main window
        # check out simple module for details
        dpg.configure_item("modal_misc", show=True)
        print("(No file selected.)")


def callback_strategy_load_cancel(sender, app_data, user_data):
    pass


def callback_strategy_save_ok(sender, app_data, user_data):
    print("save-ok")
    with open(app_data['file_path_name'], 'w') as wstream:
        strategyplayer = dpg.get_item_user_data("importantbutton")
        strategy_dict = strat2dict(strategyplayer.loaded_strategy)
        print(strategy_dict)
        yaml.safe_dump(strategy_dict, wstream)


def callback_strategy_save_cancel(sender, app_data, user_data):
    print("save-cancel")


def callback_situation_load_ok(sender, app_data, user_data):
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")


def callback_situation_load_cancel(sender, app_data, user_data):
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")


def callback_delete_trigger(sender, app_data, user_data):
    # delete the app elements,
    # and delete (list.remove()) the trigger from the Strategy
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")


def callback_trigger_type_select(sender, value, user_data):
    # Based on box selection, change the state of the template
    # ...and also change the underlying Trigger object.
    sender_header_id = str(
            dpg.get_item_parent(dpg.get_item_parent(sender))
        )

    if value == "TimeTrigger":
        dpg.configure_item("timegroup_"+sender_header_id, show=True)
        dpg.configure_item("distgroup_"+sender_header_id, show=False)
        dpg.configure_item("actiongroup_"+sender_header_id, show=False)
    elif value == "DistanceTrigger":
        dpg.configure_item("timegroup_"+sender_header_id, show=False)
        dpg.configure_item("distgroup_"+sender_header_id, show=True)
        dpg.configure_item("actiongroup_"+sender_header_id, show=False)
    elif value == "ActionTrigger":
        dpg.configure_item("timegroup_"+sender_header_id, show=False)
        dpg.configure_item("distgroup_"+sender_header_id, show=False)
        dpg.configure_item("actiongroup_"+sender_header_id, show=True)
    else:
        pass


def set_trigger_type(sender, app_data, user_data):
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")


def save_strategy(strategy: Strategy, path: str):
    with open(path) as filestream:
        yaml.safe_dump(strategy, filestream)


def load_strategy(path: str) -> Strategy:
    yaml.safe_load()
