from typing import List
from argparse import ArgumentParser
parser = ArgumentParser(description='中英对照论文翻译工具')
parser.add_argument('file', type=str, help='输入PDF文件')
parser.add_argument('--edit', action='store_true', help='手动编辑提取的文本')
parser.add_argument('--limit', type=int, default=6000, help='单次翻译长度限制')
parser.add_argument('--delay', type=float, default=1, help='等待时间')
parser.add_argument('--full', action='store_true', help='包括参考文献和其他标记')
args = parser.parse_args()


def read_pdf(path: str) -> str:
    doc: fitz.Document = fitz.open(path)
    res = ''
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
            if args.full is False and text.startswith('<image:'):
                continue
            res += text+'\n'
    res = res.encode('utf-8', 'ignore').decode('utf-8')  # fk msword
    return res


def read_txt(text: str) -> List[str]:
    res: List[str] = []
    tmp = ''
    for line in text.split('\n'):
        if len(tmp) + len(line) > args.limit:
            res.append(tmp)
            tmp = ''
        tmp += line+'\n'
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
    if args.file.endswith('.pdf'):
        print('正在提取文本')
        text = read_pdf(args.file)
        if args.edit:  # 需要手动编辑的情况
            text_filename = args.file.replace('.pdf', '.txt')
            with open(text_filename, 'w', encoding='utf-8') as f:
                f.write(text)
            input(f'文件已保存为: {text_filename}, 编辑后按下回车键继续运行')
            with open(text_filename, 'r', encoding='utf-8') as f:
                text = f.read()
    elif args.file.endswith('.txt'):
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        raise ValueError('只支持 pdf 和 txt 格式的文件')
    print('正在分割文本')
    parts = read_txt(text)
    res = []
    for i, text in enumerate(parts):
        print(f'正在翻译 {i+1}/{len(parts)}')
        r = baidu_translator(text)
        res += r['trans_result']
        time.sleep(args.delay)
    title = args.file.replace('.pdf', '')
    write_html(title, res)
    print(f'文件已保存为: {title}.html')


if __name__ == '__main__':
    import fitz
    import time
    import json
    from translator import baidu_translator
    main()
