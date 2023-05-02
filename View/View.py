import os
import json
from kivy.config import Config
from kivy.uix.anchorlayout import AnchorLayout
Config.set("graphics", "resizable", 0)
Config.set("graphics", "width", 1280)
Config.set("graphics", "height", 720)
from kivy.lang import Builder
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp
from kivymd.app import MDApp
from Model.Model import Model


Builder.load_file(os.path.join(os.path.dirname(__file__), "Screens.kv"))
with open("Model/Config/config.json", "r") as file:
    CONFIG = json.load(file)


class GeneralScreen(MDScreen):
    pass


class AnalyzeScreen(MDScreen):
    def on_apply_analyze_press(self, file_name_check_active):
        if file_name_check_active:
            self.manager.model.file_process(self.ids.file_name.text)
        else:
            self.manager.model.process(self.ids.row_text.text)


class WorkWithCurrentTableScreen(MDScreen):
    def on_view_press(self):
        self.manager.updatable.update()
        self.manager.current = "ViewAllRowsScreen"


class ViewAllRowsScreen(MDScreen):
    table_size = (0.9, 0.8)
    table_pos = {"center_x": 0.5, "center_y": 0.55}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = MDFloatLayout()
        self.data_table = MDDataTable(use_pagination=True,
                                      column_data=[(column, dp(column_witdh)) for column,
                                                                                  column_witdh in zip(CONFIG["columns"],
                                                                                                      CONFIG["column_width"])],
                                      size_hint=self.table_size,
                                      rows_num=10,
                                      pos_hint=self.table_pos)
        back_button = MDRoundFlatButton(text="Back",
                                        on_press=self.on_back_press,
                                        size_hint=(0.2, 0.1),
                                        pos_hint={"center_x": 0.15, "center_y": .08})
        self.data_table.bind(on_row_press=self.on_row_press)
        self.main_layout.add_widget(self.data_table)
        self.main_layout.add_widget(back_button)
        self.add_widget(self.main_layout)

    def on_row_press(self, instance_table, instance_row):
        row_index = instance_row.range[0] // (instance_row.range[1] - instance_row.range[0] + 1)
        word_id = instance_table.row_data[row_index][0]
        self.manager.edit_screen.on_enter_fields_press(str(word_id))
        self.manager.current = "EditRowScreen"

    def on_back_press(self, obj):
        self.manager.current = "WorkWithCurrentTableScreen"

    def update(self):
        self.data_table.row_data = self.manager.model.get_table()


class SearchRowsScreen(ViewAllRowsScreen):
    table_size = (0.9, 0.7)
    table_pos = {"center_x": 0.5, "center_y": 0.625}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hypernyms_input = MDTextField(hint_text="Enter hypernym",
                                           size_hint=(.25, .1),
                                           pos_hint={"center_x": .2, "center_y": .2})
        self.hypernyms_input.bind(text=self.update)
        self.pos_synonyms_input = MDTextField(hint_text="Enter pos_synonyms",
                                              size_hint=(.25, .1),
                                              pos_hint={"center_x": .5, "center_y": .2})
        self.pos_synonyms.bind(text=self.update)
        self.related_input = MDTextField(hint_text="Enter related",
                                         size_hint=(.25, .1),
                                         pos_hint={"center_x": .8, "center_y": .2})
        self.related_input.bind(text=self.update)
        self.main_layout.add_widget(self.hypernyms_input)
        self.main_layout.add_widget(self.pos_synonyms_input)
        self.main_layout.add_widget(self.related_input)

    def update(self, *args):
        self.data_table.row_data = self.manager.model.find_rows(hypernyms=self.hypernyms_input.text,
                                                                pos_synonyms=self.pos_synonyms_input.text,
                                                                related=self.related_input.text)


class EditRowScreen(MDScreen):
    def on_ok_press(self, word_id, normal_form, classes, hypernyms, antonyms,
                    holonyms, meronyms, pos_synonyms, related, domain_items):
        if not word_id.isdigit():
            return
        self.manager.model.edit_row(word_id=int(word_id),
                                    normal_form=normal_form,
                                    classes=classes,
                                    hypernyms=hypernyms,
                                    antonyms=antonyms,
                                    holonyms=holonyms,
                                    meronyms=meronyms,
                                    pos_synonyms=pos_synonyms,
                                    related=related,
                                    domain_items=domain_items)

    def on_enter_fields_press(self, word_id):
        if word_id.isdigit() and self.manager.model.is_there_word_id(int(word_id)):
            fields = self.manager.model.get_row(True, word_id=int(word_id))
            for key in set.intersection(set(fields.keys()), set(self.ids.keys())):
                self.ids[key].text = str(fields[key]) if fields[key] is not None else CONFIG["none_default_word"]


