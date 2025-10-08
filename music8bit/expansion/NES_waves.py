import numpy as np
from scipy.signal import butter, lfilter
from music8bit.wave import WaveGenerator

def polyblep_vec_2d(phase, dt):
    out = np.zeros_like(phase)
    mask_start = phase < dt
    mask_end = phase > 1.0 - dt

    x = np.zeros_like(phase)
    x[mask_start] = phase[mask_start] / dt
    out[mask_start] = x[mask_start] + x[mask_start] - x[mask_start]**2 - 1.0

    x[mask_end] = (phase[mask_end] - 1.0) / dt
    out[mask_end] = x[mask_end]**2 + 3 * x[mask_end] + 1.0

    return out

def envelope(t, attack=0.002, decay=0.15, sustain=0.3):
    env = np.clip(np.exp(-t / decay), sustain, 1.0)
    atk_len = max(int(attack * len(t)), 1)
    env[: atk_len] = np.linspace(0, 1, atk_len)
    return env

def nes_lowpass(sig, cutoff=12000, fs=44100):
    b, a = butter(3, cutoff / (fs / 2), btype="low")
    return lfilter(b, a, sig, axis=-1)  # axis=-1 で行ごとにフィルタ

class SquareWave2(WaveGenerator):
    NES_DUTIES = [0.125, 0.25, 0.5, 0.75]

    def __init__(self, duty=0.5):
        if duty not in self.NES_DUTIES:
            raise ValueError(f"duty must be one of {self.NES_DUTIES}")
        self.duty = duty

    def generate(self, freqs, t, sample_rate=44100):
        freqs = np.array(freqs, dtype=float)
        n = len(t)
        env = envelope(t)

        # 周波数 x サンプル の 2D 配列を作る
        phase = (freqs[:, None] * t[None, :]) % 1.0
        wave = np.where(phase < self.duty, 1.0, -1.0)

        # PolyBLEP smoothing
        dt = freqs[:, None] / sample_rate
        wave -= polyblep_vec_2d(phase, dt)
        wave += polyblep_vec_2d((phase - self.duty) % 1.0, dt)

        # Apply envelope & soft clip
        wave *= env
        wave = np.tanh(wave * 1.8)

        # Low-pass filtering (axis=-1: 各周波数ごとにフィルタ)
        wave = nes_lowpass(wave, fs=sample_rate)

        return wave
        
__all__ = [
    "SquareWave2"
]
