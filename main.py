import site
import importlib
import pkg_resources
from imp import reload

site.addsitedir('./lib/')

reload(pkg_resources)
pkg_resources.get_distribution('google-api-core')
pkg_resources.get_distribution('google-cloud-translate')

import requests
from requests_toolbelt.adapters import appengine
appengine.monkeypatch()

s = requests.Session()
s.mount('http://', appengine.AppEngineAdapter())
s.mount('https://', appengine.AppEngineAdapter())

from flask import Flask
from flask import render_template, send_from_directory
from flask import make_response
from flask import jsonify
from flask import request
#from google.cloud import language
#from requests_toolbelt.adapters import appengine
#from google.cloud.language import enums
#from google.cloud.language import types

app = Flask(__name__, static_url_path='')

#Plain endpoint is http://127.0.0.1:5000/
@app.route('/')
def hello():
    #resp = make_response(render_template('page2.html'))
    #return resp
    return render_template('index.html')

@app.route('/translate', methods=['GET', 'POST'])
def hi():
    # Imports the Google Cloud client library
    from google.cloud import translate
    # Instantiates a client
    translate_client = translate.Client()

    data = request.get_json(force=True)
    #print('Data Received: "{data}"'.format(data=data))

    input_text = data['text_to_translate']
    target_language = data['target_lang']

    # Translates some text into Russian
    translation = translate_client.translate(input_text, target_language=target_language)

    #print(u'Text: {}'.format(input_text))
    #print(u'Translation: {}'.format(translation['translatedText']))

    return jsonify(translation['translatedText'])


@app.route('/detect', methods=['GET', 'POST'])
def detecting_language():
    # Imports the Google Cloud client library
    from google.cloud import translate

    """Detects the text's language."""
    translate_client = translate.Client()

    text = request.get_json(force=True)
    #print('Data Received: "{data}"'.format(data=text))

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.detect_language(text)

    #print('Text: {}'.format(text))
    #print('Confidence: {}'.format(result['confidence']))
    #print('Language: {}'.format(result['language']))

    return jsonify(result['language'])

if __name__ == '__main__':
    #appengine.monkeypatch()
    app.run()

#
# https://stackoverflow.com/questions/26980713/solve-cross-origin-resource-sharing-with-flask
# https://flask-cors.corydolphin.com/en/2.0.1/
# https://stackoverflow.com/questions/43871637/no-access-control-allow-origin-header-is-present-on-the-requested-resource-whe
