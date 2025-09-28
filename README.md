# 8bit-music-lib (English)
This is a Python library for playing 8-bit style chiptune music.

[日本語READMEはこちら](README_ja.md)

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
│   ├── _init_.py
│   ├── core.py
│   ├── utils.py
│   └── wave.py
├── .gitignore
├── LICENSE
├── README.md
└── setup.py
```

---

## Installation

It is recommended to install with a playback library.

### Recommended: via simpleaudio (Windows/macOS/Linux)
```bash
pip install 8bit-music-lib[simpleaudio]
```

### Using PortAudio (via sounddevice)
```bash
pip install 8bit-music-lib[sounddevice]
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

---

## Note Input

To specify a single note:
```python
(['note'], beats)
```

- `note`: e.g., `'C5'` (note name + octave)
- `beats`: duration of the note (1, 2, etc.)

To play multiple notes simultaneously:
```python
(['C5','E5','G5'], 1)  # C, E, G together for 1 beat
```

For rests:
```python
(['R'],1)  # rest for 1 beat
```

To change BPM mid-song:
```python
('BPM', 200)  # change BPM to 200
```

---

## Defining a Part

Use the `Part` class to create a single melody part.  
Multiple parts can be combined to form a full song.

```python
part = m8.Part(
    melody=notes,              # list of notes
    volume=0.5,                # volume (0.0-1.0)
    generator=m8.SquareWave(), # waveform type (SquareWave, TriangleWave, NoiseWave, SineWave, etc.)
    first_bpm=120              # initial BPM
)
```

- `melody`: list of notes
- `volume`: 0.0 = silent, 1.0 = max (too high may cause clipping)
- `generator`: waveform
- `first_bpm`: initial tempo

---

## Playback

Pass a list of `Part` instances to the `SongMixer` class to combine them into a full song waveform.

```python
song = m8.SongMixer([part1, part2, part3])
```

- `synthesize()`: returns waveform data  
- `play()`: plays audio (requires playback library)

---

## Custom Waveform

To add your own waveform, subclass `WaveGenerator` and implement `generate(freqs, t)`.  
Example:
```python
from musiclib.waves import WaveGenerator
import numpy as np

class MyWave(WaveGenerator):
    def generate(self, freqs, t):
        return np.sin(2*np.pi*freqs[:, None]*t[None, :])**3
```
---

## Afterword

This library was created out of the developer's personal desire to play music on Google Colab,  
and turned into a library that anyone can use.

Honestly, the usability and completeness are limited.  
For creating proper music, using MML or a DAW is much easier.  
If you can run Pygame, convenient external libraries like Musicpy are also available in Python.

To those who still enjoy using this library, I hope you have a good 8-bit life.

