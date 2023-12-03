from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/translate', methods = ['POST'])
def translate():
    try:
        # Grab request contents
        data = request.get_json()['data']
        print(data)

        # TODO: TRANSLATE
        tranlated_data = 'yepyep!'

        # Return translated response
        res = make_response({'translated': tranlated_data}, 200)
        return res
    
    except Exception:
        return make_response({'error': Exception}, 500)