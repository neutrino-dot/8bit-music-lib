# 8bit-music-lib (English)
This is a Python library for playing 8-bit style chiptune music.

[日本語READMEはこちら](https://github.com/neutrino-dot/8bit-music-lib/blob/main/README_ja.md)

- Compatible with Jupyter Notebook, so it can also run on Google Colaboratory.
- Recommended for those who want to quickly try playing 8-bit music.
- In the future, support for importing and exporting MML and MIDI files is planned.

> **Note**  
> Waveforms are quantized to **8-bit resolution**, but for compatibility with playback libraries,  
> the output format is **16-bit PCM array**.

---

## File Structure

```
8bit-music-lib
├── music8bit
│   ├── __init__.py
│   ├── mixer.py
│   ├── notes.py
│   ├── part.py
│   ├── utils.py
│   └── wave.py
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── README.md
├── README_ja.md
└── setup.py
```

---

## Installation

It is recommended to install with a playback library.

### Recommended: via sounddevice (Windows/macOS/Linux)
```bash
pip install 8bit-music-lib[sounddevice]
```
### Alternative: via simpleaudio (requires C++ build tools on Windows)
```bash
pip install 8bit-music-lib[simpleaudio]

```
### Jupyter Notebook / Google Colaboratory
Useful for playing audio and displaying waveforms directly in the notebook.  
On Colab, add `!` at the beginning of the command:
```bash
pip install 8bit-music-lib[jupyter]
```

### Minimal installation
```bash
pip install 8bit-music-lib
```
Only waveform generation is available; audio playback is not supported.

---

## Importing

Simple import:
```python
from music8bit import *
```

To avoid conflicts with other modules:
```python
import music8bit as m8
```

---

## Example (Simple Demo: Twinkle Twinkle Little Star)

```python
import music8bit as m8

# Define notes
notes = [
    (['C5'],1), (['C5'],1), (['G5'],1), (['G5'],1),
    (['A5'],1), (['A5'],1), (['G5'],2),
    (['F5'],1), (['F5'],1), (['E5'],1), (['E5'],1),
    (['D5'],1), (['D5'],1), (['C5'],2)
]

# Define a part
part1 = m8.Part(
    melody=notes,
    volume=0.5,
    generator=m8.SquareWave(),
    first_bpm=120
)

# Create a song
song = m8.SongMixer([part1])

# Play
song.play()
```
Detailed usage, complex examples, and explanations of each class are summarized in the [Wiki](https://github.com/neutrino-dot/8bit-music-lib/wiki).

---
## Afterword

This library was created out of the developer's personal desire to play music on Google Colab,  
and turned into a library that anyone can use.

Honestly, the usability and completeness are limited.  
For creating proper music, using MML or a DAW is much easier.  
If you can run Pygame, convenient external libraries like Musicpy are also available in Python.

To those who still enjoy using this library, I hope you have a good 8-bit life.
