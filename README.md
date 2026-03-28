# Boring Lectures Game

A modern logic puzzle game made with `Python` and `Pygame`.

The game focuses on clean gameplay and a friendly UI:
- soft, rounded interface with smooth transitions
- board size, difficulty, and visual theme selection
- generated puzzles with rule validation
- undo/redo, hints, reset, and win summary popup

## Requirements

- Python `3.10+`
- `pygame`
- `pytest` (for test execution)

## Install

```bash
pip install pygame pytest
```

## Run

```bash
python main.py
```

## Controls

- `Left click` - cycle cell value
- `Right click` - clear cell
- `U` - undo
- `Y` - redo
- `H` - hint
- `R` - reset board
- `C` - check current board
- `N` - new game
- `ESC` - exit

## Tests

```bash
python -m pytest -q
```

## Project structure

- `main.py` - entry point
- `src/` - game code (logic, UI, config)
- `assets/` - icons and static resources
- `tests/` - gameplay tests
