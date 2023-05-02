from nltk.corpus import wordnet
from ruwordnet import RuWordNet
from nltk.tokenize import sent_tokenize
from wiki_ru_wordnet import WikiWordnet
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
        wn = RuWordNet()
        morphological_features_list = list()
        for first_index in range(len(storage_of_words)):
            for second_index in range(len(storage_of_words[first_index])):
                if not (morph.parse(storage_of_words[first_index][second_index])[0].tag.POS == "PREP" or
                        morph.parse(storage_of_words[first_index][second_index])[0].tag.POS == "CONJ" or
                        morph.parse(storage_of_words[first_index][second_index])[0].tag.POS == "ADVB"):
                    a = morph.parse(storage_of_words[first_index][second_index])[0].normal_form
                    if len(wn.get_senses(a)) == 0:
                        morphological_features_list.append([storage_of_words[first_index][second_index].lower(),morph.parse(storage_of_words[first_index][second_index])[0].normal_form,
                             None, None, None, None, None, None, None, None])
                        break
                    morphological_features_list.append([storage_of_words[first_index][second_index].lower(),#вывод самого слова
                                   morph.parse(storage_of_words[first_index][second_index])[0].normal_form, #начальная форма
                                   wn.get_senses(a)[0].synset.classes[0].title if len(wn.get_senses(a)[0].synset.classes) != 0 else None,#часть речи
                                   wn.get_senses(a)[0].synset.hypernyms[0].title if len(wn.get_senses(a)[0].synset.hypernyms) !=0 else None,#падеж
                                   wn.get_senses(a)[0].synset.antonyms[0].title if len(wn.get_senses(a)[0].synset.antonyms) !=0 else None,#число
                                   wn.get_senses(a)[0].synset.holonyms[0].title if len(wn.get_senses(a)[0].synset.holonyms) !=0 else None,#род
                                   wn.get_senses(a)[0].synset.meronyms[0].title if len(wn.get_senses(a)[0].synset.meronyms) !=0 else None,#номер слова в предложении
                                   wn.get_senses(a)[0].synset.pos_synonyms[0].title if len(wn.get_senses(a)[0].synset.pos_synonyms) !=0 else None,
                                   wn.get_senses(a)[0].synset.related[0].title if len(wn.get_senses(a)[0].synset.related) !=0 else None,
                                   wn.get_senses(a)[0].synset.domain_items[0].title if len(wn.get_senses(a)[0].synset.domain_items) !=0 else None])#номер предложения
        return morphological_features_list

    @staticmethod
    def dictionary_with_all_forms_of_words(text):
        dictionary_list = list()
        sentences = Analyzer.text_into_sentences(text)
        storage_of_words = Analyzer.sentences_into_words(sentences)
        morphological_features_storage = Analyzer.words_morphological_features(storage_of_words)
        for i in range(len(morphological_features_storage)):
            dictionary_list.append(
                dict({"word": morphological_features_storage[i][0].lower(),
                      "normal_form": morphological_features_storage[i][1],
                      "classes": morphological_features_storage[i][2],
                      "hypernyms": morphological_features_storage[i][3],
                      "antonyms": morphological_features_storage[i][4],
                      "holonyms": morphological_features_storage[i][5],
                      "meronyms": morphological_features_storage[i][6],
                      "pos_synonyms": morphological_features_storage[i][7],
                      "related": morphological_features_storage[i][8],
                      "domain_items": morphological_features_storage[i][9]}))
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
    text_example = "Настала весна. Солнце гонит снега с полей. Снега на деревьях раскрылись. Они выпустили новые листочки. " \
           "Проснулась и пчелка. Почистила глазки мохнатыми лапками и разбудила подруг. Выглянули они в окошечко. " \
           "Идет ли снег, холодный ли ветер? Увидели пчелки солнышко и голубое небо. Полетели к яблоньке. Но цветы еще ее спрятаны в почках."
    text_after_changes = Analyzer.process(text_example)
    for i in range(len(text_after_changes)):
        print(text_after_changes[i])

