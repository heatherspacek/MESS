import dearpygui.dearpygui as dpg
import yaml  # safe(-ish) serialization of `Strategy`s`
from MESSabstract import Strategy


def button_callback(sender, app_data, user_data):
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")

    dpg.add_button(label="b1?", callback=button_callback, parent=user_data)


def callback_add_trigger(sender, app_data, user_data):
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")


def save_strategy(strategy: Strategy, path: str):
    with open(path) as filestream:
        yaml.safe_dump(strategy, filestream)


def load_strategy(path: str) -> Strategy:
    yaml.safe_load
