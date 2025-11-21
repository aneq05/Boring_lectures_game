# ✅ Menu - Poprawiony Layout

## 🎯 Problem
Tekst instrukcji "Użyj strzałek lub myszki..." nachodzi na przycisk START.  
Za duża przerwa między podtytułem a pierwszym selektorem.

## ✅ Rozwiązanie

### Zmiany w `src/ui/menu/main_menu.py`:

**PRZED:**
```python
Tytuł:      y=50,  font=64
Podtytuł:   y=110, font=28
Trudność:   y=180, height=80
Rozmiar:    y=280, height=80
Motyw:      y=380, height=80
InfoBox:    y=480, height=120
START:      y=620  ❌ nachodzi na tekst (y=680)
```

**PO:**
```python
Tytuł:      y=30,  font=60  ⬆️ wyżej, mniejszy
Podtytuł:   y=85,  font=24  ⬆️ bliżej tytułu
Trudność:   y=125, height=75  ⬆️ zmniejszone odstępy
Rozmiar:    y=215, height=75  ⬆️
Motyw:      y=305, height=75  ⬆️
InfoBox:    y=395, height=110 ⬆️ niższy
START:      y=520  ✅ teraz nie nachodzi!
Instrukcje: y=680  ✅ wystarczająco dużo miejsca
```

## 📏 Nowy layout

```
┌─────────────────────────────────┐
│ y=30   Let Me Tango (60px)      │
│ y=85   Logiczna Gra... (24px)   │
│                                  │
│ y=125  [Poziom trudności] 75h   │
│                                  │
│ y=215  [Rozmiar planszy]  75h   │
│                                  │
│ y=305  [Motyw]            75h   │
│                                  │
│ y=395  [Informacje]      110h   │
│                                  │
│ y=520  [    START    ]   60h    │
│                                  │
│        ~ 90px wolnej przestrzeni │
│                                  │
│ y=680  Użyj strzałek...         │ ✅ Nie nachodzi!
└─────────────────────────────────┘
```

## 🎨 Korzyści

✅ Wszystkie elementy są kompaktowo ułożone  
✅ Wykorzystana przerwa między tytułem a selektorami  
✅ Instrukcje na dole mają ~90px przestrzeni nad sobą  
✅ Przycisk START nie nachodzi na tekst  
✅ Menu wygląda bardziej profesjonalnie  

## 🚀 Test

```cmd
python main.py
```

Menu powinno teraz wyglądać lepiej z odpowiednimi odstępami!

---

**Data**: 2025-11-09  
**Zmieniony plik**: `src/ui/menu/main_menu.py`  
**Linie zmienione**: 6 pozycji (tytuł, podtytuł, 3 selektory, info box, przycisk)

