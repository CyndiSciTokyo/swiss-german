#!/usr/bin/env python3
"""把 page.html(网站本体)和 lessons.json(课程内容)合成可以直接打开的 index.html。"""
import json, pathlib
here = pathlib.Path(__file__).resolve().parent
data = json.dumps(json.loads((here / 'lessons.json').read_text(encoding='utf-8')), ensure_ascii=False).replace('</', '<\\/')
page = (here / 'page.html').read_text(encoding='utf-8').replace('/*DATA*/null', data)
head = ('<!doctype html><html lang="zh"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<style>body{margin:0}[hidden]{display:none!important}</style></head><body>\n')
(here / 'index.html').write_text(head + page + '\n</body></html>\n', encoding='utf-8')
print('index.html 已生成')
