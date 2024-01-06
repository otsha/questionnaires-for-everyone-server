from flask import Flask, request, make_response
from flask_cors import CORS
import os
from dotenv import load_dotenv

from translation_utils import translate_statement_pairs, translate_statements
from evaluation_utils import evaluate_gemba, evaluate_ssa

app = Flask(__name__)
load_dotenv()
frontend_url = os.getenv('FRONTEND_URL')
CORS (app, origins = [frontend_url])

@app.route('/translate', methods = ['POST'])
def translate():
    try:
        # Grab request contents
        req = request.get_json()
        data = req['data']
        translation_type = req['listType']
        from_lang = req['sourceLang']
        to_lang = req['targetLang']

        # Translate based on list type (single / pairs)
        # TODO VALIDATE REQUEST BETTER
        translated_data = []
        if translation_type == 'single':
            translated_data = translate_statements(data, from_lang, to_lang)
        elif translation_type == 'pairs':
            translated_data = translate_statement_pairs(data, from_lang, to_lang)
        else:
            return make_response({'error': 'Invalid list type! Should be single or pairs.'})

        # Return translated response
        res = make_response({'translated': translated_data}, 200)
        return res
    
    except Exception as e:
        return make_response({'error': str(e)}, 500)
    
@app.route('/evaluate', methods = ['POST'])
def evaluate():
    try:
        # Grab request contents
        req = request.get_json()
        list_type = req['listType']
        source_items = req['sourceItems']
        new_items = req['newItems']
        bt_items = req['backtranslatedItems']
        from_lang = req['sourceLang']
        to_lang = req['targetLang']

        # 1. GEMBA (src + new)

        gemba_res = evaluate_gemba(source_items, new_items, from_lang, to_lang, list_type)
        print(gemba_res)

        if 'error' in gemba_res:
            raise AssertionError(gemba_res['error'])
        
        # 2. Semantic similarity assessment

        ssa_res = evaluate_ssa(source_items, new_items, from_lang, to_lang, list_type)
        print(ssa_res)

        if 'error' in ssa_res:
            raise AssertionError(ssa_res['error'])
        
        # TODO: COMPARE EXPRESSIONS FOR A SECOND SIMILARITY SCORE?

        return make_response({
            'gemba': gemba_res['score'],
            'semantic': ssa_res
        }, 200)

    except Exception as e:
        return make_response({'error': str(e)}, 500)