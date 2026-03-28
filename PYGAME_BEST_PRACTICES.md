# Pygame Best Practices - Let Me Tango

## 🎮 Inicjalizacja Pygame

### ✅ DOBRE PRAKTYKI

#### 1. Wywołaj `pygame.init()` tylko RAZ
**Gdzie:** W głównym pliku aplikacji (`main.py`) przed utworzeniem jakichkolwiek obiektów pygame.

```python
# main.py
import pygame

def main():
    # Inicjalizacja pygame - TYLKO RAZ na początku aplikacji
    pygame.init()
    
    # Teraz możesz tworzyć okna, menu, gry itp.
    screen = pygame.display.set_mode((800, 600))
    game = Game(settings)
    game.run()

if __name__ == "__main__":
    main()
```

#### 2. NIE inicjalizuj pygame w klasach gier/komponentów
**Dlaczego:** Wielokrotne wywołanie `pygame.init()` może prowadzić do:
- Przecieków pamięci (memory leaks)
- Konfliktów w systemach audio/wideo
- Nieprzewidywalnego zachowania
- Problemów z wydajnością

```python
# ❌ ZŁE - NIE RÓB TEGO
class Game:
    def __init__(self, settings):
        pygame.init()  # ❌ To jest złe miejsce!
        self.screen = pygame.display.set_mode((800, 600))

# ✅ DOBRE - RÓB TO
class Game:
    def __init__(self, settings):
        # Zakładamy, że pygame.init() było już wywołane w main.py
        self.screen = pygame.display.set_mode((800, 600))
```

### 📝 Struktura projektu

```
main.py                  ← pygame.init() tutaj (raz!)
├── menu (MainMenu)      ← NIE inicjalizuj pygame
├── game (Game)          ← NIE inicjalizuj pygame
└── components           ← NIE inicjalizuj pygame
```

### 🔍 Weryfikacja

Sprawdź, czy `pygame.init()` jest wywołane tylko raz:
```powershell
# PowerShell
Select-String -Path "*.py" -Pattern "pygame.init\(\)" -Recurse
```

Powinno pokazać tylko jedno wystąpienie w `main.py`.

### 🎯 Dlaczego to ważne?

1. **Jednokrotna inicjalizacja** - pygame inicjalizuje wszystkie swoje podsystemy (audio, wideo, joystick, etc.)
2. **Kontrola zasobów** - wielokrotna inicjalizacja może nie zwolnić poprzednich zasobów
3. **Przewidywalność** - znasz dokładnie moment inicjalizacji systemu
4. **Łatwiejsze debugowanie** - wszystko zaczyna się w jednym miejscu

### 📚 Dodatkowe informacje

- Oficjalna dokumentacja: https://www.pygame.org/docs/ref/pygame.html#pygame.init
- `pygame.init()` zwraca krotkę (sukces, błędy) - możesz to sprawdzić w razie problemów:
  ```python
  success, failed = pygame.init()
  if failed > 0:
      print(f"⚠️ {failed} modułów pygame nie zainicjalizowało się poprawnie")
  ```

### 🔧 Specjalne przypadki

Jeśli chcesz zainicjalizować tylko konkretne moduły:
```python
# Inicjalizuj tylko konkretne moduły (rzadko potrzebne)
pygame.font.init()   # tylko czcionki
pygame.mixer.init()  # tylko audio
```

Ale w większości przypadków wystarczy `pygame.init()` - inicjalizuje wszystko!

---

**Obecny stan w projekcie:** ✅ 
- `pygame.init()` wywołane tylko w `main.py` (linia 19)
- Klasa `Game` w `game_manager.py` nie wywołuje `pygame.init()`
- Wszystkie komponenty UI nie wywołują `pygame.init()`
