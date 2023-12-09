# Refer to https://github.com/openai/openai-python for OpenAI library documentation

import requests
import os
from dotenv import load_dotenv
from openai import OpenAI

auth_key = os.getenv('OPENAI_AUTH_KEY')
client = OpenAI(api_key = auth_key)

def format_list_singles(list):
    formatted = ''
    
    for item in list:
        formatted += item + '\n'

    return formatted

def format_list_pairs(list):
    formatted = ''
    
    for pair in list:
        formatted_pair = pair[0] + ' - ' + pair[1]
        formatted += formatted_pair + '\n'
    
    return formatted

# GEMBA evaluation of translation quality
# Kocmi, T., & Federmann, C. (2023). Large language models are state-of-the-art evaluators of translation quality. arXiv preprint arXiv:2302.14520."
def evaluate_gemba(source, translation, src_lang, tgt_lang, list_type):
    try:
        # Format input for better comparisons
        src_fmt = ''
        tlt_fmt = ''

        if list_type == 'single':
            src_fmt = format_list_singles(source)
            tlt_fmt = format_list_singles(translation)
        elif list_type == 'pairs':
            src_fmt = format_list_pairs(source)
            tlt_fmt = format_list_pairs(translation)
        else:
            raise AssertionError('List type must be single / pairs.')
        
        command = format_gemba_command(src_lang, tgt_lang, src_fmt, tlt_fmt)
        response = client.chat.completions.create(
            messages = [
                {
                    "role": "user",
                    "content": str(command),
                }
            ],
            model="gpt-3.5-turbo",
        )

        score = response.choices[0].message.content
        return {'score': score}
    except Exception as e:
        return {'error': e}

# GEMBA GPT instruction formatting
def format_gemba_command(src_lang, tgt_lang, source, target):
    fmt = """Score the following translation from {source_lang} to {target_lang} on a continuous scale from 0 to 100, where a score of zero means \"no meaning preserved\" and score of one hundred means \"perfect meaning and grammar\".\n
{source_lang} source:
{source_seg}

{target_lang} translation:
{target_seg}

Score:""".format(source_lang = src_lang, target_lang = tgt_lang, source_seg = source, target_seg = target)

    return fmt