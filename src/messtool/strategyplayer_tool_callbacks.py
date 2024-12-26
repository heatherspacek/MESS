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


'''
def callback_add_trigger(sender, app_data, user_data):
    # Add to the data structure and the app at the same time.
    # Also, give the app component a reference (so that deletion is elegant).

    # dev note: user_data will hold the strategyplayer

    # *** this section is broken, but is being replaced imminently with MVC
    # restructure.
    user_data.add_trigger(new_trigger)

    tp8.trigger_template(
        parent=dpg.get_item_parent(sender),
        trigger=new_trigger,
        n=len(user_data.loaded_strategy.triggers)+1
        )
'''


def callback_delete_trigger(sender, app_data, user_data):
    # delete the app elements,
    # and delete (list.remove()) the trigger from the Strategy
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")


def set_trigger_type(sender, app_data, user_data):
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")


def save_strategy(strategy: Strategy, path: str):
    with open(path) as filestream:
        yaml.safe_dump(strategy, filestream)


def load_strategy(path: str) -> Strategy:
    yaml.safe_load()
