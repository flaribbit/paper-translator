from typing import Any, Dict
import hashlib
import random
import requests


with open('key.txt') as f:
    appid, appkey = f.read().split()


def make_md5(s, encoding='utf-8') -> str:
    return hashlib.md5(s.encode(encoding, errors='surrogateescape')).hexdigest()


def baidu_translator(query: str) -> Dict[str, Any]:
    from_lang = 'en'
    to_lang = 'zh'
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    salt = random.randrange(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}
    r = requests.post(url, params=payload, headers=headers)
    res = r.json()
    if 'trans_result' not in res:
        raise ValueError(res)
    return res


if __name__ == '__main__':
    res = baidu_translator('Hello World! This is 1st paragraph.\nThis is 2nd paragraph.')
    print(res)
