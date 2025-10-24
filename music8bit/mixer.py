import warnings
import numpy as np
from .notes import NOTE_FREQUENCIES
from .part import Part
from .utils import _validate,_play_audio


class SongConfig:
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


class SongMixer:
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
                wave_sum = waves.sum(axis=0) * SongConfig.map_volume(part.volume)
                wave_buffer[start_sample:end_sample] += wave_sum

        self._wave = SongConfig.quantize_8bit(wave_buffer)
        return self._wave

    def play(self):
        if self._wave is None:
            self.synthesize()
        return _play_audio(self._wave, sr=self.sampling_rate)
