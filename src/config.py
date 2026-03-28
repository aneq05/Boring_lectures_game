"""
Konfiguracja gry - poziomy trudnosci, rozmiary planszy i motywy.
"""
from enum import Enum
from typing import Dict


class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class BoardSize(Enum):
    SMALL = 4
    MEDIUM = 6
    LARGE = 8
    XLARGE = 10


class Theme(Enum):
    SUN_MOON = "sun_moon"
    CAT_DOG = "cat_dog"
    CIRCLE_SQUARE = "circle_square"
    APPLE_ORANGE = "apple_orange"


class GameConfig:
    """Globalna konfiguracja dostepnych opcji gry."""

    DIFFICULTY_SETTINGS: Dict[Difficulty, Dict] = {
        Difficulty.EASY: {
            "name": "Latwy",
            "description": "40% komorek do wypelnienia",
            "remove_percent": 0.40,
            "hints_available": 5,
            "color": (100, 255, 100),
        },
        Difficulty.MEDIUM: {
            "name": "Sredni",
            "description": "55% komorek do wypelnienia",
            "remove_percent": 0.55,
            "hints_available": 3,
            "color": (255, 215, 0),
        },
        Difficulty.HARD: {
            "name": "Trudny",
            "description": "70% komorek do wypelnienia",
            "remove_percent": 0.70,
            "hints_available": 2,
            "color": (255, 140, 0),
        },
        Difficulty.EXPERT: {
            "name": "Ekspert",
            "description": "75%+ komorek do wypelnienia",
            "remove_percent": 0.75,
            "hints_available": 1,
            "color": (255, 69, 0),
        },
    }

    BOARD_SIZE_SETTINGS: Dict[BoardSize, Dict] = {
        BoardSize.SMALL: {
            "name": "Mala (4x4)",
            "size": 4,
            "cell_size": 100,
            "description": "Idealna na szybka gre",
        },
        BoardSize.MEDIUM: {
            "name": "Srednia (6x6)",
            "size": 6,
            "cell_size": 78,
            "description": "Najbardziej klasyczny wariant",
        },
        BoardSize.LARGE: {
            "name": "Duza (8x8)",
            "size": 8,
            "cell_size": 62,
            "description": "Wiecej analizy i mniej oczywistych ruchow",
        },
        BoardSize.XLARGE: {
            "name": "Bardzo duza (10x10)",
            "size": 10,
            "cell_size": 50,
            "description": "Tryb dla cierpliwych strategow",
        },
    }

    THEME_SETTINGS: Dict[Theme, Dict] = {
        Theme.SUN_MOON: {
            "name": "Slonce i Ksiezyc",
            "icon1": "sun.png",
            "icon2": "moon.png",
            "icon1_fallback": "yellow_circle",
            "icon2_fallback": "blue_circle",
            "description": "Klasyczny motyw",
        },
        Theme.CAT_DOG: {
            "name": "Kot i Pies",
            "icon1": "cat.png",
            "icon2": "dog.png",
            "icon1_fallback": "brown_circle",
            "icon2_fallback": "gray_circle",
            "description": "Zwierzaki na planszy",
        },
        Theme.CIRCLE_SQUARE: {
            "name": "Kolko i Kwadrat",
            "icon1": "circle.png",
            "icon2": "square.png",
            "icon1_fallback": "white_circle",
            "icon2_fallback": "black_square",
            "description": "Geometryczny zestaw",
        },
        Theme.APPLE_ORANGE: {
            "name": "Jablko i Pomarancza",
            "icon1": "apple.png",
            "icon2": "orange.png",
            "icon1_fallback": "red_circle",
            "icon2_fallback": "orange_circle",
            "description": "Owocowy wariant",
        },
    }

    DEFAULT_DIFFICULTY = Difficulty.MEDIUM
    DEFAULT_BOARD_SIZE = BoardSize.MEDIUM
    DEFAULT_THEME = Theme.SUN_MOON

    @staticmethod
    def get_difficulty_name(difficulty: Difficulty) -> str:
        return GameConfig.DIFFICULTY_SETTINGS[difficulty]["name"]

    @staticmethod
    def get_board_size_value(board_size: BoardSize) -> int:
        return GameConfig.BOARD_SIZE_SETTINGS[board_size]["size"]

    @staticmethod
    def get_theme_name(theme: Theme) -> str:
        return GameConfig.THEME_SETTINGS[theme]["name"]


class GameSettings:
    """Przechowuje wybrane ustawienia rozgrywki."""

    def __init__(
        self,
        difficulty: Difficulty = GameConfig.DEFAULT_DIFFICULTY,
        board_size: BoardSize = GameConfig.DEFAULT_BOARD_SIZE,
        theme: Theme = GameConfig.DEFAULT_THEME,
    ):
        self.difficulty = difficulty
        self.board_size = board_size
        self.theme = theme

        self.size = GameConfig.BOARD_SIZE_SETTINGS[board_size]["size"]
        self.cell_size = GameConfig.BOARD_SIZE_SETTINGS[board_size]["cell_size"]
        self.remove_percent = GameConfig.DIFFICULTY_SETTINGS[difficulty]["remove_percent"]
        self.hints_available = GameConfig.DIFFICULTY_SETTINGS[difficulty]["hints_available"]

        self.window_width = 1024
        self.window_height = 760
        self.fps = 60
        self.icon_scale = 0.62

        grid_width = self.size * self.cell_size
        self.grid_offset_x = 48
        self.grid_offset_y = 130
        self.toolbar_y = self.grid_offset_y + grid_width + 24
        self.sidebar_x = self.grid_offset_x + grid_width + 40
        self.sidebar_width = self.window_width - self.sidebar_x - 40
        self.sidebar_height = min(grid_width, self.window_height - self.grid_offset_y - 40)

    def __repr__(self):
        return (
            f"GameSettings(difficulty={self.difficulty.value}, "
            f"size={self.size}x{self.size}, theme={self.theme.value})"
        )
