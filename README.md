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

The project is configured for automatic deployment through GitHub Actions.

How it works:
- each push to `main` runs `.github/workflows/deploy-pages.yml`
- workflow installs `pygame-ce` and `pygbag`
- workflow builds the web bundle with `python -m pygbag --build .`
- built files from `build/web` are published to `gh-pages` branch

One-time repository setup:
1. open `Settings -> Pages`
2. in `Build and deployment`, choose `Deploy from a branch`
3. select branch `gh-pages` and folder `/ (root)`
4. save

After a successful run, the game should be available at:

`https://aneq05.github.io/Boring_lectures_game/`

If deployment fails:
1. open `Actions` and inspect the latest `Deploy to GitHub Pages` run
2. confirm `Settings -> Actions -> General -> Workflow permissions` allows write access
3. run workflow manually from `Actions -> Deploy to GitHub Pages -> Run workflow`

## Project structure

- `main.py` - entry point
- `src/` - game code (logic, UI, config)
- `assets/` - icons and static resources
- `tests/` - gameplay tests
