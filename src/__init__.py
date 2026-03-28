"""
Let Me Tango - Logiczna gra puzzle inspirowana sudoku i binarnym puzzlem.

To jest główna paczka projektu zawierająca wszystkie moduły gry.
"""

# Metadane projektu
__version__ = "0.1.0"
__author__ = "Your Name"
__title__ = "Let Me Tango"
__description__ = "Puzzle game z symbolami słońca i księżyca"

# Eksport głównych klas dla wygody
from .game_manager import Game
from .config import GameSettings, GameConfig

__all__ = [
    'Game',
    'GameSettings',
    'GameConfig',
    '__version__',
    '__title__'
]