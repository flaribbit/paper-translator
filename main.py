from typing import List
from argparse import ArgumentParser
parser = ArgumentParser(description='中英对照论文翻译工具')
parser.add_argument('file', type=str, help='输入PDF文件')
parser.add_argument('--limit', type=int, default=6000, help='单次翻译长度限制')
parser.add_argument('--delay', type=float, default=1, help='等待时间')
parser.add_argument('--full', action='store_true', help='包括参考文献和其他标记')
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
            if text.startswith('<image:') and args.full is False:
                continue
            if len(tmp) + len(text) > args.limit:
                res.append(tmp)
                tmp = ''
            tmp += text+'\n'
    res.append(tmp)
    return res


def write_html(title: str, data: List):
    with open('./template.html') as f:
        html = f.read()
    json_string = json.dumps(data, ensure_ascii=False)
    html = html.replace('<title></title>', f'<title>{title}</title>')
    html = html.replace("import data from './data.json'", f"const data = {json_string}")
    with open(title+'.html', 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    parts = read_pdf(args.file)
    res = []
    for i, text in enumerate(parts):
        print(f'translating {i+1}/{len(parts)}')
        r = baidu_translator(text)
        res += r['trans_result']
        time.sleep(args.delay)
    title = args.file.replace('.pdf', '')
    write_html(title, res)


if __name__ == '__main__':
    import fitz
    import time
    import json
    from translator import baidu_translator
    main()
