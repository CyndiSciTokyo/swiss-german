# 苏黎世一个月 · Ein Monat z Züri

**在线学习：https://cyndiscitokyo.github.io/swiss-german/**

一个学瑞士德语（苏黎世话）的小网站：跟着房东 Vreni 在苏黎世住一个月，每一课是城里的一站。
每课先学（故事 → 单词 → 说法 → 对话），四步都看过才能做练习。

- `lessons.json`：全部课程内容（单词、汉字注音、联想记忆、对话、练习题）
- `page.html`：网站本体
- `make_audio.py`：用 edge-tts（de-CH-LeniNeural）给所有瑞士德语句子录音，放到 `audio/`
- `build.py`：把 `page.html` 和 `lessons.json` 合成 `index.html`

改完内容后：

```
.venv/bin/python make_audio.py
python3 build.py
```
