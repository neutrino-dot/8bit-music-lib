# Changelog

すべての重要な変更はこのファイルに記録されます。

フォーマットは [Keep a Changelog](https://keepachangelog.com/ja/1.1.0/) に準拠し、
バージョン管理には [Semantic Versioning](https://semver.org/lang/ja/) を使用します。

---
## [Unreleased]

### Added
- Added `expansion` folder
- Added NES-style waveform functions in `nes_waves.py`
- Added `helper.py` with MML and MIDI support
---
## [v0.2.1] - 2025-10-24

### Changed  
- `core.py` に含まれていた主要なコンポーネントを、保守性向上のため複数ファイルに分割：  
  - `NOTE_FREQUENCIES` 辞書と `NoteEvent` クラスを `notes.py` へ移動  
  - `Part` クラスを `part.py` へ移動  
  - `SongMixer` クラスを `mixer.py` へ移動  
- `utils.py` 内の `_validate` 関数を、適切な箇所で使用するよう更新  

### Removed  
- `SongConfig` クラスを削除（機能は他の部分に統合済み）。

---
## [v0.2.0] - 2025-10-23

### Added
- `DrumWave` クラスを追加
- 独自音階を用いるクラスにパラメーター `using_unique_notes` を追加
- `NoiseWave` クラスにノイズの長さを調整する引数 `decay_rate` を追加

### Changed
- `README.md` や `README_ja.md` から使用方法を削除、代わりに GitHub の wiki ページに移動
- `Part` クラスの引数をキーワード専用引数に固定
- `SongMixer` クラスの docstring を変更

### Fixed
- 基底クラス `WaveGenerator` と継承先の波形クラスの引数の違いを修正
- `utils.py` にある内部用関数の名前を修正

---
## [v0.1.1] - 2025-10-07

### Fixed
- `README.md` と `README_ja.md` の誤りとわかりにくい部分を修正

---
## [v0.1.0] - 2025-09-19

### Added
- 初回リリース（`8bit-music-lib` コア機能）
