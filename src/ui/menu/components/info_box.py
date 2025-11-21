"""
InfoBox component - pole informacyjne z tytułem i opisem
"""
import pygame
from src.utils.colors import ThemeColors, BasicColors


class InfoBox:
    """
    Komponent pola informacyjnego.

    Odpowiedzialność:
    - Wyświetlanie tytułu i tekstu informacyjnego
    - Obsługa tekstu wieloliniowego
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        title: str = "",
        text: str = "",
        font_size: int = 20
    ):
        """
        Inicjalizacja pola informacyjnego.

        Args:
            x, y: Pozycja pola
            width, height: Wymiary
            title: Tytuł pola
            text: Treść (może zawierać '\n' dla wielu linii)
            font_size: Rozmiar czcionki
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.title_font = pygame.font.Font(None, font_size + 4)

    def set_content(self, title: str, text: str):
        """
        Ustawia zawartość pola.

        Args:
            title: Nowy tytuł
            text: Nowa treść
        """
        self.title = title
        self.text = text

    def draw(self, surface: pygame.Surface):
        """
        Rysuje pole informacyjne na powierzchni.

        Args:
            surface: Powierzchnia pygame do rysowania
        """
        # Tło - Alice Blue
        pygame.draw.rect(surface, (240, 248, 255), self.rect, border_radius=8)
        pygame.draw.rect(surface, ThemeColors.BLUE.value, self.rect, 2, border_radius=8)

        # Tytuł (jeśli istnieje)
        if self.title:
            title_surf = self.title_font.render(self.title, True, ThemeColors.BLUE.value)
            title_rect = title_surf.get_rect(
                midtop=(self.rect.centerx, self.rect.top + 10)
            )
            surface.blit(title_surf, title_rect)

        # Tekst (wieloliniowy)
        lines = self.text.split('\n')
        y_offset = self.rect.top + 40 if self.title else self.rect.top + 15

        for line in lines:
            text_surf = self.font.render(line, True, BasicColors.DARK_GRAY.value)
            text_rect = text_surf.get_rect(
                midtop=(self.rect.centerx, y_offset)
            )
            surface.blit(text_surf, text_rect)
            y_offset += 25

