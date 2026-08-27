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

Test suite contains **87 tests** organized in two categories:

### Test Structure

```
tests/
├── sct/                    # System/Component Tests (9 tests)
│   └── test_gameplay_core.py - Integration tests for board generation, gameplay, and solver
├── ut/                     # Unit Tests (78 tests)
│   ├── board/              - Board logic, generation, cell manipulation
│   ├── cell/               - Cell state management and toggling
│   ├── core/               - Constraints, validator, solver algorithms
│   ├── ui/                 - UI components rendering and styling
│   ├── utils/              - Utilities (timer, move history, colors)
│   ├── test_config.py      - GameSettings and configuration logic
│   └── test_game_manager.py - Main game manager
```

### Running Tests

**All tests:**
```bash
python -m pytest tests/ -q
```

**Unit tests only:**
```bash
python -m pytest tests/ut/ -v
```

**System/Component tests only:**
```bash
python -m pytest tests/sct/ -v
```

**Specific test file:**
```bash
python -m pytest tests/ut/board/test_board.py -v
```

**Coverage report:**
```bash
python -m pytest tests/ --cov=src
```

### Test Categories

- **SCT (System Component Tests)**: Integration tests verifying board generation pipeline, gameplay interactions, and solver functionality with real constraints
- **UT (Unit Tests)**: Isolated tests for individual modules and classes without external dependencies

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
