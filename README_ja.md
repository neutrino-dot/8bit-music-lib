# 8bit-music-lib(日本語説明ver)
Pythonで8bit風のチップチューン音楽を再生するためのライブラリです。

正直なところ、使い勝手はあまり良くありません。  
普通に音楽を作るなら MML や一般的な DAW を使った方がずっと楽です。  
それでも「Pythonで8bitサウンドを鳴らしてみたい！」という方向けの、かなりニッチなライブラリです。

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

## 使用方法
