# 🗺️ Let Me Tango - Roadmap Implementacji

Ten dokument zawiera szczegółowy plan rozwoju projektu w formie issues gotowych do implementacji.

---

## 🎯 FAZA 1: Core Gameplay (Podstawowa Mechanika Gry)

### Issue #1: Refaktoryzacja struktury głównego kodu
**Priorytet**: 🔴 KRYTYCZNY  
**Etykiety**: `refactoring`, `architecture`, `phase-1`

**Opis:**
Przenieść kod z `main.py` do odpowiednich modułów w strukturze `src/`, aby zachować czystą architekturę projektu.

**Zadania:**
- [ ] Przenieść klasę `Cell` do `src/cell/cell_setup.py` (rozszerzyć istniejącą)
- [ ] Przenieść klasę `Board` do `src/board/board.py` (nowy plik)
- [ ] Przenieść klasę `Game` do `src/game_manager.py` (nowy plik)
- [ ] Przenieść stałe kolorów do `src/utils/colors.py`
- [ ] Zaktualizować importy w `main.py`
- [ ] `main.py` powinien mieć max 10-15 linii (import + uruchomienie gry)

**Kryteria akceptacji:**
- Gra działa identycznie jak przed refaktoryzacją
- Kod jest podzielony logicznie na moduły
- Wszystkie importy działają poprawnie

**Oszacowany czas**: 2-3h

---

### Issue #2: Implementacja pełnego Validatora
**Priorytet**: 🔴 KRYTYCZNY  
**Etykiety**: `core-logic`, `validation`, `phase-1`

**Opis:**
Zaimplementować kompletny system walidacji wszystkich zasad gry w `src/core/validator.py`.

**Zadania:**
- [ ] `validate_three_consecutive()` - sprawdza 3 z rzędu (poziomo i pionowo)
- [ ] `validate_count_balance()` - sprawdza równą liczbę symboli w wierszu/kolumnie
- [ ] `validate_unique_rows()` - sprawdza czy wiersze są unikalne
- [ ] `validate_unique_cols()` - sprawdza czy kolumny są unikalne
- [ ] `validate_constraints()` - sprawdza ograniczenia = i × (placeholder na później)
- [ ] `is_board_complete()` - sprawdza czy plansza jest w pełni wypełniona
- [ ] `is_board_valid()` - sprawdza wszystkie warunki jednocześnie
- [ ] `get_errors()` - zwraca listę błędów z pozycjami komórek
- [ ] Dodać testy jednostkowe dla każdej funkcji

**Kryteria akceptacji:**
- Validator poprawnie wykrywa wszystkie naruszenia zasad
- Funkcje zwracają jasne informacje o błędach
- Napisane testy pokrywają wszystkie przypadki brzegowe

**Oszacowany czas**: 4-5h

---

### Issue #3: Generator Planszy - Algorytm Backtracking
**Priorytet**: 🔴 KRYTYCZNY  
**Etykiety**: `algorithm`, `board-generation`, `phase-1`

**Opis:**
Zaimplementować algorytm generowania poprawnie wypełnionej planszy używając backtrackingu.

**Zadania:**
- [ ] Napisać `generate_full_solution()` - generuje kompletne, poprawne rozwiązanie
- [ ] Algorytm backtrackingu z walidacją na każdym kroku
- [ ] Randomizacja kolejności wyboru symboli dla różnorodności
- [ ] Optymalizacja wydajności (limit rekurencji, early exit)
- [ ] Dodać opcjonalny `seed` dla reprodukowalności planszy
- [ ] Testy dla różnych rozmiarów planszy (4×4, 6×6, 8×8, 10×10)

**Kryteria akceptacji:**
- Generator tworzy poprawne rozwiązania dla wszystkich rozmiarów
- Generowanie planszy 6×6 trwa < 1 sekundy
- Możliwość utworzenia planszy z danym seedem

**Oszacowany czas**: 6-8h

---

### Issue #4: Generator Puzzli - Usuwanie Komórek
**Priorytet**: 🟠 WYSOKI  
**Etykiety**: `algorithm`, `board-generation`, `phase-1`

