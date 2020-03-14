import json
import os
from pprint import pprint

import requests

PAPAGO_ENDPOINT = 'https://naveropenapi.apigw.ntruss.com/nmt/v1/translation'


def translate(text, from_lang, to_lang):
    payload = {
        'source': from_lang,
        'target': to_lang,
        'text': text
    }

    headers = {
        'X-NCP-APIGW-API-KEY-ID': os.getenv("PAPAGO_CONFIG_KEY"),
        'X-NCP-APIGW-API-KEY': os.getenv("PAPAGO_CONFIG_SECRET")
    }

    res = requests.post(PAPAGO_ENDPOINT, data=payload, headers=headers)

    if res.status_code != 200:
        print("[PAPAGO] error on ", text)
        pprint(res)
        return None

    return json.loads(res.content)['message']['result']['translatedText']
