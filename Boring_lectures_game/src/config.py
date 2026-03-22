"""
Konfiguracja gry - poziomy trudności, rozmiary planszy, motywy
"""
from enum import Enum
from typing import Dict


class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class BoardSize(Enum):
    SMALL = 4    # 4x4
    MEDIUM = 6   # 6x6
    LARGE = 8    # 8x8
    XLARGE = 10  # 10x10


class Theme(Enum):
    SUN_MOON = "sun_moon"
    CAT_DOG = "cat_dog"
    CIRCLE_SQUARE = "circle_square"
    APPLE_ORANGE = "apple_orange"


class GameConfig:
    """Globalna konfiguracja dostępnych opcji gry"""

    DIFFICULTY_SETTINGS: Dict[Difficulty, Dict] = {
        Difficulty.EASY: {
            "name": "Łatwy",
            "description": "40% komórek do wypełnienia",
            "remove_percent": 0.40,
            "hints_available": 5,
            "color": (100, 255, 100)  # green
        },
        Difficulty.MEDIUM: {
            "name": "Średni",
            "description": "55% komórek do wypełnienia",
            "remove_percent": 0.55,
            "hints_available": 3,
            "color": (255, 215, 0)  # yellow
        },
        Difficulty.HARD: {
            "name": "Trudny",
            "description": "70% komórek do wypełnienia",
            "remove_percent": 0.70,
            "hints_available": 2,
            "color": (255, 140, 0)  # orange
        },
        Difficulty.EXPERT: {
            "name": "Ekspert",
            "description": "75%+ komórek do wypełnienia",
            "remove_percent": 0.75,
            "hints_available": 1,
            "color": (255, 69, 0)  # red
        }
    }

    BOARD_SIZE_SETTINGS: Dict[BoardSize, Dict] = {
        BoardSize.SMALL: {
            "name": "Mała (4×4)",
            "size": 4,
            "cell_size": 90,
            "description": "Idealna dla początkujących"
        },
        BoardSize.MEDIUM: {
            "name": "Średnia (6×6)",
            "size": 6,
            "cell_size": 70,
            "description": "Standardowy rozmiar"
        },
        BoardSize.LARGE: {
            "name": "Duża (8×8)",
            "size": 8,
            "cell_size": 55,
            "description": "Większe wyzwanie"
        },
        BoardSize.XLARGE: {
            "name": "Bardzo duża (10×10)",
            "size": 10,
            "cell_size": 45,
            "description": "Dla ekspertów"
        }
    }

    THEME_SETTINGS: Dict[Theme, Dict] = {
        Theme.SUN_MOON: {
            "name": "Słońce & Księżyc",
            "icon1": "sun.png",
            "icon2": "moon.png",
            "icon1_fallback": "yellow_circle",
            "icon2_fallback": "blue_circle",
            "description": "Klasyczny motyw"
        },
        Theme.CAT_DOG: {
            "name": "Kot & Pies",
            "icon1": "cat.png",
            "icon2": "dog.png",
            "icon1_fallback": "brown_circle",
            "icon2_fallback": "gray_circle",
            "description": "Zwierzątka"
        },
        Theme.CIRCLE_SQUARE: {
            "name": "Kółko & Kwadrat",
            "icon1": "circle.png",
            "icon2": "square.png",
            "icon1_fallback": "white_circle",
            "icon2_fallback": "black_square",
            "description": "Kształty geometryczne"
        },
        Theme.APPLE_ORANGE: {
            "name": "Jabłko & Pomarańcza",
            "icon1": "apple.png",
            "icon2": "orange.png",
            "icon1_fallback": "red_circle",
            "icon2_fallback": "orange_circle",
            "description": "Owoce"
        }
    }

    # Default settings
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
    """
    Klasa przechowująca wybrane ustawienia gry przez gracza.
    """

    def __init__(
        self,
        difficulty: Difficulty = GameConfig.DEFAULT_DIFFICULTY,
        board_size: BoardSize = GameConfig.DEFAULT_BOARD_SIZE,
        theme: Theme = GameConfig.DEFAULT_THEME
    ):
        self.difficulty = difficulty
        self.board_size = board_size
        self.theme = theme

        # Pobierz szczegóły z konfiguracji
        self.size = GameConfig.BOARD_SIZE_SETTINGS[board_size]["size"]
        self.cell_size = GameConfig.BOARD_SIZE_SETTINGS[board_size]["cell_size"]
        self.remove_percent = GameConfig.DIFFICULTY_SETTINGS[difficulty]["remove_percent"]
        self.hints_available = GameConfig.DIFFICULTY_SETTINGS[difficulty]["hints_available"]

        # Ustawienia okna
        self.window_width = 600
        self.window_height = 700
        self.fps = 60
        self.icon_scale = 0.7

        # Oblicz offset siatki aby wycentrować
        grid_width = self.size * self.cell_size
        self.grid_offset_x = (self.window_width - grid_width) // 2
        self.grid_offset_y = 150

    def __repr__(self):
        return (f"GameSettings(difficulty={self.difficulty.value}, "
                f"size={self.size}x{self.size}, theme={self.theme.value})")
