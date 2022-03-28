import fitz
import time
import json
from typing import List
from argparse import ArgumentParser
from translator import baidu_translator
parser = ArgumentParser(description='paper tool')
parser.add_argument('-i', '--input', type=str, help='Input PDF file')
parser.add_argument('--limit', type=int, default=6000)
parser.add_argument('--delay', type=float, default=1)
parser.add_argument('--full', action='store_true')
args = parser.parse_args()


def read_pdf(path: str):
    doc: fitz.Document = fitz.open(path)
    res = []
    tmp = ''
    for page in doc:
        blocks = page.get_text("blocks")
        for block in blocks:
            text: str = block[4]
            text = text.replace('-\n', '').replace('\n', ' ')
            text = text.replace('ﬁ', 'fi')
            text = text.replace('ﬂ', 'fl')
            text = text.replace('ﬀ', 'ff')
            text = text.replace('ﬃ', 'ffi')
            text = text.replace('ﬄ', 'ffl')
            if 'REFERENCES' in text:
                print('skipping references')
                break
            if len(tmp) + len(text) > args.limit:
                res.append(tmp)
                tmp = ''
            tmp += text+'\n'
    res.append(tmp)
    return res


parts = read_pdf(args.input)
for i, text in enumerate(parts):
    print(f'translating {i+1}/{len(parts)}')
    res = baidu_translator(text)
    with open(f'{i}.json', 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False)
    time.sleep(args.delay)
