"""
Label component - etykieta tekstowa
"""
import pygame
from src.utils.colors import BasicColors


class Label:
    """
    Komponent etykiety tekstowej.

    Odpowiedzialność:
    - Wyświetlanie tekstu
    - Centrowanie opcjonalne
    """

    def __init__(
        self,
        x: int,
        y: int,
        text: str,
        font_size: int = 24,
        color: tuple = None,
        centered: bool = False
    ):
        """
        Inicjalizacja etykiety.

        Args:
            x, y: Pozycja etykiety
            text: Tekst do wyświetlenia
            font_size: Rozmiar czcionki
            color: Kolor tekstu (domyślnie BLACK)
            centered: Czy wycentrować tekst względem (x, y)
        """
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.color = color if color is not None else BasicColors.BLACK.value
        self.centered = centered

    def set_text(self, text: str):
        """
        Zmienia tekst etykiety.

        Args:
            text: Nowy tekst
        """
        self.text = text

    def draw(self, surface: pygame.Surface):
        """
        Rysuje etykietę na powierzchni.

        Args:
            surface: Powierzchnia pygame do rysowania
        """
        text_surf = self.font.render(self.text, True, self.color)

        if self.centered:
            text_rect = text_surf.get_rect(center=(self.x, self.y))
        else:
            text_rect = text_surf.get_rect(topleft=(self.x, self.y))

        surface.blit(text_surf, text_rect)

