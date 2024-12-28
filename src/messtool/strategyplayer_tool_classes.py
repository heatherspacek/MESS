from collections import namedtuple
import dearpygui.dearpygui as dpg

import messtool.strategyplayer_tool_templates as tp8

UIEntry = namedtuple("UIEntry", "name, id, update_signature")

# get_value and set_value work on all dpg ui items, apparently.


class GuiController:

    ui_references = {}
    triggers_header_ref = None
    actions_header_ref = None
    sp2 = None

    def add_ui_entries(self, *entry_pairs):
        for name, tag in entry_pairs:
            # type = dpg.get_item_info(tag)['type']
            # config = dpg.get_item_configuration(d)
            # value = dpg.get_value(tag)
            new_entry = UIEntry(
                name=name,
                id=tag,
                update_signature=()
                )
            self.ui_references[name] = new_entry
        print(self.ui_references)

    def update_ui_elements(self):
        for uie_key in self.ui_references:
            pass
            # Retaining this as a **demo, but it might not be the best model.
            # dpg.configure_item(entry.id, **uie.update_signature)

    def add_trigger(self):
        if self.triggers_header_ref is not None:
            # add the corresponding "template" underneath it
            tp8_ref = tp8.trigger_template(parent=self.triggers_header_ref)
            n_triggers_so_far = len(self.sp2.loaded_strategy.triggers)
            self.add_ui_entries(
                ("trigger_" + str(1+n_triggers_so_far), tp8_ref)
                )

    def delete_trigger(self, ui_id):
        pass

    def load_strategy_from_file(self):
        pass

    def save_strategy_to_file(self):
        pass
