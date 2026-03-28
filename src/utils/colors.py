from enum import Enum


class BasicColors(Enum):
    WHITE = (255, 255, 255)
    BLACK = (48, 47, 61)
    GRAY = (176, 175, 190)
    DARK_GRAY = (98, 97, 120)
    LIGHT_GRAY = (246, 242, 248)
    CREAM = (255, 248, 245)


class ThemeColors(Enum):
    LIGHT_BLUE = (212, 236, 255)
    BLUE = (112, 178, 218)
    NAVY = (75, 113, 154)
    YELLOW = (255, 214, 166)
    RED = (255, 124, 146)
    GREEN = (125, 201, 168)
    BROWN = (192, 134, 112)
    ORANGE = (255, 167, 133)


class UIColors(Enum):
    BACKGROUND = (255, 245, 249)
    PANEL_BACKGROUND = (255, 255, 255)
    TEXT_COLOR = BasicColors.BLACK.value
    MUTED_TEXT = BasicColors.DARK_GRAY.value
    BORDER_COLOR = (244, 207, 223)
    ERROR_COLOR = ThemeColors.RED.value
    SUCCESS_COLOR = ThemeColors.GREEN.value
    FIXED_CELL_COLOR = (255, 234, 243)
    HOVER_COLOR = (255, 236, 244)
    SELECTED_COLOR = (255, 223, 236)
    GRID_BACKGROUND = (255, 250, 247)
    SHADOW = (238, 192, 214)
