import dearpygui.dearpygui as dpg

import numpy as np

import math

# Diverging color scale, picked from a Seaborn plot.
COLSCALE = [
    (63, 127, 147),
    (82, 139, 157),
    (108, 156, 171),
    (157, 188, 198),
    (222, 230, 233),
    (242, 239, 239),
    (234, 213, 209),
    (224, 183, 173),
    (217, 158, 143),
    (209, 132, 113),
    (199, 100, 74),
    (194, 85, 57),
]

def setup_fonts():
    if dpg.is_dearpygui_running():
        with dpg.font_registry():
            for fsize in [8, 12, 16, 20, 24, 32]:
                dpg.add_font(
                    "res/NotoSans-Regular.ttf",
                    fsize,
                    tag=f"default_font_{fsize}"
                )
            dpg.bind_font("default_font_16")
            dpg.set_global_font_scale(0.5)


class ResultsPlot:
    CELL_PADDING = 2
    def __init__(self, init_w, init_h, parent=None, tag=None):
        setup_fonts()
        with dpg.drawlist(init_w, init_h, parent=parent) as self.drawlist:
            pass
        self.w = init_w
        self.h = init_h
        self.data = None
        self._hovered = None
        self._selected = None
        self._data_w = None
        self._data_h = None
        self._x_params = None
        self._y_params = None
        ResultsPlotRegistry.append(self)

    def set_data(self, data_array: np.ndarray, parameters: list):
        if not isinstance(data_array, np.ndarray):
            raise TypeError("set_data expects an N-D numpy array.")
        
        # Determine the initial flattening of dimensions.
        if data_array.ndim >= 3:
            # Naive: mult the first N. Can improve on this later.
            data_array = data_array.reshape(
                math.prod(data_array.shape[0:-1]),
                data_array.shape[-1]
            )
        self._y_params = parameters[0:-1]
        self._x_params = parameters[-1:]

        self.data = data_array
        self._data_h = self.data.shape[0]
        self._data_w = self.data.shape[-1]

    def _plot_labels(self):
        ...

    def _calc_layout(self):
        """
        Cells layout:
        rowparam-name [...] |
                        1   |   data    data    data
                1        2   |   data    data    data
                        3   |
                        1   |
        1           


        """
        if self.data is None:
            # can silent pass here. this may be called in the draw loop
            return
        if dpg.get_text_size("foo", font="default_font_16") is None:
            # First frame always fails.
            return

        def fmt(tup):
            return f"{tup[1]}={tup[2][0]}"
        row_text_sizes = [
            dpg.get_text_size(fmt(tup), font="default_font_16")
            for tup in self._y_params
        ]
        col_text_sizes = [
            dpg.get_text_size(fmt(tup), font="default_font_16")
            for tup in self._x_params
        ]
        # needed_x = sum()

        breakpoint()
        return


    def update(self):
        """\
        needs to be updated in the main app drawing loop for mouse
        reactivity reasons. the main app drawing loop will run .update()
        of each RP registered in the module-glboal ResultsPlotRegistry.

        therefore, expect this once per frame.
        ** maybe we could only run this when the mouse position changes?
            lets save that change for an optimization pass :)
        """

        mouse_pos = (
            None
            if not dpg.is_item_hovered(self.drawlist)
            else dpg.get_drawing_mouse_pos()
        )

        dpg.delete_item(self.drawlist, children_only=True)
        # outer bounding rect
        dpg.draw_rectangle([0, 0], [self.w, self.h], parent=self.drawlist)
        if mouse_pos:
            dpg.draw_circle(mouse_pos, radius=5, parent=self.drawlist)
        
        TEST_STR = "sample string to test\nbounding rectangle"
        dpg.draw_text((27, 27), TEST_STR, parent=self.drawlist, size=20)
        tsize = dpg.get_text_size(TEST_STR, font="default_font_20")
        if tsize:
            dpg.draw_rectangle([27, 27], [27+tsize[0], 27+tsize[1]], parent=self.drawlist)
        self._calc_layout()



ResultsPlotRegistry = []
