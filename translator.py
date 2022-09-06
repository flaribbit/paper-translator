from typing import Any, Dict
import os
import hashlib
import random


if not os.path.isfile('key.py'):
    with open('key.py', 'w') as f:
        f.write('''baidu = {
    'appid': '',
    'appkey': '',
}

tencent = {
    'SecretId': '',
    'SecretKey': '',
}
''')
        print('请填写 key.py 后再次运行程序')
        exit(0)
import key
if key.baidu['appid']:
    translator = 'baidu'
    appid, appkey = key.baidu['appid'], key.baidu['appkey']
else:
    translator = 'tencent'
    appid, appkey = key.tencent['SecretId'], key.tencent['SecretKey']


def super_translator(query: str):
    if translator == 'baidu':
        return baidu_translator(query)['trans_result']
    else:
        return convert_tencent_result(query, tencent_translator(query)['TargetText'])


def make_md5(s: str, encoding='utf-8') -> str:
    return hashlib.md5(s.encode(encoding)).hexdigest()


def baidu_translator(query: str) -> Dict[str, Any]:
    import requests
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


def tencent_translator(query: str):
    import json
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.tmt.v20180321 import tmt_client, models
    cred = credential.Credential(appid, appkey)
    httpProfile = HttpProfile()
    httpProfile.endpoint = "tmt.tencentcloudapi.com"
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = tmt_client.TmtClient(cred, "ap-beijing", clientProfile)
    req = models.TextTranslateRequest()
    params = {
        "SourceText": query,
        "Source": "en",
        "Target": "zh",
        "ProjectId": 0
    }
    req.from_json_string(json.dumps(params))
    resp = client.TextTranslate(req)
    res = resp._serialize(allow_none=True)
    if 'TargetText' not in res:
        raise ValueError(res)
    return res


def convert_tencent_result(from_text: str, to_text: str):
    return [{'src': a, 'dst': b} for a, b in zip(from_text.split('\n'), to_text.split('\n'))]


if __name__ == '__main__':
    res = tencent_translator('Hello World! This is 1st paragraph.\nThis is 2nd paragraph.')
    # res = baidu_translator('Hello World! This is 1st paragraph.\nThis is 2nd paragraph.')
    print(res)
