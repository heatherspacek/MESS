import dearpygui.dearpygui as dpg
import numpy as np

from ..resultsplot import ResultsPlot, ResultsPlotRegistry

plot_data_1 = np.array([
    [
        [1, 3, 3, 3],
        [1, 3, 3, 3],
    ],
    [
        [0, 1, 1, 1],
        [1, 1, 1, 2],
    ],
    [
        [3, 2, 2, 3],
        [3, 3, 3, 3],
    ],
])

# real data doesnt quite assume this form yet, but it's the most
# condensed form i think we can do?
parameters_data_1 = [
    ("p1", "slack_frames", [6, 7, 8]),
    ("p1", "ff_frame", [1, 2]),
    ("p2", "frames_dashing", [2, 3, 4, 5]),
]


if __name__ == "__main__":
    dpg.create_context()
    dpg.create_viewport(title="Dev: Results Plot", width=700, height=550)
    dpg.setup_dearpygui()
    dpg.show_viewport()

    with dpg.window(pos=(0,0)) as win:
        RP = ResultsPlot(300, 300, parent=win)

    RP.set_data(data_array=plot_data_1, parameters=parameters_data_1)

    while dpg.is_dearpygui_running():
        for rxx in ResultsPlotRegistry:
            rxx.update()
        dpg.render_dearpygui_frame()
    dpg.destroy_context()