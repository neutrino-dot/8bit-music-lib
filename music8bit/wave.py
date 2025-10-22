import numpy as np
from scipy import signal
from abc import ABC, abstractmethod
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
        if not isinstance(duty, (int,float)) or not (0.0 <= duty <= 1.0):
            raise ValueError(f"duty must be a real number between 0.0 and 1.0, got {duty}")
        self.duty = duty
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
    So if you want to label it with your favorite symbol (★, ♪, ☂, etc.),
    go ahead! It’s purely up to your imagination.

    Methods
    -------
    generate(freqs, t)
        Generate noise waveform. `freqs` is ignored; `t` is used to shape the envelope.
    """
    @property
    def using_unique_notes(self) -> bool:
        return True  # 未知の音符もOK
    
    def generate(self, freqs, t):
        num_samples = len(t)
        waves = np.random.uniform(-1, 1, (len(freqs), num_samples))
        envelope = np.exp(-5 * t)
        waves *= envelope
        return waves

class DrumWave(WaveGenerator):
    @property
    def using_unique_notes(self) -> bool:
        return True  # 未知の音符もOK

    def generate(self, freqs, t):
        waves = []
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
            wave += 0.05 * np.random.uniform(-1, 1, len(t)) * np.exp(-20 * t)

        elif n == "snare":
            wave = np.random.uniform(-1, 1, len(t)) * np.exp(-30*t)
        elif n == "hihat":
            wave = np.random.uniform(-1, 1, len(t)) * np.exp(-80*t)
        else:
            wave = np.zeros(len(t))
        waves.append(wave)

        return np.array(waves)

__all__ = [
    "SquareWave",
    "TriangleWave",
    "SineWave",
    "NoiseWave",
    "DrumWave",
    "WaveGenerator"
]
