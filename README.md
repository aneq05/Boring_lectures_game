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

## Deploy to GitHub Pages

The project is configured for automatic web deployment through GitHub Actions.

How it works:
- on each push to `main`, workflow `.github/workflows/deploy-pages.yml` runs
- workflow installs `pygame-ce` and `pygbag`
- workflow builds a browser bundle with `python -m pygbag --build .`
- `build/web` is uploaded and published via `actions/deploy-pages`

After a successful run, the game is available at:

`https://aneq05.github.io/Boring_lectures_game/`

If deployment fails:
1. open repo `Actions` tab and inspect the latest `Deploy to GitHub Pages` run
2. verify repo `Settings -> Pages` is set to `Build and deployment: GitHub Actions`
3. re-run workflow from `Actions -> Deploy to GitHub Pages -> Run workflow`

## Project structure

- `main.py` - entry point
- `src/` - game code (logic, UI, config)
- `assets/` - icons and static resources
- `tests/` - gameplay tests
