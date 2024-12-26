from collections import namedtuple
import dearpygui.dearpygui as dpg

import messtool.strategyplayer_tool_templates as tp8

UIEntry = namedtuple("UIEntry", "name, id, update_signature")

# get_value and set_value work on all dpg ui items, apparently.


class GuiController:

    ui_references = []
    triggers_header_ref = None
    actions_header_ref = None

    def add_ui_entries(self, names, dpg_tags):
        for name, tag in zip(names, dpg_tags):
            type = dpg.get_item_info(tag)['type']
            # config = dpg.get_item_configuration(d)
            # value = dpg.get_value(tag)
            new_entry = UIEntry(
                name=name,
                id=tag,
                update_signature=self.get_ui_update_signature(type)
                )
            self.ui_references.append(new_entry)

    def get_ui_update_signature(self, type: str):
        match type:
            case 'mvAppItemType::mvInputText':
                return {'default_value': None}
            case 'mvAppItemType::mvCombo':
                return {'items': None}
            case _:
                raise NotImplementedError

    def update_ui_elements(self):
        for uie in self.ui_references:
            # Retaining this as a **demo, but it might not be the best model.
            dpg.configure_item(uie.id, **uie.update_signature)

    def add_trigger(self):
        if self.triggers_header_ref is not None:
            # add the corresponding "template" underneath it
            tp8.trigger_template(parent=self.triggers_header_ref)

    def load_strategy_from_file(self):
        pass

    def save_strategy_to_file(self):
        pass
