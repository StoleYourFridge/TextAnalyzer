import os
import json
from kivy.config import Config
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


Builder.load_file(os.path.join(os.path.dirname(__file__), "Screens.kv"))
with open("../Model/Config/config.json", "r") as file:
    CONFIG = json.load(file)


class GeneralScreen(MDScreen):
    pass


class AnalyzeScreen(MDScreen):
    pass


class ViewAllRowsScreen(MDScreen):
    table_size = (0.9, 0.8)
    table_pos = {"center_x": 0.5, "center_y": 0.55}

    def __init__(self):
        super().__init__()
        self.main_layout = MDFloatLayout()
        self.data_table = MDDataTable(use_pagination=True,
                                      column_data=[(column, dp(column_witdh)) for column,
                                                                                  column_witdh in zip(CONFIG["columns"],
                                                                                                      CONFIG["column_width"])],
                                      size_hint=self.table_size,
                                      pos_hint=self.table_pos)
        back_button = MDRoundFlatButton(text="Back",
                                        on_press=self.on_back_press,
                                        size_hint=(0.2, 0.1),
                                        pos_hint={"center_x": 0.15, "center_y": .08})
        self.main_layout.add_widget(self.data_table)
        self.main_layout.add_widget(back_button)
        self.add_widget(self.main_layout)

    def on_back_press(self):
        pass

    def update(self):
        pass


class SearchScreen(ViewAllRowsScreen):
    table_size = (0.9, 0.7)
    table_pos = {"center_x": 0.5, "center_y": 0.625}

    def __init__(self):
        super().__init__()
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

    def update(self):
        pass


class Manager(MDScreenManager):
    pass


class MyApp(MDApp):
    def build(self):
        return SearchScreen()


if __name__ == "__main__":
    app = MyApp()
    app.run()
