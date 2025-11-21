"""
Event handler - obsługa zdarzeń menu z pełną nawigacją klawiaturą
"""
import pygame
import sys
from typing import List


class MenuEventHandler:
    """
    Klasa odpowiedzialna za obsługę wszystkich zdarzeń w menu.

    Odpowiedzialność:
    - Przetwarzanie zdarzeń pygame
    - Delegowanie zdarzeń do odpowiednich komponentów
    - Obsługa globalnych skrótów (ESC, Enter)
    - Nawigacja klawiaturą (strzałki góra/dół, Tab)
    """

    def __init__(self):
        self.should_quit = False
        self.should_start_game = False
        self.focused_index = 0  # Indeks aktualnie aktywnego komponentu (0-3: selektory, 4: przycisk)
        self.max_focusable = 4  # 3 selektory + przycisk START

    def handle_events(self, components: List, selectors: List, start_button) -> dict:
        """
        Obsługuje wszystkie zdarzenia dla menu.

        Args:
            components: Lista wszystkich komponentów UI
            selectors: Lista tylko selektorów (do nawigacji)
            start_button: Przycisk START (do aktywacji)

        Returns:
            dict: Słownik z flagami akcji {'quit': bool, 'start_game': bool}
        """
        for event in pygame.event.get():
            # Zamknięcie okna
            if event.type == pygame.QUIT:
                self.should_quit = True
                return {'quit': True, 'start_game': False}

            # Klawiatura
            elif event.type == pygame.KEYDOWN:
                action = self._handle_keyboard(event, selectors, start_button)
                if action:
                    return action

            # Przekaż zdarzenie do wszystkich komponentów (dla obsługi myszy)
            for component in components:
                if hasattr(component, 'handle_event'):
                    component.handle_event(event)

        return {'quit': False, 'start_game': False}

    def _handle_keyboard(self, event: pygame.event.Event, selectors: List, start_button) -> dict:
        """
        Obsługuje zdarzenia klawiatury z nawigacją.

        Args:
            event: Zdarzenie pygame KEYDOWN
            selectors: Lista selektorów
            start_button: Przycisk START

        Returns:
            dict: Akcja do wykonania
        """
        # ESC - wyjście
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        # Enter - aktywuj element lub start gry
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            if self.focused_index == 4:  # Przycisk START
                return {'quit': False, 'start_game': True}
            # Dla selektorów Enter nie robi nic specjalnego

        # Strzałka w dół lub Tab - następny element
        elif event.key == pygame.K_DOWN or event.key == pygame.K_TAB:
            self.focused_index = (self.focused_index + 1) % (self.max_focusable + 1)
            self._highlight_focused_element(selectors, start_button)

        # Strzałka w górę lub Shift+Tab - poprzedni element
        elif event.key == pygame.K_UP or (event.key == pygame.K_TAB and pygame.key.get_mods() & pygame.KMOD_SHIFT):
            self.focused_index = (self.focused_index - 1) % (self.max_focusable + 1)
            self._highlight_focused_element(selectors, start_button)

        # Strzałka w lewo - zmniejsz wartość w aktywnym selectorze
        elif event.key == pygame.K_LEFT:
            if 0 <= self.focused_index < len(selectors):
                selector = selectors[self.focused_index]
                if selector.current_index > 0:
                    selector.current_index -= 1
                    if selector.on_change:
                        selector.on_change(selector.options[selector.current_index])
                    return {'quit': False, 'start_game': False, 'changed': True}

        # Strzałka w prawo - zwiększ wartość w aktywnym selectorze
        elif event.key == pygame.K_RIGHT:
            if 0 <= self.focused_index < len(selectors):
                selector = selectors[self.focused_index]
                if selector.current_index < len(selector.options) - 1:
                    selector.current_index += 1
                    if selector.on_change:
                        selector.on_change(selector.options[selector.current_index])
                    return {'quit': False, 'start_game': False, 'changed': True}

        return {'quit': False, 'start_game': False}

    def _highlight_focused_element(self, selectors: List, start_button):
        """
        Podświetla aktualnie aktywny element (wizualna wskazówka dla użytkownika).

        Args:
            selectors: Lista selektorów
            start_button: Przycisk START
        """
        # Reset wszystkich - usuń podświetlenie
        for selector in selectors:
            if hasattr(selector, 'is_focused'):
                selector.is_focused = False
        if hasattr(start_button, 'is_focused'):
            start_button.is_focused = False

        # Podświetl aktywny element
        if 0 <= self.focused_index < len(selectors):
            if hasattr(selectors[self.focused_index], 'is_focused'):
                selectors[self.focused_index].is_focused = True
        elif self.focused_index == 4:  # Przycisk START
            if hasattr(start_button, 'is_focused'):
                start_button.is_focused = True

    def get_focused_component_name(self) -> str:
        """Zwraca nazwę aktualnie aktywnego komponentu (do debugowania)"""
        names = ["Poziom trudności", "Rozmiar planszy", "Motyw", "Info", "Przycisk START"]
        if 0 <= self.focused_index <= self.max_focusable:
            return names[self.focused_index]
        return "Nieznany"