**Opis:**
Implementacja systemu usuwania komórek z pełnej planszy, aby utworzyć puzzle z odpowiednim poziomem trudności.

**Zadania:**
- [ ] `remove_cells()` - usuwa komórki z pełnej planszy
- [ ] Algorytm sprawdzający unikalność rozwiązania
- [ ] Różne poziomy trudności:
  - Easy: usuń 40% komórek
  - Medium: usuń 55% komórek  
  - Hard: usuń 70% komórek
  - Expert: usuń 75%+ komórek
- [ ] Sprawdzanie czy puzzle ma dokładnie jedno rozwiązanie
- [ ] Optymalizacja - preferować usuwanie symetryczne

**Kryteria akceptacji:**
- Wygenerowane puzzle mają dokładnie jedno rozwiązanie
- Różne poziomy trudności dają zauważalną różnicę
- Generowanie puzzla trwa < 2 sekundy

**Oszacowany czas**: 8-10h

---

### Issue #5: System Ograniczeń (Constraints)
**Priorytet**: 🟡 ŚREDNI  
**Etykiety**: `feature`, `constraints`, `phase-1`

**Opis:**
Dodać system ograniczeń między komórkami: równość (=) i nierówność (×).

**Zadania:**
- [ ] Stworzyć klasę `Constraint` w `src/core/constraints.py`
- [ ] Typy: `EQUAL` (=) i `NOT_EQUAL` (×)
- [ ] Dodać listę constraints do klasy Board
- [ ] Wizualizacja constraints na planszy (linie między komórkami)
- [ ] Walidacja constraints w Validatorze
- [ ] Generator automatycznie dodaje sensowne constraints
- [ ] Opcja włączenia/wyłączenia constraints w ustawieniach

**Kryteria akceptacji:**
- Constraints są poprawnie renderowane
- Validator sprawdza naruszenia constraints
- Generator dodaje constraints zwiększające trudność

**Oszacowany czas**: 5-6h

---

### Issue #6: Historia Ruchów (Undo/Redo)
**Priorytet**: 🟡 ŚREDNI  
**Etykiety**: `feature`, `game-logic`, `phase-1`

**Opis:**
Implementacja systemu cofania i ponawiania ruchów gracza.

**Zadania:**
- [ ] Stworzyć klasę `Move` przechowującą stan ruchu
- [ ] Stack dla undo (poprzednie ruchy)
- [ ] Stack dla redo (cofnięte ruchy)
- [ ] Implementacja `undo()` - cofnij ostatni ruch
- [ ] Implementacja `redo()` - ponów cofnięty ruch
- [ ] Limit historii (np. 50 ruchów)
- [ ] Dodać przyciski do UI (placeholder - będzie w Phase 2)
- [ ] Skróty klawiszowe: Ctrl+Z (undo), Ctrl+Y (redo)

**Kryteria akceptacji:**
- Gracze mogą cofać ruchy bez limitu (do początku gry)
- Redo działa po cofnięciu
- System nie powoduje błędów przy pustej historii

**Oszacowany czas**: 3-4h

---

## 🎨 FAZA 2: UI/UX (Interfejs Użytkownika)

### Issue #7: System Menu Głównego
**Priorytet**: 🟠 WYSOKI  
**Etykiety**: `ui`, `menu`, `phase-2`

**Opis:**
Stworzyć profesjonalne menu główne z opcjami gry.

**Zadania:**
- [ ] Rozbudować `src/ui/menu.py`
- [ ] Ekran tytułowy z logo
- [ ] Przyciski:
  - "Nowa Gra"
  - "Kontynuuj" (jeśli jest zapisana gra)
  - "Wybór Poziomu"
  - "Ustawienia"
  - "Instrukcja"
  - "Wyjście"
- [ ] Animacje przejść między ekranami
- [ ] Obsługa myszy i klawiatury
- [ ] Responsywny design

**Kryteria akceptacji:**
- Menu jest czytelne i intuicyjne
- Wszystkie przyciski działają
- Płynne przejścia między ekranami

