"""
Renderer - renderowanie elementów menu
"""
import pygame
from typing import List
from src.utils.colors import BasicColors


class MenuRenderer:
    """
    Klasa odpowiedzialna za renderowanie menu.

    Odpowiedzialność:
    - Czyszczenie ekranu
    - Rysowanie wszystkich komponentów
    - Rysowanie dodatkowych elementów (instrukcje)
    """

    def __init__(self, screen: pygame.Surface):
        """
        Inicjalizacja renderera.

        Args:
            screen: Powierzchnia pygame do rysowania
        """
        self.screen = screen
        self.small_font = pygame.font.Font(None, 24)

    def render(self, components: List):
        """
        Renderuje całe menu.

        Args:
            components: Lista komponentów UI do narysowania
        """
        # Czyść ekran
        self.screen.fill(BasicColors.WHITE.value)

        # Rysuj wszystkie komponenty
        for component in components:
            if hasattr(component, 'draw'):
                component.draw(self.screen)

        # Rysuj instrukcję na dole
        self._draw_instructions()

        # Aktualizuj ekran
        pygame.display.flip()

    def _draw_instructions(self):
        """Rysuje instrukcje obsługi na dole ekranu."""
        instruction_text = "↑↓ Tab - przełączaj | ←→ - zmień wartość | Enter/Space - START | ESC - wyjście"
        instruction_surf = self.small_font.render(instruction_text, True, BasicColors.DARK_GRAY.value)
        instruction_rect = instruction_surf.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() - 20)
        )
        self.screen.blit(instruction_surf, instruction_rect)

