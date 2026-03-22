"""
Utils - narzędzia pomocnicze dla projektu Let Me Tango.

Zawiera:
- Definicje kolorów (BasicColors, ThemeColors, UIColors)
- W przyszłości: dekoratory, validatory, helpery

Przykład użycia:
    from src.utils import BasicColors, ThemeColors
    screen.fill(BasicColors.WHITE.value)
"""
from .colors import BasicColors, ThemeColors, UIColors

# Metadane modułu
__version__ = "1.0.0"

__all__ = [
    'BasicColors',
    'ThemeColors', 
    'UIColors'
]