**Oszacowany czas**: 4-5h

---

### Issue #8: Ekran Wyboru Poziomu
**Priorytet**: 🟠 WYSOKI  
**Etykiety**: `ui`, `level-select`, `phase-2`

**Opis:**
Ekran pozwalający wybrać rozmiar planszy, trudność i daily challenge.

**Zadania:**
- [ ] Interfejs wyboru rozmiaru: 4×4, 6×6, 8×8, 10×10
- [ ] Wybór trudności: Easy, Medium, Hard, Expert
- [ ] Sekcja "Daily Challenge"
- [ ] Podgląd przykładowej planszy
- [ ] Statystyki (ile ukończono na każdym poziomie)
- [ ] Przycisk "Start Game"

**Kryteria akceptacji:**
- Intuicyjny wybór parametrów gry
- Wyświetlanie statystyk działa
- Generowana plansza odpowiada wyborom

**Oszacowany czas**: 3-4h

---

### Issue #9: Toolbar z Akcjami
**Priorytet**: 🟠 WYSOKI  
**Etykiety**: `ui`, `toolbar`, `phase-2`

**Opis:**
Implementacja paska narzędzi z przyciskami akcji podczas gry.

**Zadania:**
- [ ] Rozbudować `src/ui/toolbar.py`
- [ ] Przyciski:
  - 🔙 Cofnij (Undo)
  - 🔄 Ponów (Redo)
  - 💡 Podpowiedź (Hint)
  - ✓ Sprawdź Rozwiązanie
  - 🔄 Reset Planszy
  - ⏸️ Pauza
  - ⚙️ Ustawienia
  - 🏠 Menu Główne
- [ ] Tooltips przy najechaniu myszką
- [ ] Wyłączanie przycisków gdy niedostępne
- [ ] Liczniki (np. pozostałe hinty)

**Kryteria akceptacji:**
- Wszystkie przyciski są funkcjonalne
- UI jest responsywne
- Tooltips działają poprawnie

**Oszacowany czas**: 4-5h

---

### Issue #10: Ulepszenia Wizualne Planszy
**Priorytet**: 🟡 ŚREDNI  
**Etykiety**: `ui`, `visual`, `phase-2`

**Opis:**
Poprawić wygląd planszy i komórek, dodać animacje i efekty.

**Zadania:**
- [ ] Lepsze renderowanie siatki (grubsze linie co 2 komórki)
- [ ] Hover effect przy najechaniu na komórkę
- [ ] Animacja umieszczania symbolu
- [ ] Pulsowanie komórek z błędami
- [ ] Podświetlanie całego wiersza/kolumny przy kliknięciu
- [ ] Liczniki symboli na bokach (ile ☀️ i 🌙 w wierszu/kolumnie)
- [ ] Gradientowe tło
- [ ] Cienie dla głębi

**Kryteria akceptacji:**
- Plansza wygląda profesjonalnie
- Animacje są płynne (60 FPS)
- UI jest czytelne

**Oszacowany czas**: 5-6h

---

### Issue #11: Ekran Wygranej
**Priorytet**: 🟡 ŚREDNI  
**Etykiety**: `ui`, `win-screen`, `phase-2`

**Opis:**
Rozbudować `src/ui/win_popup.py` - ekran po ukończeniu puzzle.

**Zadania:**
- [ ] Animacja wygranej (confetti, fajerwerki)
- [ ] Wyświetlanie statystyk:
  - Czas rozwiązania
  - Liczba ruchów
  - Użyte podpowiedzi
  - Perfekcyjne rozwiązanie? (bez błędów)
- [ ] Przyciski:
  - Następny Poziom
  - Graj Ponownie
  - Menu Główne
- [ ] Zapisanie wyniku do statystyk
- [ ] Efekty dźwiękowe (placeholder)

**Kryteria akceptacji:**
- Ekran wygranej jest satysfakcjonujący wizualnie
- Wszystkie statystyki są poprawne
- Przyciski działają

**Oszacowany czas**: 3-4h

---

