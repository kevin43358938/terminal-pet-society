# Changelog

All notable changes to Terminal Pet Society.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.2.1] — 2026-08-08

### Fixed
- **Ghost Port**: `--port` argument was ignored; port now propagates correctly through the full call chain (`main → run_tui/run_server_only → setup_network → PetServer`)
- **UX lazy-load**: multiple saved pets now show a numbered selection menu instead of blindly loading the first one
- **Dead imports**: removed unused `get_setting`/`set_setting` from `main.py` imports
- **Lazy import**: `TerminalUI` import moved to module level (PEP8 compliance)

[3.2.1]: https://github.com/kevin43358938/terminal-pet-society/compare/v3.2.0...v3.2.1

## [3.2.0] — 2026-08-07

### Changed
- **Detailed chunky pixel art**: 6-7 line sprites with block characters (▄▀█▌▐)
- Recognizable features: cat ears/whiskers/tail, dog floppy body, dragon wings
- Species-specific details: robot double-border, unicorn triple-horn, ghost wavy bottom
- Round face eyes (◉◉) with 10 mood variations
- 2-frame idle blink animation (◉◉ → ⊙⊙)

[3.2.0]: https://github.com/kevin43358938/terminal-pet-society/compare/v3.1.0...v3.2.0

## [3.1.0] — 2026-08-07

### Changed
- **Minimal Iconic ASCII style**: 3-4 line sprites, classic internet aesthetic
- Clean simple characters only: `/\()..-_~'"` — no box-drawing glyphs
- Consistent body per species, 10 mood faces, 2-frame idle blink
- Decor elements per species (cat=🍖, dog=🦴, dragon=🔥, unicorn=🌈)
- 132 lines of code (down from 972 in v3.0.0)

[3.1.0]: https://github.com/kevin43358938/terminal-pet-society/compare/v3.0.0...v3.1.0

## [3.0.0] — 2026-08-07

### Changed
- **Template-based sprite system**: fixed body per species, interchangeable faces for 10 moods
- Zero Unicode box-drawing glyphs: only classic ASCII (`/\()..-_~'"`)
- Works on any terminal, any font, any OS

[3.0.0]: https://github.com/kevin43358938/terminal-pet-society/compare/v2.1.0...v3.0.0

## [2.1.0] — 2026-08-07

### Changed
- Larger, more recognizable ASCII sprites (7–8 lines each)
- Clear body structure for every species: head, body, limbs, tail
- Cat: sitting posture, triangle ears, curved tail
- Dog: floppy ears, sturdy body, visible paws
- Dragon: spread wings, spiky tail
- Ghost: classic sheet shape with wavy bottom and tiny arms
- Robot: box body with antenna and screen face
- Unicorn: spiral horn, flowing mane
- Penguin: chubby body, flippers, tiny feet

## [2.0.0] — 2026-08-07

### Added
- Rich-powered Terminal UI replacing curses
- Bordered panels (sportelli) with rounded corners via `rich.Panel`
- Dynamic mood-colored borders (green=happy, red=sad, blue=sleepy…)
- Animated `ProgressBar` for all stats and traits
- Real-time `Live` rendering at 15 FPS
- Kawaii-style sprite redesign (88 frames, 8 species × 10 moods)
- 2-frame idle blink animations for all species
- Two new species: Unicorn 🦄 and Penguin 🐧

### Changed
- Rewrote `tui.py` from curses to Rich (complete rewrite, 250+ LOC)
- Updated `requirements.txt` to require `rich>=13.0.0`
- Mood enum extended to 11 values (added `talkative`)

## [1.0.0] — 2026-08-07

### Added
- Initial release with curses-based TUI
- 6 species: Cat, Dog, Dragon, Slime, Ghost, Robot
- 7-stage evolution system (Egg → Legendary)
- Data-driven command learning from shell history
- 6 personality traits (Discipline, Creativity, Social, Curiosity, Aggression, Laziness)
- P2P pet visits over TCP (port 19997)
- UDP multicast auto-discovery
- SQLite persistence
- 33 unit tests
- Zero external dependencies (stdlib only)

[2.1.0]: https://github.com/kevin43358938/terminal-pet-society/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/kevin43358938/terminal-pet-society/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/kevin43358938/terminal-pet-society/releases/tag/v1.0.0

