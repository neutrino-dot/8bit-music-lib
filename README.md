# 8bit-music-lib(English Introduction ver)
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
```

