# Instrukcja optymalizacji pamieci laptopa (Windows) - 2026-03-28

## 1) Twoj aktualny stan (na podstawie skanu)

- Dysk `C:`: `473.95 GB` calkowicie, wolne tylko `1.37 GB` (stan krytyczny).
- Najwieksze obszary:
- `C:\Users\ankap\Downloads` -> `64.013 GB`
- `C:\Users\ankap\OneDrive` -> `26.285 GB`
- `C:\Users\ankap\AppData\Local` -> `8.27 GB`
- `C:\Users\ankap\.cache` -> `4.854 GB`
- `C:\Users\ankap\.gradle` -> `4.68 GB`
- `C:\Users\ankap\.vscode` -> `2.803 GB`

Najwieksze konkretne "zjadacze miejsca":
- `C:\Users\ankap\Downloads\solid_works` i podobne foldery instalacyjne SOLIDWORKS.
- `C:\Users\ankap\Downloads\FMP10_Rat_brain_breg_084.ibd` (`4.347 GB`).
- `C:\Users\ankap\.cache\whisper` (`4.833 GB`, modele: `large-v3.pt`, `large-v3-turbo.pt`).
- `C:\Users\ankap\AppData\Local\Temp` (`2.338 GB`, glownie `DiagOutputDir` `1.384 GB`).
- `C:\Users\ankap\.gradle\caches` (`4.148 GB`) + `wrapper` (`0.527 GB`).
- Stare wersje rozszerzen VS Code (`~1.54 GB` potencjalnego odzysku).
- `C:\Users\ankap\OneDrive\Desktop\sisyphus\sisyphus-ims-analysis\data` (`8.751 GB`), w tym prawdopodobna duplikacja (`raw_local` + `processed` po ~4.37 GB).
- `C:\Users\ankap\OneDrive\Desktop\ANIA\zdjęcia z telefonu` (`3.983 GB`).
- `C:\Users\ankap\OneDrive\Documents\SOLIDWORKS Downloads` (`6.039 GB`).

## 2) Dlaczego czesc rzeczy nie zapisuje sie na pulpicie

Masz bardzo malo wolnego miejsca (`1.37 GB`), wiec Windows i aplikacje zaczynaja odmawiac zapisu.

Dodatkowo pulpit jest u Ciebie pod OneDrive (`C:\Users\ankap\OneDrive\Desktop`), wiec problemy moga byc podwojne:
- brak miejsca lokalnie na dysku `C:`
- i/lub limit miejsca w chmurze OneDrive.

## 3) Co mozesz bezpiecznie usuwac (priorytet: duzy zysk)

## A. Natychmiast (najwiekszy odzysk)

1. Porzadki w `Downloads` (instalatory, paczki `.7z.*`, pliki `.zip.part`, stare eksporty danych).
2. Modele `whisper` z `C:\Users\ankap\.cache\whisper`, jesli aktualnie nie uzywasz lokalnego Whisper.
3. Czyszczenie `Temp` (`C:\Users\ankap\AppData\Local\Temp`), po zamknieciu aplikacji.
4. Czyszczenie cache Gradle (`C:\Users\ankap\.gradle\caches` i stare wrappery).
5. Usuniecie starych wersji rozszerzen VS Code.
6. Przejrzenie duzych folderow na pulpicie: `sisyphus`, `ANIA`, `modelowanie`, `nn`, `backup-...`.

## B. Bezpieczne "deweloperskie smieci"

- Foldery wirtualnych srodowisk Pythona: `.venv`, `venv`, `env` (odtworzysz z `requirements.txt`/`pyproject.toml`).
- `node_modules` (odtworzysz przez `npm install`/`pnpm install`).
- Cache testow i kompilacji:
- `__pycache__`
- `.pytest_cache`
- `.mypy_cache`
- `.ruff_cache`
- `dist`, `build`, `target` (artefakty builda).

U Ciebie same foldery typu `venv` na pulpicie zajmuja okolo `4.136 GB`.

## C. Czego NIE kasowac "w ciemno"

- Calego `AppData\Local\Packages` recznie.
- Lepsza opcja: odinstalowanie niepotrzebnych aplikacji ze `Settings > Apps`.
- Danych projektowych, ktorych nie masz w kopii zapasowej.
- Folderow `.git` w aktywnych repozytoriach.

## 4) Konkretne kroki na teraz (kolejnosc)

## Krok 1 - awaryjne odzyskanie miejsca (cel: +20 GB lub wiecej)

1. Usun z `Downloads` najwieksze i zduplikowane instalatory/archiwa.
2. Usun `C:\Users\ankap\.cache\whisper` (jesli nie uzywasz teraz whisper lokalnie).
3. Oproznij `Temp`.
4. Oproznij Kosz.
5. Restart komputera.

