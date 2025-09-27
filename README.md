# 8bit-music-lib
8-bit style music synthesis library in Python


## Custom Waveform

To add your own waveform, subclass `WaveGenerator` and implement `generate(freqs, t)`.
Example:
```python
from musiclib.waves import WaveGenerator
import numpy as np

class MyWave(WaveGenerator):
    def generate(self, freqs, t):
        return np.sin(2*np.pi*freqs[:, None]*t[None, :])**3

# 8bit-music-lib
これはPythonで8bitの音楽を流すことができるように作成されたPythonライブラリです。
はっきりいうとこれを使っていただける方はよっぽどの、もの好きです。
これを使うぐらいなら、MMLとか普通のDawとかの方が使いやすいからですね。

## ファイル構成
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

## 使用方法
