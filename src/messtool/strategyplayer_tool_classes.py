import dearpygui.dearpygui as dpg
# -
import messtool.strategyplayer_tool_templates as tp8
from messlib.classes_abstract import Strategy

import pdb

# get_value and set_value work on all dpg ui items, apparently.
# delete_item() can do runtime deletion. (container AND children!)


class GuiController:

    # Exposes callables for UI elements that will make changes to the Strategy.
    # User input -> a button in the View -> GuiController -> ...
    #   changes to the Model -> the View retrieves the changes from the Model.

    strat_name_ref: int = None
    character_combo_ref: int = None
    # --
    triggers_group_ref: int = None
    actions_group_ref: int = None
    # --
    loaded_strategy: Strategy | None = None

    def update_view(self):
        # Function to consult the Model
        # we registered key elements of the View into GuiController already

        # 1. delete everything
        dpg.delete_item(self.triggers_group_ref, children_only=True)
        print(self.loaded_strategy.triggers)
        # 2. consult the model and re-add all of them
        for i, tr in enumerate(self.loaded_strategy.triggers):
            tp8.trigger_template(
                GuiController=self,
                label="trigger#"+str(i),
                parent=self.triggers_group_ref,
                trigger=tr
            )

    def add_trigger(self):
        if self.loaded_strategy is None:
            raise RuntimeWarning("GuiController missing a loaded_strategy.")

        # Model: add a Trigger
        (trigger_ref, _) = self.loaded_strategy.add_new_trigger()

        # Send a signal to the View suggesting that it should update (look
        # at the Model!)
        self.update_view()
        # # View: add the corresponding "template" underneath the header
        # tp8_ref = tp8.trigger_template(parent=self.triggers_header_ref,
        #                                GuiController=self)
        # n = str(len(self.loaded_strategy.triggers))
        # dpg.set_item_label(tp8_ref, "Trigger #"+n)

    def delete_trigger(self, sender, value, user_data):
        # The "sender" is the button, for which we can do "parent-of-parent"...
        # But seems fragile.
        #####
        # BIG TODO: rework this to instead delete from the Model!

        trigger_header = dpg.get_item_parent(dpg.get_item_parent(sender))
        matching_trigger_ref = None
        for uik, uie in zip(self.ui_references, self.ui_references.values()):
            if uie.id == trigger_header:
                matching_trigger_ref = uie.trigger_ref
                # Registry: delete the co-entry.
                self.ui_references.pop(uik)
                break

        if matching_trigger_ref is None:
            raise RuntimeError("clicked delete button, but couldnt find " +
                               "the correct associated trigger")

        # Model: tell the Strategy to delete the appropriate Trigger.
        self.loaded_strategy.delete_trigger_by_reference(matching_trigger_ref)

        # View: delete the header.
        dpg.delete_item(trigger_header)

    def trigger_type_select(self, sender, value, user_data):

        pdb.set_trace()
        # Update the model. Trigger object is in user_data
        self.loaded_strategy.change_trigger_type(
            trigger_ref=user_data,
            new_type_string=value
            )
        self.update_view()


    ####
    # Serialization

    def load_strategy_from_file(self):
        pass

    def save_strategy_to_file(self):
        pass

    ####
    # View-only

    def collapse_all(self):
        pass

    def expand_all(self):
        pass