## ⚡ FAZA 3: Features (Dodatkowe Funkcje)

### Issue #12: System Timerów
**Priorytet**: 🟡 ŚREDNI  
**Etykiety**: `feature`, `timer`, `phase-3`

**Opis:**
Dodać timer mierzący czas rozwiązywania puzzle.

**Zadania:**
- [ ] Klasa `Timer` w `src/utils/timer.py`
- [ ] Start timera przy rozpoczęciu gry
- [ ] Pauza timera
- [ ] Wyświetlanie czasu w formacie MM:SS
- [ ] Zapisywanie najlepszych czasów
- [ ] Opcja trybu "na czas" (time challenge)

**Kryteria akceptacji:**
- Timer działa dokładnie
- Pauza nie wpływa na czas
- Najlepsze czasy są zapisywane

**Oszacowany czas**: 2-3h

---

### Issue #13: System Podpowiedzi (Hints)
**Priorytet**: 🟡 ŚREDNI  
**Etykiety**: `feature`, `hints`, `phase-3`

**Opis:**
Implementacja inteligentnego systemu podpowiedzi.

**Zadania:**
- [ ] Algorytm znajdujący najbezpieczniejszy ruch
- [ ] Typy podpowiedzi:
  - Podświetl komórkę do wypełnienia
  - Pokaż błąd na planszy
  - Usuń jeden błędny symbol
- [ ] Limit podpowiedzi (3-5 na grę zależnie od trudności)
- [ ] Animacja podświetlenia podpowiedzi
- [ ] Kara punktowa za użycie podpowiedzi

**Kryteria akceptacji:**
- Podpowiedzi są pomocne ale nie rozwiązują gry
- Limit działa poprawnie
- Animacje są czytelne

**Oszacowany czas**: 5-6h

---

### Issue #14: System Sprawdzania Rozwiązania
**Priorytet**: 🟡 ŚREDNI  
**Etykiety**: `feature`, `validation`, `phase-3`

**Opis:**
Funkcja "Check Solution" sprawdzająca postęp gracza.

**Zadania:**
- [ ] Przycisk "Sprawdź"
- [ ] Podświetlenie wszystkich błędów na czerwono
- [ ] Podświetlenie poprawnych komórek na zielono
- [ ] Komunikat z procentem poprawności
- [ ] Opcja automatycznego sprawdzania (podczas gry)
- [ ] Licznik błędów

**Kryteria akceptacji:**
- Sprawdzanie jest dokładne
- Wizualizacja błędów jest czytelna
- Nie spowalnia gry

**Oszacowany czas**: 3-4h

---

### Issue #15: System Zapisywania Gry
**Priorytet**: 🟡 ŚREDNI  
**Etykiety**: `feature`, `save-system`, `phase-3`

**Opis:**
Możliwość zapisywania i wczytywania stanu gry.

**Zadania:**
- [ ] Serializacja stanu planszy do JSON
- [ ] Zapisywanie do pliku `saves/savegame.json`
- [ ] Wczytywanie przy starcie (przycisk "Kontynuuj")
- [ ] Autosave co 5 ruchów
- [ ] Zapisywanie historii ruchów
- [ ] Obsługa wielu slotów zapisu (opcjonalne)

**Kryteria akceptacji:**
- Zapis zachowuje pełny stan gry
- Wczytywanie przywraca stan identycznie
- Autosave nie przeszkadza w grze

**Oszacowany czas**: 4-5h

---

### Issue #16: Statystyki Gracza
**Priorytet**: 🟢 NISKI  
**Etykiety**: `feature`, `statistics`, `phase-3`

**Opis:**
System śledzenia i wyświetlania statystyk gracza.

**Zadania:**
- [ ] Baza danych SQLite lub JSON dla statystyk
- [ ] Śledzone metryki:
  - Liczba ukończonych gier (per poziom trudności i rozmiar)
  - Średni czas rozwiązania
  - Najlepszy czas
  - Liczba użytych podpowiedzi
  - Seria wygranych (streak)
  - Perfekcyjne rozwiązania (bez błędów)
