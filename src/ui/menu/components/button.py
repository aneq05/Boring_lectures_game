"""
Button component - przycisk klikalny z hover effect
"""
import pygame
from typing import Callable
from src.utils.colors import BasicColors, ThemeColors


class Button:
    """
    Komponent przycisku z obsługą kliknięć i hover effect.

    Odpowiedzialność:
    - Renderowanie przycisku
    - Detekcja hover
    - Wywołanie callback przy kliknięciu
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        callback: Callable,
        font_size: int = 32,
        color: tuple = None,
        hover_color: tuple = None,
        text_color: tuple = None
    ):
        """
        Inicjalizacja przycisku.

        Args:
            x, y: Pozycja przycisku
            width, height: Wymiary
            text: Tekst na przycisku
            callback: Funkcja wywoływana przy kliknięciu
            font_size: Rozmiar czcionki
            color: Kolor tła (domyślnie BLUE)
            hover_color: Kolor przy najechaniu myszką (domyślnie LIGHT_BLUE)
            text_color: Kolor tekstu (domyślnie WHITE)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.color = color if color is not None else ThemeColors.BLUE.value
        self.hover_color = hover_color if hover_color is not None else ThemeColors.LIGHT_BLUE.value
        self.text_color = text_color if text_color is not None else BasicColors.WHITE.value
        self.font = pygame.font.Font(None, font_size)
        self.is_hovered = False
        self.is_focused = False  # Dla nawigacji klawiaturą

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Obsługuje zdarzenia dla przycisku.

        Args:
            event: Zdarzenie pygame

        Returns:
            bool: True jeśli przycisk został kliknięty
        """
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                self.callback()
                return True

        return False

    def draw(self, surface: pygame.Surface):
        """
        Rysuje przycisk na powierzchni.

        Args:
            surface: Powierzchnia pygame do rysowania
        """
        # Tło przycisku (zmienia kolor przy hover lub focus)
        current_color = self.hover_color if (self.is_hovered or self.is_focused) else self.color
        border_width = 3 if self.is_focused else 2

        pygame.draw.rect(surface, current_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BasicColors.BLACK.value, self.rect, border_width, border_radius=10)

        # Tekst wycentrowany
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

