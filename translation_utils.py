import deepl
import os
from dotenv import load_dotenv

load_dotenv()
auth_key = os.getenv('DEEPL_AUTH_KEY')

def translate_statements(item_list, from_lang, to_lang):
    translated_list = []
    
    for item in item_list:
        ti = translate(item, from_lang, to_lang)
        translated_list.append(ti)

    return translated_list

def translate_statement_pairs(item_list, from_lang, to_lang):
    translated_pairs = []

    for pair in item_list:
        translated_pair = []

        for item in pair:
            ti = translate(item, from_lang, to_lang)
            translated_pair.append(ti)

        translated_pairs.append(translated_pair)

    return translated_pairs

def translate(item, from_lang, to_lang):
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(item, source_lang = from_lang, target_lang = to_lang)

    translated_item = result.text
    return translated_item