#!/usr/bin/env python3
"""给 lessons.json 里所有要朗读的瑞士德语生成录音，存到 audio/ 下。

用法:  .venv/bin/python make_audio.py          只补缺的
       .venv/bin/python make_audio.py --force  全部重录
凡是 JSON 里叫 "w" 的字段都会被录音；有 "say" 的就录 "say" 的内容。
文件名是文本的 FNV-1a 哈希，和 page.html 里的 akey() 保持一致。
"""
import asyncio, json, pathlib, sys
import edge_tts

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / 'audio'
VOICE = 'de-CH-LeniNeural'
RATE = '-8%'

def akey(t):
    x = 2166136261
    b = t.encode('utf-16-le')
    for i in range(0, len(b), 2):
        x = ((x ^ (b[i] | b[i + 1] << 8)) * 16777619) & 0xffffffff
    return '%08x' % x

def texts():
    out = []
    def walk(o):
        if isinstance(o, dict):
            t = o.get('say') or o.get('w')
            if isinstance(t, str) and t not in out:
                out.append(t)
            # 对话里的句子按原文播放，"say" 只用在单词卡上
            if 'say' in o and o['w'] not in out and 's' in o:
                out.append(o['w'])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(json.loads((HERE / 'lessons.json').read_text(encoding='utf-8')))
    return out

async def main():
    force = '--force' in sys.argv
    OUT.mkdir(exist_ok=True)
    items = texts()
    keep = set()
    for t in items:
        path = OUT / (akey(t) + '.mp3')
        keep.add(path.name)
        if path.exists() and not force:
            continue
        spoken = t.replace('…', '').replace(' / ', ', ').replace('/', ',')
        await edge_tts.Communicate(spoken, VOICE, rate=RATE).save(str(path))
        print('+', path.name, t)
    for old in OUT.glob('*.mp3'):
        if old.name not in keep:
            old.unlink(); print('-', old.name)
    print(len(items), '条文本，audio/ 下', len(list(OUT.glob('*.mp3'))), '个文件')

asyncio.run(main())
