import warnings
import numpy as np
from .notes import NOTE_FREQUENCIES
from .part import Part
from .utils import _validate,_play_audio


def quantize_8bit(wave_buffer: np.ndarray) -> np.ndarray:
    """
    Normalize and quantize waveform to 8-bit style.
    """
    max_amp = np.max(np.abs(wave_buffer))
    if max_amp > 0:
        wave_buffer /= max_amp
    wave_buffer_8bit = np.round(wave_buffer * 127).astype(np.int8)
    return (wave_buffer_8bit.astype(np.float32) / 127 * 32767).astype(np.int16)


class SongMixer:
    """
    Mixes multiple Parts into a single song waveform.

    Parameters
    ----------
    parts : list[Part]
        List of Part instances to be mixed.
    sampling_rate : int, optional
        The sampling rate (in Hz) used for playback. Default is 22050 Hz.

    Attributes
    ----------
    parts : list[Part]
        List of parts in the song.
    sampling_rate : int, optional

    _wave : np.ndarray or None
        Cached waveform of the mixed song; None if not synthesized yet.
    total_duration : float
        Total duration of the song in seconds; calculated on demand.

    Methods
    -------
    get_total_duration()
        Compute the total duration of the song in seconds.
    synthesize()
        Generate and mix the waveform from all parts into a single track.
    play()
        Play the mixed waveform using the best available audio backend.



    Notes
    -----
    - All parts must use a WaveGenerator subclass as their generator.
    - Notes not found in NOTE_FREQUENCIES are ignored.
    - Empty melodies produce a silent waveform.

    Examples
    --------
    from your_library import Part, SongMixer, SquareWave

    # Define two parts
    part1 = Part([(['C4'],1),(['E4'],1)], volume=0.5, generator=SquareWave(), first_bpm=120)
    part2 = Part([(['G4'],2)], volume=0.4, generator=SquareWave(), first_bpm=120)

    # Mix and play
    mixer = SongMixer([part1, part2])
    mixer.synthesize()
    mixer.play()
    """
    def __init__(self, parts, sampling_rate=22050):
        if not isinstance(parts, list):
            raise TypeError("parts must be a list")
        elif not all(isinstance(part, Part) for part in parts):
            raise TypeError("all elements of parts must be Part")
        self.parts = parts
        self.sampling_rate = _validate(sampling_rate,int,least_range=0,name="sampling_rate")
        self._wave = None
        self.total_duration = self.get_total_duration()

    def get_total_duration(self) -> float:
        """Get the total duration of the song in seconds."""
        if not self.parts:  # parts が空
            return 0.0

        durations = []
        for part in self.parts:
            if part.events:  # events がある場合のみ
                durations.append(max(e.start_time + e.duration for e in part.events))

        return max(durations, default=0.0)  # durations が空でも 0.0


    def _validate_note(self, note) -> bool:
        if note.upper() not in NOTE_FREQUENCIES:
            warnings.warn(f"Unknown note: {note}")
            return False
        return True

    def synthesize(self) -> np.ndarray:
        """
        Generate and mix the waveform of all parts.

        This method synthesizes each Part's events using its assigned
        WaveGenerator, aligns them in time, applies volume scaling,
        and sums them into a single waveform.

        Returns
        -------
        np.ndarray
            The mixed waveform as an 8-bit quantized NumPy array.

        Notes
        -----
        - Unknown notes are ignored with a warning.
        - Parts with no events are skipped.
        - The generated waveform is cached in `_wave` for reuse.
        """
        total_duration = self.total_duration
        total_samples = int(self.sampling_rate * total_duration)
        wave_buffer = np.zeros(total_samples)

        for part in self.parts:
            for event in part.events:
                start_sample = int(self.sampling_rate * event.start_time)
                end_sample = int(self.sampling_rate * (event.start_time + event.duration))
                num_samples = end_sample - start_sample
                t = np.linspace(0, event.duration, num_samples, endpoint=False)

                if part.wave_generator.using_unique_notes:
                    # freqの代わりにnotesをそのまま渡す
                    freqs = event.notes
                else:
                    freqs = np.array([
                        NOTE_FREQUENCIES[note.upper()]
                        for note in event.notes
                        if self._validate_note(note)
                        and NOTE_FREQUENCIES[note.upper()] > 0
                    ])

                if len(freqs) == 0:
                    continue

                waves = part.wave_generator.generate(freqs, t)
                wave_sum = waves.sum(axis=0) * (0.01 + 0.07 * part.volume) # 合計&音量調整
                wave_buffer[start_sample:end_sample] += wave_sum

        self._wave = quantize_8bit(wave_buffer)
        return self._wave

    def play(self):
        """
        Play the mixed song waveform.

        If the waveform has not been synthesized yet, this method calls
        `synthesize()` automatically before playback.

        Returns
        -------
        IPython.display.Audio or None
            - In Jupyter/Colab environments, returns an Audio widget
            for inline playback.
            - In other environments, plays audio using `sounddevice` or
            `simpleaudio` if available, and returns None.

        Notes
        -----
        - If no playback backend is available, a warning is issued.
        - For inline playback in notebooks, install `IPython`.
        - For local playback outside notebooks, install `sounddevice`
        or `simpleaudio`.
        """
        if self._wave is None:
            self.synthesize()
        return _play_audio(self._wave, sr=self.sampling_rate)
