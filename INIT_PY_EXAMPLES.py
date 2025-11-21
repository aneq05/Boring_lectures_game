"""
Let Me Tango - przykłady użycia __init__.py

Ten plik pokazuje różne zastosowania __init__.py w projekcie.
"""

# ============================================================
# PRZYKŁAD 1: Podstawowy re-export (już masz w projekcie)
# ============================================================
# src/utils/__init__.py

from .colors import BasicColors, ThemeColors, UIColors

__all__ = ['BasicColors', 'ThemeColors', 'UIColors']

# Użycie:
# from src.utils import BasicColors  # Zamiast: from src.utils.colors import BasicColors


# ============================================================
# PRZYKŁAD 2: Grupowanie komponentów (już masz w projekcie)
# ============================================================
# src/ui/menu/components/__init__.py

from .button import Button
from .selector import Selector
from .label import Label
from .info_box import InfoBox

__all__ = ['Button', 'Selector', 'Label', 'InfoBox']

# Użycie:
# from src.ui.menu.components import Button, Selector  # Wszystko w jednym miejscu!


# ============================================================
# PRZYKŁAD 3: Metadane projektu
# ============================================================
# src/__init__.py (propozycja rozszerzenia)

"""
Let Me Tango - Logiczna gra puzzle.

Główna paczka projektu zawierająca wszystkie moduły gry.
"""
__version__ = "0.1.0"
__author__ = "Twoje Imię"
__description__ = "Puzzle game inspirowany logiką binarną"

# Użycie:
# from src import __version__
# print(f"Gra v{__version__}")


# ============================================================
# PRZYKŁAD 4: Stałe konfiguracyjne na poziomie paczki
# ============================================================
# src/config/__init__.py (propozycja)

from .settings import GameSettings, GameConfig
from .enums import Difficulty, BoardSize, Theme

# Stałe domyślne dostępne globalnie
DEFAULT_WINDOW_SIZE = (600, 700)
DEFAULT_FPS = 60
GAME_TITLE = "Let Me Tango"

__all__ = [
    'GameSettings',
    'GameConfig',
    'Difficulty',
    'BoardSize',
    'Theme',
    'DEFAULT_WINDOW_SIZE',
    'DEFAULT_FPS',
    'GAME_TITLE'
]

# Użycie:
# from src.config import DEFAULT_FPS, GAME_TITLE


# ============================================================
# PRZYKŁAD 5: Inicjalizacja loggera dla całej paczki
# ============================================================
# src/game/__init__.py (propozycja)

import logging

# Stwórz logger dla całej paczki game
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Handler (opcjonalnie)
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(_handler)

from .game_manager import Game

__all__ = ['Game', 'logger']

# Użycie w innych modułach w game/:
# from . import logger
# logger.info("Gra rozpoczęta!")


# ============================================================
# PRZYKŁAD 6: Lazy loading (dla ciężkich zasobów)
# ============================================================
# src/assets/__init__.py (propozycja)

"""Assets module - zarządzanie zasobami gry."""

# NIE ładuj od razu wszystkich obrazków!
_icons = None
_sounds = None

def get_icons():
    """Lazy loading ikon - ładuje tylko gdy potrzebne."""
    global _icons
    if _icons is None:
        import pygame
        from pathlib import Path
        
        icons_path = Path("assets/images/icons")
        _icons = {
            "sun": pygame.image.load(icons_path / "sun.png"),
            "moon": pygame.image.load(icons_path / "moon.png")
        }
    return _icons

def get_sounds():
    """Lazy loading dźwięków - ładuje tylko gdy potrzebne."""
    global _sounds
    if _sounds is None:
        import pygame.mixer
        from pathlib import Path
        
        sounds_path = Path("assets/sounds")
        _sounds = {
            "click": pygame.mixer.Sound(sounds_path / "click.wav"),
            "success": pygame.mixer.Sound(sounds_path / "success.wav")
        }
    return _sounds

__all__ = ['get_icons', 'get_sounds']

# Użycie:
# from src.assets import get_icons
# icons = get_icons()  # Ładuje się dopiero tutaj!


# ============================================================
# PRZYKŁAD 7: Warunkowe importy (cross-platform)
# ============================================================
# src/platform/__init__.py (propozycja)

import sys
import os

# Różne ustawienia w zależności od platformy
if sys.platform == "win32":
    PATH_SEPARATOR = "\\"
    CONFIG_DIR = os.path.join(os.getenv("APPDATA"), "LetMeTango")
    