class AddRowScreen(MDScreen):
    def on_ok_press(self, word, normal_form, classes, hypernyms, antonyms,
                    holonyms, meronyms, pos_synonyms, related, domain_items):
        self.manager.model.insert_row(word=word,
                                      normal_form=normal_form,
                                      classes=classes,
                                      hypernyms=hypernyms,
                                      antonyms=antonyms,
                                      holonyms=holonyms,
                                      meronyms=meronyms,
                                      pos_synonyms=pos_synonyms,
                                      related=related,
                                      domain_items=domain_items)


class WorkWithTablesScreen(MDScreen):
    def on_create_press(self, table_name):
        if not self.manager.model.is_there_table_name(table_name):
            self.manager.model.create_table(table_name=table_name)

    def on_delete_press(self, table_name):
        if self.manager.model.is_there_table_name(table_name) and table_name != CONFIG["default_table_name"]:
            self.manager.model.delete_table(table_name=table_name)
            self.manager.model.current_table = CONFIG["default_table_name"]
            self.refresh_table_name()

    def on_switch_press(self, table_name):
        if self.manager.model.is_there_table_name(table_name):
            self.manager.model.current_table = table_name
            self.refresh_table_name()

    def refresh_table_name(self):
        self.ids.table_name.text = self.manager.model.current_table


class HelpScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        s = AnchorLayout(anchor_x='center', anchor_y='bottom', pos_hint={'center_x': .5, 'center_y': .65})
        self.datatable = MDDataTable(
            size_hint=(1, 0.8),
            use_pagination=True,
            rows_num=13,
            column_data=[
                ("Function", dp(140)),
                ("Value description", dp(140))
            ],
            row_data=[
                (
                    "Syn",
                    "Синонимы"
                ),
                (
                    "Anti",
                    "Антонимы"
                ),
                (
                    "Der",
                    "Синтаксический дериват"
                ),
                (
                    "Gener",
                    "Обобщение"
                ),
                (
                    "Sing",
                    "Отдельный элемент множества"
                ),
                (
                    "Mult",
                    "Множество элемента"
                ),
                (
                    "Magn",
                    "Высокая степень интенсивности"
                ),
                (
                    "Ver",
                    "Соответствующий назначению, истинный"
                ),
                (
                    "Loc",
                    "Место, локализация"
                ),
                (
                    "Oper",
                    "Операция совершать"
                ),
                (
                    "Func",
                    "Функционирование"
                ),
                (
                    "Attr",
                    "Параметр"
                ),
                (
                    "Plus, Minus",
                    "Соответственно, 'более'/'менее'"
                ),
            ]
        )
        s.add_widget(self.datatable)
        self.add_widget(s)


class FilterRowsScreen(ViewAllRowsScreen):
    table_size = (0.9, 0.7)
    table_pos = {"center_x": 0.5, "center_y": 0.5}

    def update(self):
        self.data_table.row_data = self.manager.model.filter_rows(normal_form=self.ids.filter_input.text)


class BuildScreen(MDApp):
    def build(self):
        sm = MDScreenManager()
        sm.model = Model()
        sm.add_widget(GeneralScreen(name='GeneralScreen'))
        sm.add_widget(AnalyzeScreen(name='AnalyzeScreen'))
        sm.add_widget(WorkWithCurrentTableScreen(name='WorkWithCurrentTableScreen'))
        sm.updatable = ViewAllRowsScreen(name='ViewAllRowsScreen')
        sm.add_widget(sm.updatable)
        sm.add_widget(SearchRowsScreen(name='SearchRowsScreen'))
        sm.edit_screen = EditRowScreen(name='EditRowScreen')
        sm.add_widget(sm.edit_screen)
        sm.add_widget(FilterRowsScreen(name='FilterRowsScreen'))
        sm.add_widget(AddRowScreen(name='AddRowScreen'))
        sm.add_widget(WorkWithTablesScreen(name='WorkWithTablesScreen'))
        sm.add_widget(HelpScreen(name='HelpScreen'))
        return sm


if __name__ == "__main__":
    pass
