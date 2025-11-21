# 📁 Nowa Struktura Menu - Single Responsibility Principle

## ✅ GOTOWE! Menu przeorganizowane zgodnie z SRP

### 🎯 Struktura katalogów

```
src/ui/menu/
├── __init__.py                      # Eksport MainMenu
├── main_menu.py                     # Orkiestrator menu (główna logika)
├── events.py                        # Obsługa zdarzeń
├── renderer.py                      # Renderowanie
└── components/                      # Komponenty UI
    ├── __init__.py                 # Eksport komponentów
    ├── button.py                   # Tylko Button
    ├── selector.py                 # Tylko Selector
    ├── label.py                    # Tylko Label
    └── info_box.py                 # Tylko InfoBox
```

---

## 📝 Single Responsibility Principle - Podział odpowiedzialności

### 1. **`components/button.py`** (90 linii)
**Odpowiedzialność**: Komponent przycisku
- Renderowanie przycisku
- Detekcja hover
- Wywołanie callback przy kliknięciu

**Zależności**: `pygame`, `colors`

---

### 2. **`components/selector.py`** (160 linii)
**Odpowiedzialność**: Komponent selektora opcji
- Renderowanie selektora z strzałkami
- Obsługa zmiany opcji (mysz + klawiatura)
- Wywoływanie callback przy zmianie

**Zależności**: `pygame`, `colors`

---

### 3. **`components/label.py`** (60 linii)
**Odpowiedzialność**: Komponent etykiety tekstowej
- Wyświetlanie tekstu
- Centrowanie opcjonalne

**Zależności**: `pygame`, `colors`

---

### 4. **`components/info_box.py`** (80 linii)
**Odpowiedzialność**: Komponent pola informacyjnego
- Wyświetlanie tytułu i tekstu
- Obsługa tekstu wieloliniowego

**Zależności**: `pygame`, `colors`

---

### 5. **`events.py`** (75 linii)
**Odpowiedzialność**: Obsługa zdarzeń menu
- Przetwarzanie zdarzeń pygame
- Delegowanie zdarzeń do komponentów
- Obsługa globalnych skrótów (ESC, Enter)

**Zależności**: `pygame`, `sys`

**Zwraca**: `dict` z flagami akcji `{'quit': bool, 'start_game': bool}`

---

### 6. **`renderer.py`** (50 linii)
**Odpowiedzialność**: Renderowanie menu
- Czyszczenie ekranu
- Rysowanie wszystkich komponentów
- Rysowanie instrukcji

**Zależności**: `pygame`, `colors`

---

### 7. **`main_menu.py`** (200 linii)
**Odpowiedzialność**: Orkiestrator menu (główna logika)
- Koordynacja komponentów UI
- Zarządzanie stanem wybranych opcji
- Generowanie `GameSettings` na podstawie wyborów
- Callbacks dla zmian opcji

**Zależności**: 
- `config` (GameConfig, GameSettings, Difficulty, BoardSize, Theme)
- `components` (Button, Selector, Label, InfoBox)
- `events` (MenuEventHandler)
- `renderer` (MenuRenderer)

**Metody**:
- `__init__()` - inicjalizacja menu
- `_create_ui_components()` - tworzy komponenty
- `_get_info_text()` - generuje tekst info
- `_on_difficulty_change()` - callback trudności
- `_on_size_change()` - callback rozmiaru
- `_on_theme_change()` - callback motywu
- `_start_game()` - callback START
- `run()` - główna pętla menu

---

## 🎭 Separacja odpowiedzialności (Before/After)

### ❌ PRZED (menu_components.py):
```
menu_components.py (280 linii)
├── Button
├── Selector
├── Label
└── InfoBox
```
**Problem**: Jeden plik odpowiada za 4 różne komponenty

---

### ✅ PO (components/):
```
components/
├── button.py      (90 linii)   - tylko Button
├── selector.py    (160 linii)  - tylko Selector  
├── label.py       (60 linii)   - tylko Label
└── info_box.py    (80 linii)   - tylko InfoBox
```
**Korzyść**: Każdy plik ma jedną odpowiedzialność

---

### ❌ PRZED (menu.py):
```
menu.py (220 linii)
├── Obsługa zdarzeń
├── Renderowanie
├── Zarządzanie stanem
└── Tworzenie komponentów
```
**Problem**: Jedna klasa robi wszystko

---

### ✅ PO:
```
events.py (75 linii)          - tylko zdarzenia
renderer.py (50 linii)        - tylko renderowanie
main_menu.py (200 linii)      - orkiestracja
```
**Korzyść**: Każdy moduł ma jasną odpowiedzialność

---

## 🔄 Przepływ danych

