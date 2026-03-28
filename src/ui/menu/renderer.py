"""
Renderer for menu screens.
"""
from __future__ import annotations

import math
from typing import List

import pygame

from src.ui.style import AppStyle


class MenuRenderer:
    """Handles menu background, decorative layers and transitions."""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.small_font = AppStyle.font(22)
        self.frame = 0

    def render(self, components: List):
        self.frame += 1
        self._draw_background()

        for component in components:
            if hasattr(component, "draw"):
                component.draw(self.screen)

        self._draw_instructions()
        pygame.display.flip()

    def play_exit_transition(self, components: List, duration_ms: int = 320):
        """Plays a short fade-out before switching to the game screen."""
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        start = pygame.time.get_ticks()
        clock = pygame.time.Clock()

        while True:
            elapsed = pygame.time.get_ticks() - start
            progress = min(1.0, elapsed / max(1, duration_ms))
            self._draw_background()
            for component in components:
                if hasattr(component, "draw"):
                    component.draw(self.screen)
            self._draw_instructions()

            overlay.fill((255, 246, 250, int(235 * progress)))
            self.screen.blit(overlay, (0, 0))
            pygame.display.flip()
            if progress >= 1.0:
                break
            clock.tick(60)

    def _draw_background(self):
        AppStyle.draw_vertical_gradient(self.screen, AppStyle.BG_TOP, AppStyle.BG_BOTTOM)
        width, height = self.screen.get_size()
        t = self.frame / 28.0

        circles = [
            (int(width * 0.12), int(height * 0.18 + 8 * math.sin(t)), 120),
            (int(width * 0.86), int(height * 0.30 + 7 * math.sin(-t)), 95),
            (int(width * 0.18), int(height * 0.82 + 9 * math.sin(t * 0.8)), 80),
            (int(width * 0.80), int(height * 0.76 + 8 * math.sin(-t * 0.9)), 130),
        ]
        for x, y, radius in circles:
            pygame.draw.circle(self.screen, AppStyle.DECORATION, (x, y), radius)

        card_rect = pygame.Rect(width // 2 - 265, 24, 530, height - 70)
        AppStyle.draw_shadowed_rect(
            surface=self.screen,
            rect=card_rect,
            color=AppStyle.CARD,
            border_color=AppStyle.CARD_BORDER,
            radius=34,
            shadow_offset=6,
        )

    def _draw_instructions(self):
        instruction_text = "Tab/Up/Down: selection | Left/Right: change option | Enter: start | ESC: exit"
        instruction_surf = self.small_font.render(instruction_text, True, AppStyle.MUTED)
        instruction_rect = instruction_surf.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() - 24)
        )
        self.screen.blit(instruction_surf, instruction_rect)
