import dearpygui.dearpygui as dpg

def button_callback(sender, app_data, user_data):
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")

    dpg.add_button(label="b1?", callback = button_callback, parent=user_data)

def open_console(sender, app_data, user_data):
    console = melee.Console(path=relative_path)