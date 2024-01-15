# Refer to https://github.com/openai/openai-python for OpenAI library documentation

import os
from dotenv import load_dotenv
from openai import OpenAI

auth_key = os.getenv('OPENAI_AUTH_KEY')
client = OpenAI(api_key = auth_key)

def format_input(items, list_type):
    if list_type == 'single':
        return format_list_singles(items)
    elif list_type == 'pairs':
        return format_list_pairs(items)
    else:
        raise AssertionError('List type must be single / pairs.')

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

# GEMBA-DA evaluation of translation quality
# Kocmi, T., & Federmann, C. (2023). Large language models are state-of-the-art evaluators of translation quality. arXiv preprint arXiv:2302.14520."
def evaluate_gemba(source, translation, src_lang, tgt_lang, list_type):
    try:
        # Format input for better comparisons
        src_fmt = format_input(source, list_type)
        tlt_fmt = format_input(translation, list_type)
        
        command = format_gemba_command(src_lang, tgt_lang, src_fmt, tlt_fmt)
        response = client.chat.completions.create(
            messages = [
                {
                    'role': 'user',
                    'content': str(command),
                }
            ],
            model = 'gpt-4',
            max_tokens = 1
        )

        score = response.choices[0].message.content
        return {'score': score}
    except Exception as e:
        return {'error': e}

# GEMBA GPT instruction formatting
def format_gemba_command(src_lang, tgt_lang, source, target):
    fmt = """Score the following translation from {source_lang} to {target_lang} on a continuous scale from 0 to 100, where a score of zero means \"no meaning preserved\" and score of one hundred means \"perfect meaning and grammar\".

{source_lang} source: \"{source_seg}\"
{target_lang} translation: \"{target_seg}\"

Score:""".format(source_lang = src_lang, target_lang = tgt_lang, source_seg = source, target_seg = target)

    return fmt

# SSA (Semantic similarity assessment)
# Experimental! Attempts to score the semantic similarity between the source and original,
# to justify the score verbally, and to give suggestions for improving the score.
def evaluate_ssa(source, translation, src_lang, tgt_lang, list_type):
    try:
        src_fmt = format_input(source, list_type)
        tlt_fmt = format_input(translation, list_type)
        
        command = format_ssa_command(src_lang, tgt_lang, src_fmt, tlt_fmt)
        response = client.chat.completions.create(
            messages = [
                {
                    'role': 'user',
                    'content': str(command),
                }
            ],
            model = 'gpt-4-1106-preview',
            max_tokens = 400,
            response_format = { 'type': 'json_object' }
        )

        return response.choices[0].message.content
    except Exception as e:
        return {'error': e}
    
# SSA GPT instruction formatting
def format_ssa_command(src_lang, tgt_lang, source, target):
    fmt = """Assess the semantic similarity of the following texts in {source_lang} and {target_lang} on a scale from 0 (no semantic similarity at all) to 100 (perfect semantic similarity). Justify the score. Provide a single paragraph suggesting changes to the {target_lang} version (i.e. word or expression replacements) to improve the score.

{source_lang}:  \"{source_text}\"
{target_lang}: \"{target_text}\"

Respond with JSON only in the following format:

score
reasoning,
suggestion""".format(source_lang = src_lang, target_lang = tgt_lang, source_text = source, target_text = target)
    return fmt