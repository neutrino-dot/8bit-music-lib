# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---
## [Unreleased]

### Added
- Added `expansion` folder
- Added NES-style waveform functions in `nes_waves.py`
- Added `helper.py` with MML and MIDI support

---
## [v0.2.0] - 2025-10-23

### Added
- Added `DrumWave` class
- Added parameter `using_unique_notes` for classes using unique note sets
- Added argument `decay_rate` in `NoiseWave` class to control noise decay length

### Changed
- Made `Part` class arguments keyword-only
- Updated docstring in `SongMixer` class

### Removed
- Removed usage examples from `README.md` and `README_ja.md`, moved them to the GitHub wiki

### Fixed
- Fixed inconsistencies in `generator` method arguments between `WaveGenerator` base class and subclasses
- Renamed some internal helper functions in `utils.py`

---
## [v0.1.1] - 2025-10-07

### Fixed
- Corrected typos and unclear descriptions in `README.md` and `README_ja.md`

---
## [v0.1.0] - 2025-09-19

### Added
- Initial release of core features (`8bit-music-lib`)