### Przykladowe komendy PowerShell (ostroznie, uruchamiaj po kolei)

```powershell
# 1) Najwieksze pliki w Downloads
Get-ChildItem "C:\Users\ankap\Downloads" -Recurse -File -ErrorAction SilentlyContinue |
  Sort-Object Length -Descending |
  Select-Object -First 50 @{n='SizeGB';e={[math]::Round($_.Length/1GB,3)}}, FullName
```

```powershell
# 2) Usuniecie cache whisper (jesli chcesz odzyskac ~4.8 GB)
Remove-Item "C:\Users\ankap\.cache\whisper" -Recurse -Force
```

```powershell
# 3) Usuniecie zawartosci Temp
Get-ChildItem "C:\Users\ankap\AppData\Local\Temp" -Force -ErrorAction SilentlyContinue |
  Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
```

```powershell
# 4) Czyszczenie Gradle cache
Remove-Item "C:\Users\ankap\.gradle\caches" -Recurse -Force -ErrorAction SilentlyContinue
```

```powershell
# 5) Skan duzych folderow na pulpicie (przed decyzja co usunac)
Get-ChildItem "C:\Users\ankap\OneDrive\Desktop" -Directory -Force |
  ForEach-Object {
    $size=(Get-ChildItem $_.FullName -Recurse -File -Force -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
    [PSCustomObject]@{Folder=$_.Name; SizeGB=[math]::Round($size/1GB,3)}
  } | Sort-Object SizeGB -Descending
```

## Krok 2 - uporzadkowanie projektow programistycznych

Pomysl "wszystko na GitHub i usuwam lokalnie" jest dobry tylko czesciowo.

Dobra praktyka:
- GitHub trzyma kod i historie.
- Lokalnie trzymaj tylko aktywne projekty.
- Dane, modele, duze eksporty trzymaj poza repo (OneDrive/drive zewnetrzny), nie w Git.

Proponowana struktura:
- `C:\dev\active` -> projekty aktywne (maks 3-5 naraz).
- `C:\dev\archive` -> projekty zakonczone (zip lub clone readonly).
- `C:\dev\templates` -> startery.
- `C:\data` -> duze dane (csv, ibd, modele, buildy).

Zasada:
- Pulpit ma byc "lekki" (skroty, nie magazyn plikow).
- Projekty i dane nie powinny siedziec luzem na pulpicie OneDrive.

## Krok 3 - jak archiwizowac projekty bez chaosu

Przed usunieciem lokalnego projektu:
1. `git status` ma byc czysty.
2. Wszystko wypchniete na GitHub (`git push`).
3. Jest `README` z instrukcja uruchomienia.
4. Jest plik zaleznosci (`requirements.txt` albo lockfile).
5. Wazne dane sa poza repo i maja osobna kopie.

Potem:
- Usun lokalny `node_modules`, `.venv`, `build`, `dist`.
- Jesli projekt nieaktywny: spakuj i przenies do `C:\dev\archive` albo na dysk zewnetrzny.

## Krok 4 - OneDrive i pulpit

Poniewaz pulpit jest zsynchronizowany z OneDrive:
- sprawdz limit OneDrive w aplikacji (Storage).
- dla ciezkich folderow kliknij "Free up space" (zwolnij miejsce lokalnie) tam, gdzie to bezpieczne.
- nie trzymaj instalatorow i danych badawczych na pulpicie.

## 5) Rutyna na przyszlosc (zeby problem nie wracal)

### Co tydzien (10-15 minut)

1. Przejrzyj `Downloads` i usun pliki > 1 GB, ktore nie sa potrzebne.
2. Oczysc `Temp`.
3. W projekcie usun `__pycache__`, `.pytest_cache`, `dist`, `build`.
4. Sprawdz wolne miejsce (cel: zawsze min. 15-20 GB zapasu).

### Co miesiac (20-30 minut)

1. Oczysc cache narzedzi (`.gradle`, ewentualnie npm/pip cache).
2. Przejrzyj stare rozszerzenia VS Code i duplikaty wersji.
3. Przenies nieaktywne projekty z `active` do `archive`.
4. Sprawdz duze dane i eksporty (czy nie sa zdublowane).

## 6) Twoj najszybszy plan odzysku miejsca (praktycznie)

Najpierw zrob:
1. `Downloads` (najpierw najwieksze pliki) - potencjalnie dziesiatki GB.
2. `C:\Users\ankap\.cache\whisper` - ok. `4.8 GB`.
3. `C:\Users\ankap\AppData\Local\Temp` - ok. `2.3 GB`.
4. `C:\Users\ankap\.gradle\caches` - ok. `4.1 GB`.
5. Stare wersje rozszerzen VS Code - ok. `1.5 GB`.

To razem daje realistycznie ponad `20-40 GB` odzysku, bez ruszania krytycznych plikow systemowych.
