import dearpygui.dearpygui as dpg
# -
import messtool.strategyplayer_tool_templates as tp8
from messlib.classes_abstract import Strategy

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
    responses_group_ref: int = None
    # --
    loaded_strategy: Strategy | None = None

    def update_view(self):
        # Function to consult the Model
        # we registered key elements of the View into GuiController already

        # 1. delete everything
        dpg.delete_item(self.triggers_group_ref, children_only=True)
        dpg.delete_item(self.responses_group_ref, children_only=True)
        print(self.loaded_strategy.triggers)
        print(self.loaded_strategy.responses)
        # 2. consult the model and re-add all of them
        for i, tr in enumerate(self.loaded_strategy.triggers):
            tp8.trigger_template(
                GuiController=self,
                label="trigger #"+str(i),
                parent=self.triggers_group_ref,
                trigger=tr
            )
        for i, re in enumerate(self.loaded_strategy.responses):
            tp8.response_template(
                GuiController=self,
                label="response #"+str(i),
                parent=self.responses_group_ref,
                response=re
            )

    def add_trigger(self):
        if self.loaded_strategy is None:
            raise RuntimeWarning("GuiController missing a loaded_strategy.")

        self.loaded_strategy.add_new_trigger()
        self.update_view()

    def delete_trigger(self, sender, value, user_data):
        if self.loaded_strategy is None:
            raise RuntimeWarning("GuiController missing a loaded_strategy.")

        self.loaded_strategy.delete_trigger_by_reference(user_data)
        self.update_view()

    def trigger_type_select(self, sender, value, user_data):
        # Update the model. Trigger object is in user_data
        self.loaded_strategy.change_trigger_type(
            trigger_ref=user_data,
            new_type_string=value
            )
        self.update_view()

    def add_response(self, sender, value, user_data):
        self.loaded_strategy.add_new_response()
        self.update_view()

    def delete_response(self, sender, value, user_data):
        self.loaded_strategy.delete_response_by_reference(user_data)
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