- [ ] Ekran statystyk w menu
- [ ] Wykresy i wizualizacje
- [ ] Reset statystyk

**Kryteria akceptacji:**
- Wszystkie statystyki są dokładnie śledzone
- Ekran statystyk jest czytelny
- Dane przetrwają restart aplikacji

**Oszacowany czas**: 5-6h

---

## 🎮 FAZA 4: Content (Zawartość)

### Issue #17: Daily Challenge
**Priorytet**: 🟡 ŚREDNI  
**Etykiety**: `feature`, `daily-challenge`, `phase-4`

**Opis:**
System dziennego wyzwania - ta sama plansza dla wszystkich użytkowników.

**Zadania:**
- [ ] Generator seedu bazującego na dacie (YYYY-MM-DD)
- [ ] Specjalny ekran Daily Challenge
- [ ] Zapisywanie czy dzisiejsze wyzwanie zostało ukończone
- [ ] Tablica wyników (opcjonalnie - wymaga backendu)
- [ ] Nagrody za ukończenie (punkty, odznaki)
- [ ] Historia daily challenges (kalendarz)

**Kryteria akceptacji:**
- Seed dla danej daty jest zawsze taki sam
- Można grać tylko raz dziennie
- Status jest zapisywany

**Oszacowany czas**: 4-5h

---

### Issue #18: System Motywów (Themes)
**Priorytet**: 🟢 NISKI  
**Etykiety**: `feature`, `themes`, `phase-4`

**Opis:**
Różne motywy wizualne do wyboru.

**Zadania:**
- [ ] System ładowania motywów z plików JSON
- [ ] Motywy:
  - Classic (obecny)
  - Dark Mode
  - Forest (zielone odcienie)
  - Ocean (niebieskie)
  - Sunset (ciepłe kolory)
  - High Contrast (dla accessibility)
- [ ] Możliwość zmiany ikon (nie tylko ☀️🌙)
- [ ] Zapisywanie preferencji
- [ ] Podgląd w ustawieniach

**Kryteria akceptacji:**
- Minimum 4 motywy działają poprawnie
- Zmiana motywu nie resetuje gry
- Motywy są estetyczne

**Oszacowany czas**: 6-8h

---

### Issue #19: Alternatywne Ikony (Zwierzątka)
**Priorytet**: 🟢 NISKI  
**Etykiety**: `assets`, `icons`, `phase-4`

**Opis:**
Dodać alternatywne zestawy ikon zamiast słońca/księżyca.

**Zadania:**
- [ ] Zestawy ikon:
  - Zwierzęta: 🐱🐶 (kot/pies)
  - Owoce: 🍎🍊 (jabłko/pomarańcza)
  - Kształty: ⚪⚫ (koło/kwadrat)
  - Emotikony: 😊😢 (uśmiech/smutek)
- [ ] Wybór zestawu w ustawieniach
- [ ] Skalowanie i optymalizacja ikon
- [ ] Wsparcie dla custom ikon (użytkownik może dodać swoje)

**Kryteria akceptacji:**
- Minimum 3 zestawy działają
- Ikony są czytelne na wszystkich rozmiarach
- Zmiana zestawu jest instant

**Oszacowany czas**: 4-5h

---

### Issue #20: Tutorial Interaktywny
**Priorytet**: 🟡 ŚREDNI  
**Etykiety**: `feature`, `tutorial`, `phase-4`

**Opis:**
Interaktywny samouczek dla nowych graczy.

**Zadania:**
- [ ] Seria prostych puzzli jako tutorial
- [ ] Podświetlenia i wskazówki krok po kroku
- [ ] Wyjaśnienie każdej zasady z przykładem
- [ ] Niemożliwość popełnienia błędu (blokada złych ruchów)
- [ ] Nagroda za ukończenie tutorialu
- [ ] Opcja pominięcia dla doświadczonych

**Kryteria akceptacji:**
- Tutorial jest jasny i pomocny
- Każda zasada jest wyjaśniona
- Nowi gracze rozumieją grę po tutorialu

