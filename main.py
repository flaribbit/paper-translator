from argparse import ArgumentParser
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


def main():
    parts = read_pdf(args.input)
    res = []
    for i, text in enumerate(parts):
        print(f'translating {i+1}/{len(parts)}')
        r = baidu_translator(text)
        res += r['trans_result']
        time.sleep(args.delay)
    out_filename = args.input.replace('.pdf', '.json')
    with open(out_filename, 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False)


if __name__ == '__main__':
    import fitz
    import time
    import json
    from typing import List
    from translator import baidu_translator
    main()
