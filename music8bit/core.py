import warnings
import numbers
import numpy as np
from dataclasses import dataclass
from .utils import _play_audio,_validate
from .wave import WaveGenerator
from .notes import NOTE_FREQUENCIES


# -------------------------
# Global configuration
# -------------------------
class SongConfig:
    """Mapping from note names (C4, D#5, etc.) to frequencies in Hz. 'R' represents rest (0 Hz)."""

    @staticmethod
    def map_volume(user_vol: float) -> float:
        """
        Map user volume from 0.0-1.0 to 0.01-0.08 range.
        """
        min_v, max_v = 0.01, 0.08
        return min_v + (max_v - min_v) * user_vol

    @staticmethod
    def quantize_8bit(wave_buffer: np.ndarray) -> np.ndarray:
        """
        Normalize and quantize waveform to 8-bit style.
        """
        max_amp = np.max(np.abs(wave_buffer))
        if max_amp > 0:
            wave_buffer /= max_amp
        wave_buffer_8bit = np.round(wave_buffer * 127).astype(np.int8)
        return (wave_buffer_8bit.astype(np.float32) / 127 * 32767).astype(np.int16)




# -------------------------
# NoteEvent
# -------------------------

@dataclass(slots=True)
class NoteEvent:
    """
    Represents a single note event with start time, duration, and notes.
    """
    start_time: float
    duration: float
    notes: list[str]




# -------------------------
# Part
# -------------------------
class Part:
    """
    A single musical part consisting of a melody sequence, a waveform generator,
    and playback settings.

    Parameters
    ----------
    melody : list of tuples or str
        Melody sequence. You can provide a list of (notes, beat) tuples, e.g.:
        [(['C4'], 1), (['E4','E5'], 1), (['G4'], 2), (['R'], 1), (['BPM'], 90)]
    volume : float
        Volume of the part (0.0 to 1.0).
    generator : WaveGenerator
        An instance of a waveform generator (e.g., SquareWave(), TriangleWave(), NoiseWave()).
    first_bpm : float
        The initial tempo in beats per minute.

    Attributes
    ----------
    bpm : float
        Current BPM of the part, updated if BPM change events occur.
    volume : float
        Volume of the part.
    wave_generator : WaveGenerator
        The waveform generator used to create the sound.
    events : list of NoteEvent
        Scheduled note events (with start time, duration, and notes).
    total_beat : float
        Total number of beats in the melody (ignores BPM changes).

    Notes
    -----
    - Rest notes ("R") are treated as silence.
    - BPM change events ("BPM",value) affect subsequent durations.

    Examples
    --------
    from your_library import Part, SquareWave


    melody = [(['C4'], 1), (['E4','E5'], 1), (['G4'], 2), (['R'], 1), (['BPM'], 90)]

    part = Part(melody, volume=0.5, generator=SquareWave(), first_bpm=120)
    """
    def __init__(self, *, melody, volume=0.5, generator:"WaveGenerator", first_bpm=120):
        # 自動判定
        if not isinstance(melody, list):
            raise TypeError("melody must be a list")
        elif not all(isinstance(item, tuple) and len(item) == 2 for item in melody):
            for i, item in enumerate(melody):
              if not isinstance(item, tuple):
                  raise TypeError(f"melody[{i}] must be tuple, got {type(item).__name__}")
              if len(item) != 2:
                  raise TypeError(f"melody[{i}] must have length 2, got {len(item)}")

        self.bpm = _validate(first_bpm,numbers.Real,least_range=0.01,name="first_bpm")
        self.volume = _validate(volume,numbers.Real,least_range=0.0,name="volume")
        self.wave_generator = _validate(generator, WaveGenerator, name="generator")
        self.events = self.schedule(melody)
        self.total_beat = self.get_total_beat(melody)

    def schedule(self, melody):
        events = []
        current_time = 0.0
        current_bpm = self.bpm
        for notes, beat in melody:
            if notes == "BPM":
                current_bpm = _validate(float(beat), numbers.Real, least_range=1, name="BPM")
                continue
            duration = beat * (60 / current_bpm)
            events.append(NoteEvent(current_time, duration, notes))
            current_time += duration
        return events

    def get_total_beat(self, melody):
        return sum(beat for notes,beat in melody if notes != "BPM")



# -------------------------
# SongMixer
# -------------------------
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
    - Notes not found in SongConfig.NOTE_FREQUENCIES are ignored.
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
        if note.upper() not in SongConfig.NOTE_FREQUENCIES:
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
                        SongConfig.NOTE_FREQUENCIES[note.upper()]
                        for note in event.notes
                        if self._validate_note(note)
                        and SongConfig.NOTE_FREQUENCIES[note.upper()] > 0
                    ])

                if len(freqs) == 0:
                    continue

                waves = part.wave_generator.generate(freqs, t)
                wave_sum = waves.sum(axis=0) * SongConfig.map_volume(part.volume)
                wave_buffer[start_sample:end_sample] += wave_sum

        self._wave = SongConfig.quantize_8bit(wave_buffer)
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
