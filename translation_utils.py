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
    print('translating <<', item, '>>', 'from', from_lang, 'to', to_lang)

    # TODO: CALL TRANSLATOR
    
    translated_item = item
    return translated_item