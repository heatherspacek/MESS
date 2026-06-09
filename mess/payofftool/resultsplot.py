import dearpygui.dearpygui as dpg


class ResultsPlot:
    def __init__(self, init_w, init_h, parent=None, tag=None):
        # dpg.add_spacer(width=0, height=0, tag=tag)
        with dpg.drawlist(init_w, init_h, parent=parent) as self.drawlist:
            ...
        self.w = init_w
        self.h = init_h
        ResultsPlotRegistry.append(self)

    def update(self):
        """\
        needs to be updated in the main app drawing loop for mouse
        reactivity reasons.
        """
        print(dpg.get_drawing_mouse_pos())
        print(dpg.is_item_hovered(self.drawlist))

        dpg.delete_item(self.drawlist, children_only=True)
        dpg.draw_rectangle([0, 0], [self.w, self.h], parent=self.drawlist)


ResultsPlotRegistry = []
