# Python `__init__.py` - Kompletny przewodnik

## 🎯 Co to jest `__init__.py`?

Plik `__init__.py` pełni **dwie główne role**:

1. **Oznacza katalog jako paczkę Pythona** (package marker)
2. **Kod inicjalizacyjny paczki** - wszystko co wpiszesz w `__init__.py` wykonuje się gdy importujesz paczkę

## 📦 Podstawy

### Pusty `__init__.py`
```python
# src/core/__init__.py
# (pusty plik)
```
**Efekt:** Katalog `core/` jest traktowany jako paczka, można robić:
```python
from src.core import something
```

### Niepusty `__init__.py` - tu zaczyna się magia! ✨

---

## 🔥 Co można zawrzeć w `__init__.py`?

### 1️⃣ **Re-export symboli** (Twój obecny przypadek)

**Plik:** `src/utils/__init__.py`
```python
from .colors import BasicColors, ThemeColors, UIColors

__all__ = [
    'BasicColors',
    'ThemeColors', 
    'UIColors'
]
```

**Co to robi:**
- Importuje klasy z modułu `colors.py`
- Udostępnia je na poziomie paczki `utils`

**Korzyści:**
```python
# ❌ BEZ __init__.py - długi import
from src.utils.colors import BasicColors, ThemeColors

# ✅ Z __init__.py - krótszy, czytelniejszy import
from src.utils import BasicColors, ThemeColors
```

**`__all__`** kontroluje co jest eksportowane przy `from utils import *`:
```python
from src.utils import *  # Importuje TYLKO: BasicColors, ThemeColors, UIColors
```

---

### 2️⃣ **Grupowanie importów z wielu modułów**

**Przykład dla Twojego projektu:**

```python
# src/ui/menu/__init__.py
from .main_menu import MainMenu
from .renderer import MenuRenderer
from .events import MenuEventHandler
from .components import Button, Selector, Label, InfoBox

__all__ = [
    'MainMenu',
    'MenuRenderer', 
    'MenuEventHandler',
    'Button',
    'Selector',
    'Label',
    'InfoBox'
]
```

**Efekt:**
```python
# Zamiast:
from src.ui.menu.main_menu import MainMenu
from src.ui.menu.components.button import Button
from src.ui.menu.components.selector import Selector

# Możesz napisać:
from src.ui.menu import MainMenu, Button, Selector
```

---

### 3️⃣ **Kod inicjalizacyjny paczki**

```python
# src/game/__init__.py
import logging

# Konfiguracja loggera dla całej paczki
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

print("🎮 Pakiet 'game' załadowany!")

# Teraz każdy moduł w game/ może użyć tego loggera
```

**Kiedy się wykonuje:** Przy pierwszym imporcie czegokolwiek z paczki `game/`.

---

### 4️⃣ **Zmienne na poziomie paczki**

```python
# src/config/__init__.py
from .settings import GameSettings, GameConfig
from .constants import DEFAULT_FPS, MAX_BOARD_SIZE

__version__ = "1.0.0"
__author__ = "Twoje Imię"

# Singleton/stałe dostępne w całej paczce
DEFAULT_SETTINGS = GameSettings(
    difficulty=Difficulty.MEDIUM,
    board_size=BoardSize.MEDIUM,
    theme=Theme.CLASSIC
)

__all__ = ['GameSettings', 'GameConfig', 'DEFAULT_SETTINGS', '__version__']
```

**Użycie:**
```python
from src.config import __version__, DEFAULT_SETTINGS
print(f"Wersja gry: {__version__}")
```

---

### 5️⃣ **Warunkowe importy / lazy loading**

```python
# src/assets/__init__.py
import sys

# Importuj różne rzeczy w zależności od platformy
if sys.platform == "win32":
    from .windows_assets import load_icons
elif sys.platform == "darwin":
    from .mac_assets import load_icons
else:
    from .linux_assets import load_icons

__all__ = ['load_icons']
```

---

### 6️⃣ **Inicjalizacja zasobów**

```python
# src/audio/__init__.py
import pygame.mixer
import os

# Inicjalizacja audio przy pierwszym imporcie
_audio_initialized = False

def init_audio():
    global _audio_initialized
    if not _audio_initialized:
        pygame.mixer.init()
        _audio_initialized = True
        print("🔊 System audio zainicjalizowany")

# Wczytaj domyślne dźwięki
SOUND_CLICK = os.path.join("assets", "sounds", "click.wav")
SOUND_SUCCESS = os.path.join("assets", "sounds", "success.wav")

__all__ = ['init_audio', 'SOUND_CLICK', 'SOUND_SUCCESS']
```

---

### 7️⃣ **Dekoratory i fabryki**

```python
# src/utils/__init__.py
from .colors import BasicColors, ThemeColors, UIColors
from .decorators import cache_result, log_calls
from .validators import validate_positive

__all__ = [
    'BasicColors', 'ThemeColors', 'UIColors',
    'cache_result', 'log_calls', 'validate_positive'
]
```

Teraz możesz:
```python
from src.utils import cache_result, BasicColors

@cache_result
def expensive_calculation():
    # ...
```

---

## 🎨 Przykład: Struktura UI w Twoim projekcie

