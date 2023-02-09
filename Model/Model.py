from Analyzer.Analyzer import Analyzer
from ConnectionController import ConnectionController
import json


BASE_ADDRESS = "Data/Data.db"
with open("Model/Config/config.json", "r") as file:
    CONFIG = json.load(file)


class Model:
    def __init__(self):
        self.analyzer = Analyzer()
        self.connection_controller = ConnectionController()
        self.current_table = CONFIG["default_table_name"]
        if not self.is_there_table_name(CONFIG["default_table_name"]):
            self.create_table(table_name=CONFIG["default_table_name"])

    def process(self, text):
        result = self.analyzer.process(text)
        cursor = self.connection_controller.require_connection(BASE_ADDRESS)
        cursor.execute("""DELETE FROM :table_name;""",
                       {"table_name": self.current_table})
        for row in result:
            cursor.execute("""INSERT INTO :table_name
                              VALUES (:word, :normal_form, :part_of_speech, :gender, :number, :common_case,
                                      :sentence_part, :number_in_sentence, :number_of_sentence);""",
                           {**row, "table_name": self.current_table})
        self.connection_controller.drop_connection()

    def get_all_table_names(self):
        cursor = self.connection_controller.require_connection(BASE_ADDRESS)
        cursor.execute("""SELECT name
                          FROM sqlite_master;""")
        self.connection_controller.drop_connection()
        return tuple(item[0] for item in cursor.fetchall())

    def get_all_word_ids(self):
        cursor = self.connection_controller.require_connection(BASE_ADDRESS)
        cursor.execute("""SELECT word_id
                          FROM :table_name""",
                       {"table_name": self.current_table})
        self.connection_controller.drop_connection()
        return tuple(item[0] for item in cursor.fetchall())

    def is_there_table_name(self, table_name):
        return table_name in self.get_all_table_names()

    def is_there_word_id(self, word_id):
        return word_id in self.get_all_word_ids()

    def switch_table(self, **kwargs):
        self.current_table = kwargs["table_name"]

    def create_table(self, **kwargs):
        cursor = self.connection_controller.require_connection(BASE_ADDRESS)
        cursor.execute("""CREATE TABLE :table_name (
                          word_id INT PRIMARY KEY AUTO_INCREMENT,
                          word VARCHAR(30),
                          normal_form VARCHAR(30),
                          part_of_speech VARCHAR(30),
                          gender VARCHAR(30),
                          number VARCHAR(30),
                          common_case VARCHAR(30),
                          sentence_part VARCHAR(30),
                          number_in_sentence VARCHAR(30),
                          number_of_sentence VARCHAR(30)
                          );""",
                       kwargs)
        self.connection_controller.drop_connection()

    def delete_table(self, **kwargs):
        cursor = self.connection_controller.require_connection(BASE_ADDRESS)
        cursor.execute("""DROP TABLE :table_name;""",
                       kwargs)
        self.connection_controller.drop_connection()

    def get_row(self, **kwargs):
        cursor = self.connection_controller.require_connection(BASE_ADDRESS)
        cursor.execute("""SELECT word, normal_form, part_of_speech, gender, number, common_case,
                                 sentence_part, number_in_sentence, number_of_sentence
                          FROM :table_name
                          WHERE word_id = :row_number;""",
                       {"table_name": self.current_table, **kwargs})
        self.connection_controller.drop_connection()
        return cursor.fetchone()

    def get_table(self):
        cursor = self.connection_controller.require_connection(BASE_ADDRESS)
        cursor.execute("""SELECT word_id, word, normal_form, part_of_speech, gender, number,
                                 common_case, sentence_part, number_in_sentence, number_of_sentence
                          FROM :table_name;""",
                       {"table_name": self.current_table})
        self.connection_controller.drop_connection()
        return cursor.fetchall()

    def edit_row(self, **kwargs):
        cursor = self.connection_controller.require_connection(BASE_ADDRESS)
        cursor.execute("""UPDATE :table_name
                          SET normal_form = :normal_form,
                              part_of_speech = :part_of_speech,
                              gender = :gender,
                              number = :number,
                              common_case = :common_case,
                              sentence_part = :sentence_part
                          WHERE word_id = :word_id;""",
                       {"table_name": self.current_table, **kwargs})
        self.connection_controller.drop_connection()

    def insert_row(self, **kwargs):
        cursor = self.connection_controller.require_connection(BASE_ADDRESS)
        cursor.execute("""INSERT INTO :table_name
                          VALUES (:word, :normal_form, :part_of_speech, :gender, :number, :common_case,
                                  :sentence_part, :number_in_sentence, :number_of_sentence);""",
                       {"table_name":  self.current_table, **kwargs})
        self.connection_controller.drop_connection()

    def find_rows(self, **kwargs):
        cursor = self.connection_controller.require_connection(BASE_ADDRESS)
        cursor.execute("""SELECT word, normal_form, part_of_speech, gender, number, common_case,
                                 sentence_part, number_in_sentence, number_of_sentence
                          FROM :table_name
                          WHERE gender = :gender AND number = :number AND common_case = :common_case;
                          """,
                       {"table_name": self.current_table, **kwargs})
        self.connection_controller.drop_connection()


if __name__ == "__main__":
    pass
