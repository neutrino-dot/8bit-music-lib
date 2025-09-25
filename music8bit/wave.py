import numpy as np
from scipy import signal
from abc import ABC, abstractmethod
from .core import SongConfig
import numbers
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
        self.duty = SongConfig.checkVT(duty, numbers.Real, 0.0, 1.0, "duty")
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
        return 2 / np.pi * np.arcsin(np.sin(tt))

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
    def generate(self, freqs, t):
        num_samples = len(t)
        waves = np.random.uniform(-1, 1, (len(freqs), num_samples))
        envelope = np.exp(-5 * t)
        waves *= envelope
        return waves
