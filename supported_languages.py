from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.cloud import translate

translate_client = translate.Client()

results = translate_client.get_languages()

for language in results:
    print(u'{name} ({language})'.format(**language))