```
main.py
  ↓
MainMenu.run()
  ├─→ MenuEventHandler.handle_events(components)
  │     ├─ pygame.event.get()
  │     ├─ obsługa ESC/Enter
  │     └─ delegacja do komponentów
  │
  ├─→ Komponenty.handle_event()
  │     ├─ Button sprawdza kliknięcie
  │     ├─ Selector zmienia opcję
  │     └─ Callback (_on_*_change)
  │
  ├─→ MainMenu aktualizuje stan
  │     └─ info_box.set_content()
  │
  └─→ MenuRenderer.render(components)
        ├─ screen.fill()
        ├─ component.draw() dla każdego
        └─ pygame.display.flip()

Użytkownik kliknął START
  ↓
MainMenu._start_game()
  ↓
Tworzy GameSettings(difficulty, board_size, theme)
  ↓
Zwraca do main.py
  ↓
Game(settings).run()
```

---

## 🎯 Zalety nowej struktury

### 1. **Łatwość testowania**
Każdy komponent można testować osobno:
```python
# Test tylko przycisku
from src.ui.menu.components import Button
button = Button(...)
assert button.is_hovered == False
```

### 2. **Łatwość rozbudowy**
Dodanie nowego komponentu:
```python
# Wystarczy stworzyć nowy plik
components/slider.py
```

### 3. **Czytelność**
Każdy plik ma jasny cel:
- `button.py` - wiesz że tam jest Button i nic więcej
- `events.py` - wiesz że to obsługa zdarzeń

### 4. **Możliwość reużycia**
Komponenty można użyć w innych miejscach:
```python
# W innym menu, dialogu, toolbar
from src.ui.menu.components import Button, Label
```

### 5. **Łatwość utrzymania**
Bug w przycisku? Edytujesz tylko `button.py`

### 6. **Niezależność modułów**
Zmiana w `renderer.py` nie wpływa na `events.py`

---

## 📊 Porównanie

| Aspekt | Przed | Po |
|--------|-------|-----|
| **Plików w menu/** | 2 | 7 |
| **Linii w największym pliku** | 280 | 200 |
| **Odpowiedzialności na plik** | 3-4 | 1 |
| **Łatwość testowania** | Trudne | Łatwe |
| **Reużywalność** | Niska | Wysoka |
| **Zgodność z SRP** | ❌ | ✅ |

---

## 🚀 Jak używać?

### Import pozostał prosty:
```python
from src.ui.menu import MainMenu

menu = MainMenu(screen)
settings = menu.run()
```

### Wewnętrznie używa:
```python
# main_menu.py
from src.ui.menu.components import Button, Selector, Label, InfoBox
from src.ui.menu.events import MenuEventHandler
from src.ui.menu.renderer import MenuRenderer
```

---

## 📁 Stare pliki (do usunięcia)

Te pliki są już niepotrzebne:
- ❌ `src/ui/menu.py` (stary, 220 linii)
- ❌ `src/ui/menu_components.py` (stary, 280 linii)

**Nowa struktura** jest w `src/ui/menu/` (katalog).

---

## ✅ Checklist zgodności z SRP

- [x] **Każdy komponent w osobnym pliku**
- [x] **Każdy plik ma jedną odpowiedzialność**
- [x] **Obsługa zdarzeń oddzielona od renderowania**
- [x] **Orkiestrator oddzielony od komponentów**
- [x] **Komponenty nie znają się nawzajem**
- [x] **Łatwo dodać nowy komponent**
- [x] **Łatwo przetestować każdą część**

---

## 🎓 Zasada Single Responsibility

> "A class should have one, and only one, reason to change."
> — Robert C. Martin

### Przykłady w naszym kodzie:

**Button ma jeden powód do zmiany**: zmiana wyglądu/zachowania przycisku  
**Events ma jeden powód do zmiany**: zmiana obsługi zdarzeń  
**Renderer ma jeden powód do zmiany**: zmiana sposobu renderowania  

**Gdyby były razem**: zmiana renderowania wymagałaby edycji tego samego pliku co zmiana obsługi zdarzeń → naruszenie SRP.

---

## 🔮 Przyszła rozbudowa

Dzięki strukturze łatwo dodać:

### Nowe komponenty:
```
components/
├── slider.py         # Suwak
├── checkbox.py       # Checkbox
├── dropdown.py       # Lista rozwijana
├── textbox.py        # Pole tekstowe
```

### Nowe menu:
```
src/ui/
├── menu/            # Menu główne
├── settings_menu/   # Menu ustawień
├── pause_menu/      # Menu pauzy
└── game_over/       # Ekran Game Over
```

Każde może reużywać komponenty z `menu/components/`!

---

## 📝 Podsumowanie

✅ **Menu przeorganizowane zgodnie z Single Responsibility Principle**  
✅ **7 osobnych plików zamiast 2 dużych**  
✅ **Każdy plik ma jedną jasną odpowiedzialność**  
✅ **Łatwe testowanie, rozbudowa, utrzymanie**  
✅ **Komponenty reużywalne**  
✅ **Kod czytelny i profesjonalny**  

**Struktura gotowa do produkcji!** 🎉

---

**Utworzono**: 2025-11-09  
**Zasada**: Single Responsibility Principle (SOLID)  
**Plików**: 7 nowych, 2 stare do usunięcia  
**Linii kodu**: ~750 (podzielone na moduły)

