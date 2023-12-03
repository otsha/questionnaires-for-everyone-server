from flask import Flask, request, make_response

app = Flask(__name__)

# Translation route
@app.route('/translate', methods = ['POST'])
def translate():
    try:
        # Grab request contents
        req = request.get_json()
        data = req['data']
        translation_type = req['type']

        # Translate based on list type (single / pairs)
        # TODO VALIDATE REQUEST BETTER
        translated_data = []
        if translation_type == 'single':
            translated_data = translate_statements(data)
        elif translation_type == 'pairs':
            translated_data = translate_statement_pairs(data)
        else:
            return make_response({'error': 'Invalid list type! Should be single or pairs.'})

        # Return translated response
        res = make_response({'translated': translated_data}, 200)
        return res
    
    except Exception:
        return make_response({'error': Exception}, 500)
    
def translate_statements(item_list):
    translated_list = []
    
    for item in item_list:
        ti = translate(item)
        translated_list.append(ti)

    return translated_list

def translate_statement_pairs(item_list):
    translated_pairs = []

    for pair in item_list:
        translated_pair = []

        for item in pair:
            ti = translate(item)
            translated_pair.append(ti)

        translated_pairs.append(translated_pair)

    return translated_pairs

def translate(item):
    print('translating <<', item, '>>')
    # TODO: CALL TRANSLATOR
    translated_item = item
    return translated_item