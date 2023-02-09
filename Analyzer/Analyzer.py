from nltk.tokenize import sent_tokenize
import pymorphy2
import spacy
import re


class Analyzer:
    def __init__(self):
        pass

    @staticmethod
    def text_into_sentences(text):
        sentences = sent_tokenize(text)
        return sentences

    @staticmethod
    def sentences_into_words(sentences):
        storage = list()
        for index in range(len(sentences)):
            words_in_sentence = re.findall('\w[\w-]*', sentences[index], flags=re.IGNORECASE)
            storage.append(words_in_sentence)
        return storage

    @staticmethod
    def words_morphological_features(storage_of_words):
        morph = pymorphy2.MorphAnalyzer()
        morphological_features_list = list()
        for first_index in range(len(storage_of_words)):
            for second_index in range(len(storage_of_words[first_index])):
                if not (morph.parse(storage_of_words[first_index][second_index])[0].tag.POS == "PREP" or
                        morph.parse(storage_of_words[first_index][second_index])[0].tag.POS == "CONJ" or
                        morph.parse(storage_of_words[first_index][second_index])[0].tag.POS == "ADVB"):
                    morphological_features_list.append([storage_of_words[first_index][second_index],#вывод самого слова
                                   morph.parse(storage_of_words[first_index][second_index])[0].normal_form, #начальная форма
                                   morph.parse(storage_of_words[first_index][second_index])[0].tag.POS,#часть речи
                                   morph.parse(storage_of_words[first_index][second_index])[0].tag.case,#падеж
                                   morph.parse(storage_of_words[first_index][second_index])[0].tag.number,#число
                                   morph.parse(storage_of_words[first_index][second_index])[0].tag.gender,#род
                                   second_index + 1,#номер слова в предложении
                                   first_index + 1])#номер предложения
        return morphological_features_list

    @staticmethod
    def syntactic_role(text):
        nlp = spacy.load("ru_core_news_sm")
        storage_of_words = nlp(text)
        syntactic_role_storage = list()
        syntactic_role_storage_without_trash = list()
        for token in storage_of_words:
            syntactic_role_storage.append([token.text, token.dep_])
        for index in range(len(syntactic_role_storage)):
            if not (syntactic_role_storage[index][1] == "punct" or
                    syntactic_role_storage[index][1] == "case" or
                    syntactic_role_storage[index][1] == "advmod" or
                    syntactic_role_storage[index][1] == "cc"):
                syntactic_role_storage_without_trash.append(syntactic_role_storage[index])
        return syntactic_role_storage_without_trash

    @staticmethod
    def dictionary_with_all_forms_of_words(text):
        dictionary_list = list()
        sentences = Analyzer.text_into_sentences(text)
        storage_of_words = Analyzer.sentences_into_words(sentences)
        morphological_features_storage = Analyzer.words_morphological_features(storage_of_words)
        syntactic_role_without_trash_storage = Analyzer.syntactic_role(text)
        for i in range(len(morphological_features_storage)):
            for j in range(len(syntactic_role_without_trash_storage)):
                if morphological_features_storage[i][0] == syntactic_role_without_trash_storage[j][0]:
                    morphological_features_storage[i].append(syntactic_role_without_trash_storage[j][1])
            dictionary_list.append(
                dict({"word": morphological_features_storage[i][0].lower(),
                      "normal_form": morphological_features_storage[i][1],
                      "part_of_speech": morphological_features_storage[i][2],
                      "gender": morphological_features_storage[i][5],
                      "number": morphological_features_storage[i][4],
                      "common_case": morphological_features_storage[i][3],
                      "sentence_part": morphological_features_storage[i][8],
                      "number_in_sentence": morphological_features_storage[i][6],
                      "number_of_sentence": morphological_features_storage[i][7]}))
        return dictionary_list

    @staticmethod
    def process(text):
        dictionary_list = Analyzer.dictionary_with_all_forms_of_words(text)
        dictionary_of_russian_words = list()
        for i in range(len(dictionary_list)):
            for j in range(len(dictionary_list)):
                if dictionary_list[i].get("word") == dictionary_list[j].get("word") and i != j and i < j:
                    for key in dictionary_list[i]:
                        if not (dictionary_list[i][key] == dictionary_list[j][key]):
                            dictionary_list[i][key] = str(dictionary_list[i][key]) + ", " + str(dictionary_list[j][key])
                    dictionary_list[j] = {}
        for i in range(len(dictionary_list)):
            if dictionary_list[i] != {}:
                dictionary_of_russian_words.append(dictionary_list[i])
        return dictionary_of_russian_words


if __name__ == "__main__":
    text = "Настала весна. Солнце гонит снега с полей. " \
           "Снега на деревьях раскрылись. " \
           "Они выпустили новые листочки. " \
           "Проснулась и пчелка. " \
           "Почистила глазки мохнатыми лапками и разбудила подруг. " \
           "Выглянули они в окошечко. Идет ли снег, холодный ли ветер? " \
           "Увидели пчелки солнышко и голубое небо. Полетели к яблоньке. " \
           "Но цветы еще ее спрятаны в почках. "
    analyzer = Analyzer()
    dictionary = analyzer.process(text)
    for i in range(len(dictionary)):
        print(dictionary[i])