### Obecna struktura:
```
src/ui/menu/
├── __init__.py          ← Tutaj możesz zgrupować importy
├── main_menu.py
├── renderer.py
├── events.py
└── components/
    ├── __init__.py      ← I tutaj też!
    ├── button.py
    ├── selector.py
    ├── label.py
    └── info_box.py
```

### Propozycja `src/ui/menu/__init__.py`:

```python
"""
Menu module - główne menu gry z komponentami UI.

Eksportuje wszystkie kluczowe klasy dla łatwiejszego importu.
"""
from .main_menu import MainMenu
from .renderer import MenuRenderer
from .events import MenuEventHandler

__all__ = ['MainMenu', 'MenuRenderer', 'MenuEventHandler']
```

### Propozycja `src/ui/menu/components/__init__.py`:

```python
"""
UI Components - komponenty interfejsu użytkownika.

Wszystkie komponenty dostępne z jednego importu.
"""
from .button import Button
from .selector import Selector
from .label import Label
from .info_box import InfoBox

__all__ = ['Button', 'Selector', 'Label', 'InfoBox']
```

### Użycie:
```python
# Zamiast:
from src.ui.menu.main_menu import MainMenu
from src.ui.menu.components.button import Button
from src.ui.menu.components.selector import Selector

# Wystarczy:
from src.ui.menu import MainMenu
from src.ui.menu.components import Button, Selector
```

---

## ⚠️ Pułapki i uwagi

### 1. **Unikaj cyklicznych importów**
```python
# ❌ ZŁE - może prowadzić do cyklicznych importów
# src/module_a/__init__.py
from src.module_b import something  # module_b importuje module_a -> błąd!
```

**Rozwiązanie:** Importuj tylko w funkcjach lub używaj `import` zamiast `from ... import`

### 2. **Importy względne (relative imports)**
```python
# W __init__.py używaj importów względnych
from .colors import BasicColors      # ✅ Dobre - relative
from src.utils.colors import ...     # ❌ Unikaj - absolute w __init__.py
```

### 3. **`__all__` jest opcjonalne**
- Bez `__all__`: `from package import *` importuje WSZYSTKO co nie zaczyna się od `_`
- Z `__all__`: `from package import *` importuje TYLKO elementy z listy
- Lepiej **zawsze definiować `__all__`** dla przejrzystości!

### 4. **Wydajność**
Kod w `__init__.py` wykonuje się **przy pierwszym imporcie**:
```python
# ❌ Unikaj ciężkich operacji w __init__.py
import heavy_library
result = expensive_computation()  # To się wykona przy imporcie!

# ✅ Lepiej - lazy loading
def get_result():
    return expensive_computation()
```

---

## 🏆 Best Practices dla Twojego projektu

### ✅ Dobra struktura `__init__.py`:

1. **Krótki i przejrzysty** - nie więcej niż 20-30 linii
2. **Dokumentacja** - docstring na początku
3. **Jasne `__all__`** - wyraźnie określ co jest publiczne API
4. **Grupuj logicznie** - wszystkie komponenty UI razem, kolory razem, etc.
5. **Unikaj logiki biznesowej** - to tylko "routing" importów

### Przykład wzorcowy:

```python
"""
Nazwa paczki - krótki opis.

Dłuższy opis funkcjonalności paczki.
"""
from .module_a import ClassA, function_a
from .module_b import ClassB
from .subpackage import SubClass

# Stałe paczki (opcjonalnie)
__version__ = "1.0.0"
__author__ = "Your Name"

# Definicja publicznego API
__all__ = [
    'ClassA',
    'ClassB', 
    'SubClass',
    'function_a',
]
```

---

## 📊 Twój obecny `src/utils/__init__.py` - analiza

```python
from .colors import BasicColors, ThemeColors, UIColors

__all__ = [
    'BasicColors',
    'ThemeColors', 
    'UIColors'
]
```

**Ocena:** ✅ **Bardzo dobre!**

✅ Używa importów względnych (`.colors`)  
✅ Definiuje jasne `__all__`  
✅ Krótkie i czytelne  
✅ Grupuje kolory w jednym miejscu  

**Możliwe rozszerzenia:**
```python
"""
Utils - narzędzia pomocnicze dla projektu Let Me Tango.

Zawiera:
- Definicje kolorów (BasicColors, ThemeColors, UIColors)
- (w przyszłości: dekoratory, validatory, helpery)
"""
from .colors import BasicColors, ThemeColors, UIColors

__version__ = "1.0.0"

__all__ = [
    'BasicColors',
    'ThemeColors', 
    'UIColors'
]
```

---

## 🎓 Podsumowanie

| Co można zawrzeć | Przykład | Kiedy używać |
|-----------------|----------|--------------|
| Re-eksport modułów | `from .colors import Colors` | Zawsze - dla wygody importów |
| `__all__` | `__all__ = ['Class1', 'func1']` | Zalecane - definiuje API |
| Stałe paczki | `__version__ = "1.0.0"` | Opcjonalnie - metadane |
| Kod init | `logging.basicConfig(...)` | Ostrożnie - tylko lekkie operacje |
| Grupowanie | Import z wielu modułów | Dla czytelności API |
| Docstring | `"""Opis paczki"""` | Zawsze - dokumentuj! |

**Złota zasada:** `__init__.py` to **"wizytówka"** Twojej paczki - powinien być prosty, przejrzysty i definiować co jest publicznym API! 🎯