**Oszacowany czas**: 5-6h

---

## ✨ FAZA 5: Polish (Dopracowanie)

### Issue #21: System Dźwięków
**Priorytet**: 🟢 NISKI  
**Etykiety**: `audio`, `polish`, `phase-5`

**Opis:**
Dodać efekty dźwiękowe i muzykę tła.

**Zadania:**
- [ ] Efekty dźwiękowe:
  - Kliknięcie komórki
  - Błąd (próba złego ruchu)
  - Ukończenie wiersza/kolumny
  - Wygrana
  - Przycisk UI
- [ ] Muzyka tła (opcjonalna, możliwość wyłączenia)
- [ ] Slider głośności w ustawieniach
- [ ] Osobne kontrolki dla SFX i muzyki
- [ ] Znajdź/stwórz darmowe dźwięki (freesound.org, OpenGameArt)

**Kryteria akceptacji:**
- Dźwięki są przyjemne i nie irytujące
- Można je wyłączyć
- Nie ma opóźnień w odtwarzaniu

**Oszacowany czas**: 3-4h

---

### Issue #22: Animacje i Efekty Cząsteczkowe
**Priorytet**: 🟢 NISKI  
**Etykiety**: `visual`, `animations`, `phase-5`

**Opis:**
Dodać płynne animacje i efekty wizualne.

**Zadania:**
- [ ] Animacje:
  - Fade in/out symboli
  - Shake przy błędzie
  - Bounce przy kliknięciu
  - Slide in menu
  - Confetti przy wygranej
- [ ] Efekty cząsteczkowe:
  - Iskierki przy perfekcyjnym ruchu
  - Fale przy ukończeniu wiersza
- [ ] Smooth transitions między ekranami
- [ ] Opcja wyłączenia animacji (accessibility)

**Kryteria akceptacji:**
- Animacje są płynne (60 FPS)
- Nie spowalniają gry
- Można je wyłączyć

**Oszacowany czas**: 6-8h

---

### Issue #23: Accessibility Features
**Priorytet**: 🟡 ŚREDNI  
**Etykiety**: `accessibility`, `polish`, `phase-5`

**Opis:**
Funkcje ułatwiające dostęp dla osób z niepełnosprawnościami.

**Zadania:**
- [ ] Tryb dla daltonistów (różne kolory/kształty)
- [ ] Duże ikony / zwiększona czcionka
- [ ] Obsługa klawiatury (nawigacja bez myszy)
- [ ] Screen reader support (etykiety tekstowe)
- [ ] Wysokontraścyjny motyw
- [ ] Możliwość wyłączenia animacji
- [ ] Dostosowywalna prędkość gry

**Kryteria akceptacji:**
- Gra jest dostępna dla osób z wadami wzroku
- Pełna obsługa klawiatury działa
- Wysokontraścyjny tryb jest czytelny

**Oszacowany czas**: 5-6h

---

### Issue #24: Optymalizacja Wydajności
**Priorytet**: 🟡 ŚREDNI  
**Etykiety**: `performance`, `optimization`, `phase-5`

**Opis:**
Optymalizacja kodu dla lepszej wydajności.

**Zadania:**
- [ ] Profilowanie kodu (cProfile)
- [ ] Optymalizacja generatora planszy
- [ ] Caching renderowania
- [ ] Lazy loading assetów
- [ ] Redukcja alokacji pamięci
- [ ] Optymalizacja pętli głównej
- [ ] Target: 60 FPS na starszych komputerach

**Kryteria akceptacji:**
- Generowanie planszy < 1s
- Stały 60 FPS podczas gry
- Zużycie RAM < 100MB

**Oszacowany czas**: 4-5h

---

### Issue #25: Testy Jednostkowe i Integracyjne
**Priorytet**: 🟠 WYSOKI  
**Etykiety**: `testing`, `quality`, `phase-5`

**Opis:**
Napisać kompleksowe testy dla całej aplikacji.

**Zadania:**
- [ ] Testy jednostkowe:
  - Validator (wszystkie metody)
  - BoardGenerator
  - Cell operations
  - Constraints
