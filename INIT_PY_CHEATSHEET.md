# `__init__.py` Cheat Sheet - Szybka ściągawka

## 🎯 Co to jest?
Plik `__init__.py` oznacza katalog jako paczkę Pythona i wykonuje kod przy pierwszym imporcie.

---

## 📋 Podstawowe wzorce

### 1. Pusty (minimum)
```python
# Katalog jest paczką, nic więcej
```

### 2. Re-export modułów
```python
from .module import Class1, function1
__all__ = ['Class1', 'function1']
```
**Efekt:** `from package import Class1` zamiast `from package.module import Class1`

### 3. Grupowanie wielu modułów
```python
from .module_a import ClassA
from .module_b import ClassB
from .module_c import ClassC

__all__ = ['ClassA', 'ClassB', 'ClassC']
```
**Efekt:** Wszystko z jednego miejsca!

### 4. Metadane
```python
"""Opis paczki."""
__version__ = "1.0.0"
__author__ = "Imię"

from .main import MainClass
__all__ = ['MainClass', '__version__']
```

### 5. Kod inicjalizacyjny
```python
import logging

# Wykona się przy pierwszym imporcie
logger = logging.getLogger(__name__)
print(f"✅ Pakiet {__name__} załadowany")

from .main import MainClass
```

---

## ⚡ Quick Reference

| Chcę... | Kod |
|---------|-----|
| Oznacz katalog jako paczkę | Pusty `__init__.py` |
| Łatwiejszy import | `from .module import Class` |
| Kontroluj `import *` | Zdefiniuj `__all__` |
| Stałe paczki | `CONSTANT = value` |
| Kod na starcie | Wpisz bezpośrednio w `__init__.py` |
| Dokumentacja | Docstring na początku |

---

## ✅ Best Practices

1. **Zawsze używaj `__all__`** - określa publiczne API
2. **Importy względne w `__init__.py`** - użyj `.module` nie `package.module`
3. **Krótkie i przejrzyste** - max 30 linii
4. **Unikaj ciężkich operacji** - lazy loading dla dużych zasobów
5. **Dokumentuj** - dodaj docstring

---

## ❌ Czego unikać

```python
# ❌ ZŁE - ciężka operacja przy imporcie
expensive_data = load_big_file()

# ✅ DOBRE - lazy loading
_data = None
def get_data():
    global _data
    if _data is None:
        _data = load_big_file()
    return _data
```

```python
# ❌ ZŁE - importy absolutne w __init__.py
from myproject.package.module import Class

# ✅ DOBRE - importy względne
from .module import Class
```

---

## 🔍 Twój projekt - obecny stan

### ✅ Dobre przykłady już masz:

**`src/utils/__init__.py`**
```python
from .colors import BasicColors, ThemeColors, UIColors
__all__ = ['BasicColors', 'ThemeColors', 'UIColors']
```
⭐ Ocena: **Doskonałe!**

**`src/ui/menu/components/__init__.py`**
```python
from .button import Button
from .selector import Selector
from .label import Label
from .info_box import InfoBox
__all__ = ['Button', 'Selector', 'Label', 'InfoBox']
```
⭐ Ocena: **Wzorcowe!**

---

## 🎓 Jak z tego korzystać?

### Przed (bez __init__.py):
```python
from src.utils.colors import BasicColors
from src.ui.menu.components.button import Button
from src.ui.menu.components.selector import Selector
```

### Po (z __init__.py):
```python
from src.utils import BasicColors
from src.ui.menu.components import Button, Selector
```

**Mniej kodu, większa czytelność!** 🎉

---

## 📚 Więcej informacji

- Szczegółowy przewodnik: `PYTHON_INIT_EXPLAINED.md`
- Przykłady kodu: `INIT_PY_EXAMPLES.py`
- Oficjalna dokumentacja: https://docs.python.org/3/tutorial/modules.html#packages
