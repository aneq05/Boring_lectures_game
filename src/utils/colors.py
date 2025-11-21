from enum import Enum


class BasicColors(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    DARK_GRAY = (100, 100, 100)
    LIGHT_GRAY = (240, 240, 240)


class ThemeColors(Enum):
    LIGHT_BLUE = (173, 216, 230)
    BLUE = (100, 149, 237)
    YELLOW = (255, 215, 0)
    RED = (255, 100, 100)
    GREEN = (100, 255, 100)
    BROWN = (139, 69, 19)
    ORANGE = (255, 140, 0)


class UIColors(Enum):
    BACKGROUND = BasicColors.WHITE.value
    TEXT_COLOR = BasicColors.BLACK.value
    BORDER_COLOR = BasicColors.BLACK.value
    ERROR_COLOR = ThemeColors.RED.value
    SUCCESS_COLOR = ThemeColors.GREEN.value
    FIXED_CELL_COLOR = BasicColors.LIGHT_GRAY.value
    HOVER_COLOR = ThemeColors.LIGHT_BLUE.value