- [ ] Testy integracyjne:
  - Pełny flow gry
  - Zapisywanie/wczytywanie
  - UI interactions (pygame.event)
- [ ] Pokrycie kodu > 70%
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Automatyczne testy przy każdym commit

**Kryteria akceptacji:**
- Wszystkie kluczowe funkcje mają testy
- Testy przechodzą automatycznie
- Pokrycie > 70%

**Oszacowany czas**: 8-10h

---

### Issue #26: Dokumentacja i Komentarze
**Priorytet**: 🟡 ŚREDNI  
**Etykiety**: `documentation`, `polish`, `phase-5`

**Opis:**
Dodać docstringi i komentarze do całego kodu.

**Zadania:**
- [ ] Docstringi dla wszystkich klas i funkcji (format Google)
- [ ] Komentarze wyjaśniające złożone algorytmy
- [ ] Type hints dla wszystkich funkcji
- [ ] Wygenerować dokumentację (Sphinx lub pdoc)
- [ ] README z przykładami użycia API
- [ ] Contributing guidelines
- [ ] Code of Conduct

**Kryteria akceptacji:**
- Każda publiczna funkcja ma docstring
- Dokumentacja HTML jest generowana
- Type hints są wszędzie

**Oszacowany czas**: 4-5h

---

### Issue #27: Packaging i Dystrybucja
**Priorytet**: 🟢 NISKI  
**Etykiety**: `deployment`, `packaging`, `phase-5`

**Opis:**
Przygotować aplikację do dystrybucji.

**Zadania:**
- [ ] Konfiguracja PyInstaller
- [ ] Build dla Windows (.exe)
- [ ] Build dla macOS (.app)
- [ ] Build dla Linux (AppImage)
- [ ] Ikona aplikacji
- [ ] Installer (opcjonalnie)
- [ ] Publikacja na GitHub Releases
- [ ] Opcjonalnie: Steam, itch.io

**Kryteria akceptacji:**
- Aplikacja działa jako standalone
- Łatwa instalacja dla użytkowników
- Builds dla 3 głównych platform

**Oszacowany czas**: 6-8h

---

## 📊 Podsumowanie Faz

| Faza | Issues | Szacowany Czas | Priorytet |
|------|--------|----------------|-----------|
| **Faza 1: Core Gameplay** | #1-6 | 28-36h | 🔴 Krytyczny |
| **Faza 2: UI/UX** | #7-11 | 19-24h | 🟠 Wysoki |
| **Faza 3: Features** | #12-16 | 19-24h | 🟡 Średni |
| **Faza 4: Content** | #17-20 | 19-24h | 🟡 Średni |
| **Faza 5: Polish** | #21-27 | 36-45h | 🟢 Niski-Średni |
| **TOTAL** | 27 issues | **121-153h** | |

---

## 🏷️ Etykiety (Labels)

Użyj tych etykiet w GitHub Issues:

- `phase-1`, `phase-2`, `phase-3`, `phase-4`, `phase-5` - fazy projektu
- `bug` - błędy do naprawienia
- `feature` - nowe funkcje
- `refactoring` - refaktoryzacja kodu
- `ui` - interfejs użytkownika
- `core-logic` - logika gry
- `optimization` - optymalizacja
- `documentation` - dokumentacja
- `testing` - testy
- `accessibility` - dostępność
- `good-first-issue` - dla początkujących
- `help-wanted` - potrzebna pomoc

---

## 📝 Jak Używać tej Roadmapy

1. **Skopiuj każdy Issue** do GitHub Issues w swoim repo
2. **Przypisz etykiety** zgodnie z powyższą listą
3. **Pracuj sekwencyjnie** - najpierw Faza 1, potem 2, itd.
4. **Twórz branch** dla każdego issue: `feature/issue-XX-short-name`
5. **Pull Request** po ukończeniu z linkiem do issue
6. **Zamknij issue** po merge do main

---

**Utworzono**: Listopad 2025  
**Wersja**: 1.0  
**Status**: 📋 Gotowe do implementacji

