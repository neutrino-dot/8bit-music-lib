import numpy as np
import warnings
def _play_audio(wave: np.ndarray, sr: int = 22050):
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

def _validate(value, expected_type, least_range=None, most_range=None, name="value"):
    """ある変数が期待通りの型でかつそれが範囲内に入っているかを調べる関数"""
    # 型チェック
    if not isinstance(value, expected_type):
        # expected_type がタプルなら型名をまとめる
        if isinstance(expected_type, tuple):
            type_names = ", ".join(t.__name__ for t in expected_type)
        else:
            type_names = expected_type.__name__
        raise TypeError(f"{name} must be {type_names}, got {type(value).__name__}")

    # 数値型なら範囲チェック（int, float など）
    if isinstance(value, (int,float)):
        if least_range is not None and value < least_range:
            raise ValueError(f"{name} must be >= {least_range}, got {value}")
        if most_range is not None and value > most_range:
            raise ValueError(f"{name} must be <= {most_range}, got {value}")

    return value
