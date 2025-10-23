# 8bit-music-lib（日本語説明）

Pythonで8bit風のチップチューン音楽を再生するためのライブラリです。

- Google Colaboratoryでも動かせるようにJupyter Notebookに対応
- 「試しに8bit音楽を再生させてみたい！」という方向け
- 将来的にはMMLやMIDIファイルの入出力にも対応予定

> **注記**  
> 波形は **8bit相当の解像度に量子化** されますが、再生ライブラリとの互換性を考慮し、  
> 出力形式は **16bit PCM配列** です。

---

## ファイル構成

```
8bit-music-lib
├── music8bit
│   ├── __init__.py
│   ├── core.py
│   ├── utils.py
│   └── wave.py
├── .gitignore
├── LICENSE
├── README.md
├── README_ja.md
└── setup.py
```

---

## インストール方法

基本的には、再生ライブラリ付きでのインストールを推奨します。

### 推奨: sounddevice 経由（Windows/macOS/Linux）
```bash
pip install 8bit-music-lib[sounddevice]
```

### 代替: simpleaudio 経由（要C++ビルド環境、Windowsで注意）
```bash
pip install 8bit-music-lib[simpleaudio]
```

### Jupyter Notebook / Google Colaboratory
Notebook上で音声再生や波形表示を行う場合に便利です。
Colabではコマンドの先頭に `!` を付けて実行してください。
```bash
pip install 8bit-music-lib[jupyter]
```

### 最低限の機能だけ使用する場合
```bash
pip install 8bit-music-lib
```
波形データの生成のみ可能で、音声再生はできません。

---

## インポート方法

簡単にインポート：
```python
from music8bit import *
```

干渉を避けたい場合：
```python
import music8bit as m8
```

---

## 使用例（簡単デモ：キラキラ星）

```python
import music8bit as m8

# 音符定義
notes = [
    (['C5'],1), (['C5'],1), (['G5'],1), (['G5'],1),
    (['A5'],1), (['A5'],1), (['G5'],2),
    (['F5'],1), (['F5'],1), (['E5'],1), (['E5'],1),
    (['D5'],1), (['D5'],1), (['C5'],2)
]

# パート定義
part1 = m8.Part(
    melody=notes,
    volume=0.5,
    generator=m8.SquareWave(),
    first_bpm=120
)

# 曲を作成
song = m8.SongMixer([part1])

# 再生
song.play()
```

詳細な使い方や複雑なサンプル、各クラスの説明などは[wiki](https://github.com/neutrino-dot/8bit-music-lib/wiki/Home_JP)にまとめています。

---
## あとがき

このライブラリは、制作者が Google Colab で音楽を流したいという身勝手な欲求のために、  
個人的に作ったプログラムをライブラリ化したものです。

正直、使い勝手や完成度はあまり良くありません。  
ちゃんとした音楽を作るなら、MML や一般的な DAW を使った方がずっと楽です。  
また、Pygame を動かせる環境であれば、Musicpy などの便利な外部ライブラリも Python にはあります。

それでも、このライブラリを使っていただける人のために、  
今後も身勝手に開発を続けていきます。
