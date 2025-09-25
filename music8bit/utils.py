import numpy as np
import warnings

def play_audio(wave: np.ndarray, sr: int = 22050):
    """
    環境に応じて自動で再生方式を切り替える
    """
    # Colab や Jupyter Notebook なら IPython.display.Audio を優先
    try:
        from IPython.display import Audio
        return Audio(wave, rate=sr)
    except ImportError:
        pass

    # sounddevice が使えるならそっち
    try:
        import sounddevice as sd
        sd.play(wave, sr)
        sd.wait()
        return None
    except ImportError:
        pass

    # simpleaudio も候補
    try:
        import simpleaudio as sa
        # 16bit整数に変換
        wave_int16 = np.int16(wave / np.max(np.abs(wave)) * 32767)
        sa.play_buffer(wave_int16, 1, 2, sr)
        return None
    except ImportError:
        pass

    warnings.warn("No available audio playback method found.")
    return None
