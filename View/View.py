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
        self.main_layout.add_widget(self.data_table)
        self.main_layout.add_widget(back_button)
        self.add_widget(self.main_layout)

    def on_back_press(self, obj):
        self.manager.current = "WorkWithCurrentTableScreen"

    def update(self):
        self.data_table.row_data = self.manager.model.get_table()


class SearchRowsScreen(ViewAllRowsScreen):
    table_size = (0.9, 0.7)
    table_pos = {"center_x": 0.5, "center_y": 0.625}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gender_input = MDTextField(hint_text="Enter gender",
                                        size_hint=(.25, .1),
                                        pos_hint={"center_x": .2, "center_y": .2})
        self.number_input = MDTextField(hint_text="Enter number",
                                        size_hint=(.25, .1),
                                        pos_hint={"center_x": .5, "center_y": .2})
        self.common_case_input = MDTextField(hint_text="Enter common case",
                                             size_hint=(.25, .1),
                                             pos_hint={"center_x": .8, "center_y": .2})
        search_button = MDRoundFlatButton(text="Search",
                                          on_press=self.update,
                                          size_hint=(0.2, 0.1),
                                          pos_hint={"center_x": 0.85, "center_y": .08})
        self.main_layout.add_widget(self.gender_input)
        self.main_layout.add_widget(self.number_input)
        self.main_layout.add_widget(self.common_case_input)
        self.main_layout.add_widget(search_button)

    def update(self, obj):
        self.data_table.row_data = self.manager.model.find_rows(gender=self.gender_input.text,
                                                                number=self.number_input.text,
                                                                common_case=self.common_case_input.text)


class EditRowScreen(MDScreen):
    def on_ok_press(self, word_id, normal_form, part_of_speech, gender,
                    number, common_case, sentence_part):
        if not word_id.isdigit():
            return
        self.manager.model.edit_row(word_id=int(word_id),
                                    normal_form=normal_form,
                                    part_of_speech=part_of_speech,
                                    gender=gender,
                                    number=number,
                                    common_case=common_case,
                                    sentence_part=sentence_part)


class AddRowScreen(MDScreen):
    def on_ok_press(self, word, normal_form, part_of_speech, gender, number,
                    common_case, sentence_part, number_in_sentence, number_of_sentence):
        self.manager.model.insert_row(word=word,
                                      normal_form=normal_form,
                                      part_of_speech=part_of_speech,
                                      gender=gender,
                                      number=number,
                                      common_case=common_case,
                                      sentence_part=sentence_part,
                                      number_in_sentence=number_in_sentence,
                                      number_of_sentence=number_of_sentence)


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
        self.data = []
        s = AnchorLayout(anchor_x='center', anchor_y='bottom', pos_hint={'center_x': .5, 'center_y': .65})
        self.datatable = MDDataTable(
            size_hint=(1, 0.8),
            use_pagination=True,
            rows_num=13,
            column_data=[
                ("Grammeme", dp(140)),
                ("Value", dp(140))
            ],
            row_data=[
                (
                    "NOUN",
                    "имя существительное"
                ),
                (
                    "ADJF",
                    "имя прилагательное"
                ),
                (
                    "VERB",
                    "глагол(личная форма)"
                ),
                (
                    "INFN",
                    "глагол(инфинитив)"
                ),
                (
                    "PRTF",
                    "причастие"
                ),
                (
                    "GRND",
                    "деепричастие"
                ),
                (
                    "NUMR",
                    "числительное"
                ),
                (
                    "ADVB",
                    "наречие"
                ),
                (
                    "NPRO",
                    "местоимение"
                ),
                (
                    "PREP",
                    "предлог"
                ),
                (
                    "CONJ",
                    "союз"
                ),
                (
                    "PRCL",
                    "частица"
                ),
                (
                    "INTG",
                    "междометие"
                ),
                (
                    "nomn",
                    "именительный"
                ),
                (
                    "gent",
                    "родительный"
                ),
                (
                    "datv",
                    "дательный"
                ),
                (
                    "accs",
                    "винительный"
                ),
                (
                    "ablt",
                    "творительный"
                ),
                (
                    "loct",
                    "предложный"
                ),
                (
                    "sing",
                    "единственное число"
                ),
                (
                    "plur",
                    "множественное число"
                ),
                (
                    "femn",
                    "женский род"
                ),
                (
                    "masc",
                    "мужской род"
                ),
                (
                    "neut",
                    "средний род"
                ),
                (
                    "nsubj",
                    "подлежащее"
                ),
                (
                    "root",
                    "сказуемое"
                ),
                (
                    "amod, acl",
                    "определение"
                ),
                (
                    "obj",
                    "дополнение"
                ),
                (
                    "obl",
                    "обстоятельство"
                ),
                (
                    "conj",
                    "однородные члены предложения"
                )
            ]
        )
        s.add_widget(self.datatable)
        self.add_widget(s)


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
        sm.add_widget(EditRowScreen(name='EditRowScreen'))
        sm.add_widget(AddRowScreen(name='AddRowScreen'))
        sm.add_widget(WorkWithTablesScreen(name='WorkWithTablesScreen'))
        sm.add_widget(HelpScreen(name='HelpScreen'))
        return sm


if __name__ == "__main__":
    pass
