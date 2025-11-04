import numbers
from .notes import NoteEvent
from .wave import WaveGenerator
from .utils import _validate


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
