"""Core package for the Let Me Tango game."""

__version__ = "0.1.0"
__author__ = "Your Name"
__title__ = "Let Me Tango"
__description__ = "Puzzle game with two opposing symbols."

from .config import GameConfig, GameSettings
from .game_manager import Game

__all__ = ["Game", "GameSettings", "GameConfig", "__version__", "__title__"]
