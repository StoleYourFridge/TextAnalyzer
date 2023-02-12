from Analyzer.Analyzer import Analyzer
from Model.ConnectionController import ConnectionController
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
        cursor.execute(f"""DELETE FROM {self.current_table};""")
        cursor.executemany(f"""INSERT INTO {self.current_table}
                                      (word, normal_form, part_of_speech, gender, number, common_case,
                                       sentence_part, number_in_sentence, number_of_sentence)
                               VALUES (:word, :normal_form, :part_of_speech, :gender, :number, :common_case,
                                       :sentence_part, :number_in_sentence, :number_of_sentence);""",
                           result)
        self.connection_controller.drop_connection()

    def file_process(self, filename):
        with open(f"TestFiles/{filename}", "r") as file:
            text = file.read()
            self.process(text)

    def get_all_table_names(self):
        cursor = self.connection_controller.require_connection(BASE_ADDRESS)
        cursor.execute("""SELECT name
                          FROM sqlite_master;""")
        result = tuple(item[0] for item in cursor.fetchall())
        self.connection_controller.drop_connection()
        return result

    def get_all_word_ids(self):
        cursor = self.connection_controller.require_connection(BASE_ADDRESS)
        cursor.execute(f"""SELECT word_id
                           FROM {self.current_table}""")
        result = tuple(item[0] for item in cursor.fetchall())
        self.connection_controller.drop_connection()
        return result

    def is_there_table_name(self, table_name):
        return table_name in self.get_all_table_names()

    def is_there_word_id(self, word_id):
        return word_id in self.get_all_word_ids()

    def switch_table(self, **kwargs):
        self.current_table = kwargs["table_name"]

    def create_table(self, **kwargs):
        cursor = self.connection_controller.require_connection(BASE_ADDRESS)
        cursor.execute(f"""CREATE TABLE {kwargs["table_name"]} (
                           word_id INTEGER PRIMARY KEY ,
                           word VARCHAR(30),
                           normal_form VARCHAR(30),
                           part_of_speech VARCHAR(30),
                           gender VARCHAR(30),
                           number VARCHAR(30),
                           common_case VARCHAR(30),
                           sentence_part VARCHAR(30),
                           number_in_sentence VARCHAR(30),
                           number_of_sentence VARCHAR(30)
                           );""")
        self.connection_controller.drop_connection()

    def delete_table(self, **kwargs):
        cursor = self.connection_controller.require_connection(BASE_ADDRESS)
        cursor.execute(f"""DROP TABLE {kwargs["table_name"]};""")
        self.connection_controller.drop_connection()

    def get_row(self, is_dict, **kwargs):
        cursor = self.connection_controller.require_connection(BASE_ADDRESS)
        self.disable_none(kwargs)
        cursor.execute(f"""SELECT word_id, word, normal_form, part_of_speech, gender, number, 
                                  common_case, sentence_part, number_in_sentence, number_of_sentence
                           FROM {self.current_table}
                           WHERE word_id = :word_id;""",
                       kwargs)
        result = cursor.fetchone()
        if is_dict:
            result = {key: value for key, value in zip(CONFIG["columns"], result)}
        self.connection_controller.drop_connection()
        return result

    def get_table(self):
        cursor = self.connection_controller.require_connection(BASE_ADDRESS)
        cursor.execute(f"""SELECT word_id, word, normal_form, part_of_speech, gender, number,
                                  common_case, sentence_part, number_in_sentence, number_of_sentence
                           FROM {self.current_table}
                           ORDER BY word ASC;""")
        result = cursor.fetchall()
        self.connection_controller.drop_connection()
        return result

    def edit_row(self, **kwargs):
        cursor = self.connection_controller.require_connection(BASE_ADDRESS)
        self.disable_none(kwargs)
        cursor.execute(f"""UPDATE {self.current_table}
                           SET normal_form = :normal_form,
                               part_of_speech = :part_of_speech,
                               gender = :gender,
                               number = :number,
                               common_case = :common_case,
                               sentence_part = :sentence_part
                           WHERE word_id = :word_id;""",
                       kwargs)
        self.connection_controller.drop_connection()

    def insert_row(self, **kwargs):
        cursor = self.connection_controller.require_connection(BASE_ADDRESS)
        self.disable_none(kwargs)
        cursor.execute(f"""INSERT INTO {self.current_table}
                                  (word, normal_form, part_of_speech, gender, number, common_case,
                                   sentence_part, number_in_sentence, number_of_sentence)
                           VALUES (:word, :normal_form, :part_of_speech, :gender, :number, :common_case,
                                   :sentence_part, :number_in_sentence, :number_of_sentence);""",
                       kwargs)
        self.connection_controller.drop_connection()

    def find_rows(self, **kwargs):
        cursor = self.connection_controller.require_connection(BASE_ADDRESS)
        kwargs = {key: value + "%" for key, value in kwargs.items()}
        cursor.execute(f"""SELECT word_id, word, normal_form, part_of_speech, gender, number,
                                  common_case, sentence_part, number_in_sentence, number_of_sentence
                           FROM {self.current_table}
                           WHERE gender LIKE :gender AND number LIKE :number AND common_case LIKE :common_case
                           ORDER BY word ASC;
                          """,
                       kwargs)
        self.disable_none(kwargs)
        result = cursor.fetchall()
        self.connection_controller.drop_connection()
        return result

    def filter_rows(self, **kwargs):
        cursor = self.connection_controller.require_connection(BASE_ADDRESS)
        kwargs["normal_form"] = f'{kwargs["normal_form"]}%'
        cursor.execute(f"""SELECT word_id, word, normal_form, part_of_speech, gender, number, 
                                  common_case, sentence_part, number_in_sentence, number_of_sentence
                           FROM {self.current_table}
                           WHERE normal_form LIKE :normal_form
                           ORDER BY word ASC;
                          """,
                       kwargs)
        result = cursor.fetchall()
        self.connection_controller.drop_connection()
        return result

    @staticmethod
    def disable_none(dictionary):
        for key, value in dictionary.items():
            if dictionary[key] == CONFIG["none_default_word"]:
                dictionary[key] = None


if __name__ == "__main__":
    pass
