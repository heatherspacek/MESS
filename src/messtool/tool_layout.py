import dearpygui.dearpygui as dpg
import ctypes  # for Windows high-dpi text rendering "fuzziness" fix
import os  # for os.path.join and os.listdir

# --
from messtool.windows import (
    situation_editor,
    strategy_editor,
    game_setup,
    logging_window,
    )


def layout_setup():
    load_textures()
    window_themes()
    window_fonts()
    hidden_windows_setup()
    # Window 1- strategy editor
    strategy_editor.strategy_editor_window()
    # Window 2- situation editor
    situation_editor.situation_editor_window()
    # Window 3- game setup
    game_setup.game_setup_window()
    # Window 4- logging
    logging_window.logging_window()
    # "Window" 5- status bar
    with dpg.viewport_menu_bar():
        dpg.add_text(
            default_value="Welcome to MESS! Status messages will go here.",
            tag="status_bar_text"
            )
        dpg.add_spacer(width=150)
        with dpg.menu(label="View..."):
            dpg.add_menu_item(label="Reset all windows")

    dpg.create_viewport(title="MESS", width=1320, height=650)
    dpg.setup_dearpygui()

    if os.name == "nt":
        # Windows-specific "high-DPI" bugfix for blurry text.
        # before showing the viewport/calling `show_viewport`:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)

    dpg.show_viewport()


def hidden_windows_setup():
    dpg.add_file_dialog(
        directory_selector=False,
        show=False,
        tag="strategy_fileselect",
        file_count=1,
        width=500,
        height=400,
    )
    dpg.add_file_extension(".yaml", parent="strategy_fileselect")
    dpg.add_file_dialog(
        directory_selector=False,
        show=False,
        callback=None,
        tag="situation_fileselect",
        cancel_callback=None,
        width=500,
        height=400,
    )
    with dpg.window(
        label="[Placeholder Title]",
        modal=True,
        show=False,
        tag="modal_misc",
        no_title_bar=True,
    ):
        dpg.add_text("File load failed.", tag="model_misc_text")
        dpg.add_checkbox(label="Don't ask me next time")
        with dpg.group(horizontal=True):
            dpg.add_button(
                label="OK",
                width=75,
                callback=lambda: dpg.configure_item("modal_misc", show=False),
            )
            dpg.add_button(
                label="Cancel",
                width=75,
                callback=lambda: dpg.configure_item("modal_misc", show=False),
            )


def window_themes():
    with dpg.theme(tag="theme1"):
        with dpg.theme_component(dpg.mvCollapsingHeader):
            dpg.add_theme_color(dpg.mvThemeCol_Header, [98, 48, 67])
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, [119, 61, 84])
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, [119, 44, 74])
            dpg.add_theme_color(dpg.mvThemeCol_Text, [211, 211, 211])

    with dpg.theme(tag="theme2"):
        with dpg.theme_component(dpg.mvCollapsingHeader):
            dpg.add_theme_color(dpg.mvThemeCol_Header, [28, 48, 97])
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, [48, 61, 184])
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, [48, 44, 174])
            dpg.add_theme_color(dpg.mvThemeCol_Text, [211, 211, 211])


def window_fonts():
    with dpg.font_registry():
        # first argument ids the path to the .ttf or .otf file
        # TODO: this is fragile!!! only works right now because VS Code sets
        # a specific cwd. Look more later!
        dpg.add_font(
            os.path.join("res", "NotoSans-Regular.ttf"), 20, tag="default_font"
        )
        dpg.add_font(os.path.join("res", "NotoSans-Bold.ttf"), 20, tag="bold_font")

    dpg.bind_font("default_font")


def load_textures():
    for png in os.listdir(os.path.join("res", "stock_icons")):
        with dpg.texture_registry():
            (w, h, c, d) = dpg.load_image(os.path.join("res", "stock_icons", png))
            dpg.add_static_texture(
                width=w, height=h, default_value=d, tag=png.split(".")[0]
            )

    for png in os.listdir(os.path.join("res", "stages")):
        with dpg.texture_registry():
            (w, h, c, d) = dpg.load_image(os.path.join("res", "stages", png))
            dpg.add_static_texture(
                width=w, height=h, default_value=d, tag="stage_" + png.split(".")[0]
            )
