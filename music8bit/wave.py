import numpy as np
from scipy import signal
import warnings
from abc import ABC, abstractmethod
from .utils import _validate


class WaveGenerator(ABC):
    """
    Abstract base class for waveform generators.

    This class defines the interface for all waveform generators.
    Subclasses must implement the `generate` method.

    Methods
    -------
    generate(freqs, t)
        Generate waveform data for the given frequencies and time array.
    """
    @property
    def using_unique_notes(self) -> bool:
        return False

    @abstractmethod
    def generate(self, freqs, t):
        pass

class SquareWave(WaveGenerator):
    """
    Generate square wave signals with optional duty cycle.

    Parameters
    ----------
    duty : float, optional
        Duty cycle of the square wave (0.0-1.0), default is 0.5.

    Methods
    -------
    generate(freqs, t)
        Generate square wave for the given frequencies and time array.
    """
    def __init__(self, duty=0.5):
        self.duty = _validate(duty, (int,float), least_range=0.0, most_range=1.0, name="duty")
    
    def generate(self, freqs, t):
        tt = 2 * np.pi * freqs[:, None] * t[None, :]
        return signal.square(tt, duty=self.duty)

class SineWave(WaveGenerator):
    """
    Generate sine wave signals.

    Methods
    -------
    generate(freqs, t)
        Generate sine wave for the given frequencies and time array.
    """
    def generate(self, freqs, t):
        tt = 2 * np.pi * freqs[:, None] * t[None, :]
        return np.sin(tt)

class TriangleWave(WaveGenerator):
    """
    Generate triangle wave signals using arcsin(sin(...)) approximation.

    Methods
    -------
    generate(freqs, t)
        Generate triangle wave for the given frequencies and time array.
    """
    def generate(self, freqs, t):
        tt = 2 * np.pi * freqs[:, None] * t[None, :]
        return 2 * np.abs(2 * (tt - np.floor(tt + 0.5))) - 1

class NoiseWave(WaveGenerator):
    """
    Generate noise signals with an exponential decay envelope.

    This class mimics the noise channel found in retro game consoles.
    The noise itself has no inherent meaning—it's just randomness.
    
    Parameters
    ----------
    decay_rate : float, optional
        Duty cycle of the square wave (0.0-1.0), default is 0.5.

    Methods
    -------
    generate(freqs, t)
        Exponential decay coefficient. Larger = faster decay. Default is 5.0.
    """
    @property
    def using_unique_notes(self) -> bool:
        return True  # 未知の音符もOK

    def __init__(self, decay_rate=5.0):
        self.decay_rate = _validate(decay_rate, (int, float), least_range=0.0, name="decay_rate")
        
    def generate(self, freqs, t, decay_rate=None):
        if decay_rate is None:
            decay_rate = self.decay_rate
        num_samples = len(t)
        waves = np.random.uniform(-1, 1, (len(freqs), num_samples))
        envelope = np.exp(-decay_rate * t)
        waves *= envelope
        return waves

class DrumWave(WaveGenerator):
    @property
    def using_unique_notes(self) -> bool:
        return True  # 未知の音符もOK

    def __init__(self):
        self.noise = NoiseWave()

    def generate(self, freqs, t):
        n = str(freqs).lower()
        if n == "kick":
            # 初期ピッチ高めから最終ピッチへスライド
            freq_start = 150.0
            freq_end = 50.0
            freqs_t = freq_start + (freq_end - freq_start) * t / t[-1]

            # 三角波生成
            tt = 2 * np.pi * freqs_t * t
            wave = 2 / np.pi * np.arcsin(np.sin(tt))

            # 短い減衰（Decay）
            wave *= np.exp(-8 * t)

            # 短いアタックノイズ
            wave += 0.05 * self.noise.generate([1], t, decay_rate=20.0)[0]

        elif n == "snare":
            wave = self.noise.generate([1], t, decay_rate=30.0)[0]
        elif n == "hihat":
            wave = self.noise.generate([1], t, decay_rate=80.0)[0]
        else:
            if n != "r":
                warnings.warn(f"Unknown note: {n}")
            wave = np.zeros(len(t))

        return np.array([wave])

__all__ = [
    "SquareWave",
    "TriangleWave",
    "SineWave",
    "NoiseWave",
    "DrumWave",
    "WaveGenerator"
]
