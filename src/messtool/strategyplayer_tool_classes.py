import dearpygui.dearpygui as dpg
# -
from dataclasses import dataclass
# -
import messtool.strategyplayer_tool_templates as tp8


@dataclass
class UIEntry:
    name: str
    id: int


@dataclass
class UIEntryTrigger(UIEntry):
    trigger_ref: any  # well not ANY but im lazyyy
    trigger_index: int


# get_value and set_value work on all dpg ui items, apparently.
# delete_item() can do runtime deletion. (container AND children!)


class GuiController:

    # this table should co-register Model items (e.g. trigger N) against
    # the associated Strategy elements
    ui_references = {}
    triggers_header_ref = None
    actions_header_ref = None
    loaded_strategy = None  # TODO: make this type-hint Strategy

    def register_ui_reference(self, name, id):
        self.ui_references[name] = UIEntry(name=name, id=id)

    def add_trigger(self):
        if (self.triggers_header_ref is None) or (
                self.loaded_strategy is None):
            raise RuntimeWarning(
                "GuiController missing something for add_trigger. " +
                "Likely unintended behaviour")

        # Model: add a Trigger
        (trigger_ref, _) = self.loaded_strategy.add_new_trigger()

        # View: add the corresponding "template" underneath the header
        tp8_ref = tp8.trigger_template(parent=self.triggers_header_ref,
                                       GuiController=self)
        n = str(len(self.loaded_strategy.triggers))
        dpg.set_item_label(tp8_ref, "Trigger #"+n)

        # Co-register them.
        self.ui_references["trigger_"+n] = UIEntryTrigger(
            name="trigger_"+n,
            id=tp8_ref,
            trigger_ref=trigger_ref
            )

        print(self.loaded_strategy)
        print(self.ui_references)

    def delete_trigger(self, sender, value, user_data):
        # The "sender" is the button, for which we can do "parent-of-parent"...
        # But seems fragile.
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
        # TODO: make the header names update?!

    def trigger_type_select(self, sender, value, user_data):
        # Based on box selection, change the state of the template
        # ...and also change the underlying Trigger object.
        sender_header_id = str(
                dpg.get_item_parent(dpg.get_item_parent(sender))
            )

        if value == "TimeTrigger":
            dpg.configure_item("timegroup_"+sender_header_id, show=True)
            dpg.configure_item("distgroup_"+sender_header_id, show=False)
            dpg.configure_item("actiongroup_"+sender_header_id, show=False)
            dpg.configure_item("responseselect_"+sender_header_id, show=True)
        elif value == "DistanceTrigger":
            dpg.configure_item("timegroup_"+sender_header_id, show=False)
            dpg.configure_item("distgroup_"+sender_header_id, show=True)
            dpg.configure_item("actiongroup_"+sender_header_id, show=False)
            dpg.configure_item("responseselect_"+sender_header_id, show=True)
        elif value == "ActionTrigger":
            dpg.configure_item("timegroup_"+sender_header_id, show=False)
            dpg.configure_item("distgroup_"+sender_header_id, show=False)
            dpg.configure_item("actiongroup_"+sender_header_id, show=True)
            dpg.configure_item("responseselect_"+sender_header_id, show=True)
        else:
            pass

    ####
    # Synchronization
    def pull_values(self):
        pass

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
