# 8bit-music-lib(日本語説明)
Pythonで8bit風のチップチューン音楽を再生するためのライブラリです。

正直なところ、使い勝手はあまり良くありません。
ちゃんとした音楽を作るなら MML や一般的な DAW を使った方がずっと楽です。  
「試しに8bit音楽を再生させてみたい！」とかの人達におすすめです。

将来的には MML や MIDI ファイルの入出力にも対応させる予定です。

> **注記**  
> 波形は **8bit相当の解像度に量子化** されますが、再生ライブラリの互換性を考慮し、  
> 出力形式は **16bit PCM配列** になっています。


## ファイル構成
```
8bit-music-lib
├── music8bit
    ├── _init_.py
    ├── core.py
    ├── utils.py
    └── wave.py
 ├── .gitignore
 ├── LICENSE
 ├── README.md
 └── setup.py
```

## インストール方法
基本的には、再生ライブラリ付きでインストールするのを推奨します。


### simpleaudio を使う場合（おすすめ）
依存関係が少なく、Windows / macOS / Linux で安定して動作します。
```bash
pip install 8bit-music-lib[simpleaudio]
```  


### sounddevice を使う場合
PortAudio を利用した再生が可能です。
一部の環境では追加ライブラリの導入が必要になる場合があります。
```bash
pip install 8bit-music-lib[sounddevice]
```


###  を使う場合
Notebook での実験や Google Colaboratory での利用に便利です。
Colab の場合は先頭に `!` を付けて実行してください。
```bash
pip install 8bit-music-lib[jupyter]
```  

※最低限の機能だけ使いたい場合は
```
pip install 8bit-music-lib
```

でもOKですが、この場合波形データ生成のみ行うことができ、音声再生はできません。