elif sys.platform == "darwin":  # macOS
    PATH_SEPARATOR = "/"
    CONFIG_DIR = os.path.expanduser("~/Library/Application Support/LetMeTango")
    
else:  # Linux
    PATH_SEPARATOR = "/"
    CONFIG_DIR = os.path.expanduser("~/.config/letmetango")

# Stwórz katalog jeśli nie istnieje
os.makedirs(CONFIG_DIR, exist_ok=True)

__all__ = ['PATH_SEPARATOR', 'CONFIG_DIR']

# Użycie:
# from src.platform import CONFIG_DIR
# save_path = os.path.join(CONFIG_DIR, "savegame.dat")


# ============================================================
# PRZYKŁAD 8: Funkcje pomocnicze na poziomie paczki
# ============================================================
# src/utils/__init__.py (rozszerzenie obecnego)

from .colors import BasicColors, ThemeColors, UIColors

def hex_to_rgb(hex_color: str) -> tuple:
    """
    Konwertuje kolor hex na RGB.
    
    Args:
        hex_color: Kolor w formacie "#RRGGBB"
        
    Returns:
        tuple: (R, G, B)
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb: tuple) -> str:
    """Konwertuje RGB na hex."""
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

__all__ = [
    'BasicColors', 
    'ThemeColors', 
    'UIColors',
    'hex_to_rgb',
    'rgb_to_hex'
]

# Użycie:
# from src.utils import hex_to_rgb
# color = hex_to_rgb("#FF0000")  # (255, 0, 0)


# ============================================================
# PRZYKŁAD 9: Dekoratory dostępne na poziomie paczki
# ============================================================
# src/utils/__init__.py (dalsze rozszerzenie)

import functools
import time

def timer(func):
    """Dekorator mierzący czas wykonania funkcji."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"⏱️ {func.__name__} zajęło {end - start:.4f}s")
        return result
    return wrapper

def cache_result(func):
    """Prosty cache dla funkcji bez argumentów."""
    _cache = {}
    
    @functools.wraps(func)
    def wrapper(*args):
        key = args
        if key not in _cache:
            _cache[key] = func(*args)
        return _cache[key]
    return wrapper

__all__ = [
    'BasicColors', 'ThemeColors', 'UIColors',
    'timer', 'cache_result'
]

# Użycie:
# from src.utils import timer
# 
# @timer
# def generate_puzzle():
#     # ... długa operacja ...


# ============================================================
# PRZYKŁAD 10: Eksport podpaczek (hierarchia głębsza)
# ============================================================
# src/ui/__init__.py (propozycja)

"""
UI Package - wszystkie elementy interfejsu użytkownika.

Hierarchia:
- menu/ - system menu
- game/ - interfejs gry  
- dialogs/ - okna dialogowe
"""

from .menu import MainMenu
# from .game import GameUI  # Jeśli będziesz mieć
# from .dialogs import Dialog  # Jeśli będziesz mieć

__all__ = ['MainMenu']

# Użycie:
# from src.ui import MainMenu  # Zamiast: from src.ui.menu import MainMenu


# ============================================================
# PODSUMOWANIE - Twoje obecne __init__.py
# ============================================================

# ✅ src/utils/__init__.py - BARDZO DOBRE
"""
from .colors import BasicColors, ThemeColors, UIColors
__all__ = ['BasicColors', 'ThemeColors', 'UIColors']
"""

# ✅ src/ui/menu/__init__.py - DOBRE
"""
from .main_menu import MainMenu
__all__ = ['MainMenu']
"""

# ✅ src/ui/menu/components/__init__.py - DOSKONAŁE
"""
from .button import Button
from .selector import Selector
from .label import Label
from .info_box import InfoBox
__all__ = ['Button', 'Selector', 'Label', 'InfoBox']
"""

# ✅ src/board/__init__.py - DOBRE
"""
from .board import Board
__all__ = ['Board']
"""


# ============================================================
# ZALECENIA dla Twojego projektu
# ============================================================

"""
1. src/__init__.py - dodaj metadane:
   __version__ = "0.1.0"
   __author__ = "Your Name"

2. Wszystkie inne __init__.py są już dobrze zrobione!

3. W przyszłości możesz dodać:
   - Logger na poziomie paczek
   - Pomocnicze funkcje w src/utils/__init__.py
   - Lazy loading dla ciężkich zasobów (ikony, dźwięki)
"""
