"""
Selector component - przełącznik opcji z strzałkami
"""
import pygame
from typing import Callable, Optional, List, Any
from src.utils.colors import BasicColors, ThemeColors


class Selector:
    """
    Komponent selektora z opcjami przełączanymi strzałkami.

    Odpowiedzialność:
    - Renderowanie selektora z opcjami
    - Obsługa zmiany opcji (strzałki, mysz)
    - Wywoływanie callback przy zmianie
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        label: str,
        options: List[Any],
        option_display: Callable[[Any], str],
        initial_index: int = 0,
        on_change: Optional[Callable[[Any], None]] = None,
        font_size: int = 28
    ):
        """
        Inicjalizacja selektora.

        Args:
            x, y: Pozycja selektora
            width, height: Wymiary
            label: Etykieta opisująca selektor
            options: Lista opcji do wyboru
            option_display: Funkcja konwertująca opcję na tekst
            initial_index: Początkowy indeks wybranej opcji
            on_change: Callback wywoływany przy zmianie opcji
            font_size: Rozmiar czcionki
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.options = options
        self.option_display = option_display
        self.current_index = initial_index
        self.on_change = on_change
        self.font = pygame.font.Font(None, font_size)
        self.small_font = pygame.font.Font(None, font_size - 4)
        self.is_focused = False  # Dla nawigacji klawiaturą

        # Obszary strzałek
        arrow_size = 30
        arrow_y = y + height // 2 - arrow_size // 2
        self.left_arrow_rect = pygame.Rect(x + 10, arrow_y, arrow_size, arrow_size)
        self.right_arrow_rect = pygame.Rect(x + width - arrow_size - 10, arrow_y, arrow_size, arrow_size)

        self.left_hovered = False
        self.right_hovered = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Obsługuje zdarzenia dla selektora.

        Args:
            event: Zdarzenie pygame

        Returns:
            bool: True jeśli wartość została zmieniona
        """
        if event.type == pygame.MOUSEMOTION:
            self.left_hovered = self.left_arrow_rect.collidepoint(event.pos)
            self.right_hovered = self.right_arrow_rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Lewy strzałka - poprzednia opcja
                if self.left_hovered and self.current_index > 0:
                    self.current_index -= 1
                    if self.on_change:
                        self.on_change(self.options[self.current_index])
                    return True

                # Prawy strzałka - następna opcja
                if self.right_hovered and self.current_index < len(self.options) - 1:
                    self.current_index += 1
                    if self.on_change:
                        self.on_change(self.options[self.current_index])
                    return True

        elif event.type == pygame.KEYDOWN:
            # Klawiatura: strzałki lewo/prawo
            if event.key == pygame.K_LEFT and self.current_index > 0:
                self.current_index -= 1
                if self.on_change:
                    self.on_change(self.options[self.current_index])
                return True

            elif event.key == pygame.K_RIGHT and self.current_index < len(self.options) - 1:
                self.current_index += 1
                if self.on_change:
                    self.on_change(self.options[self.current_index])
                return True

        return False

    def get_current_option(self) -> Any:
        """Zwraca aktualnie wybraną opcję"""
        return self.options[self.current_index]

    def draw(self, surface: pygame.Surface):
        """
        Rysuje selektor na powierzchni.

        Args:
            surface: Powierzchnia pygame do rysowania
        """
        # Tło (jaśniejsze jeśli aktywny)
        bg_color = (230, 240, 255) if self.is_focused else BasicColors.LIGHT_GRAY.value
        border_color = ThemeColors.BLUE.value if self.is_focused else BasicColors.DARK_GRAY.value
        border_width = 3 if self.is_focused else 2

        pygame.draw.rect(surface, bg_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, border_color, self.rect, border_width, border_radius=8)

        # Etykieta (na górze)
        label_surf = self.small_font.render(self.label, True, BasicColors.DARK_GRAY.value)
        label_rect = label_surf.get_rect(midtop=(self.rect.centerx, self.rect.top + 5))
        surface.blit(label_surf, label_rect)

        # Aktualna wartość (wycentrowana)
        current_option = self.options[self.current_index]
        value_text = self.option_display(current_option)
        value_surf = self.font.render(value_text, True, BasicColors.BLACK.value)
        value_rect = value_surf.get_rect(center=self.rect.center)
        surface.blit(value_surf, value_rect)

        # Lewa strzałka
        left_color = ThemeColors.BLUE.value if self.left_hovered and self.current_index > 0 else BasicColors.GRAY.value
        if self.current_index == 0:
            left_color = BasicColors.LIGHT_GRAY.value  # Disabled
        pygame.draw.polygon(surface, left_color, [
            (self.left_arrow_rect.centerx + 5, self.left_arrow_rect.centery),
            (self.left_arrow_rect.centerx - 5, self.left_arrow_rect.centery - 8),
            (self.left_arrow_rect.centerx - 5, self.left_arrow_rect.centery + 8)
        ])

        # Prawa strzałka
        right_color = ThemeColors.BLUE.value if self.right_hovered and self.current_index < len(self.options) - 1 else BasicColors.GRAY.value
        if self.current_index == len(self.options) - 1:
            right_color = BasicColors.LIGHT_GRAY.value  # Disabled
        pygame.draw.polygon(surface, right_color, [
            (self.right_arrow_rect.centerx - 5, self.right_arrow_rect.centery),
            (self.right_arrow_rect.centerx + 5, self.right_arrow_rect.centery - 8),
            (self.right_arrow_rect.centerx + 5, self.right_arrow_rect.centery + 8)
        ])

