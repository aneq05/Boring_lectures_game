"""
Win popup overlay.
"""
from __future__ import annotations

import math

import pygame

from src.ui.style import AppStyle


class WinPopup:
    """Soft celebratory popup shown after solving a board."""

    def __init__(self, screen: pygame.Surface, time_text: str, move_count: int, hints_used: int):
        self.screen = screen
        self.time_text = time_text
        self.move_count = move_count
        self.hints_used = hints_used
        self.title_font = AppStyle.font(56, bold=True)
        self.body_font = AppStyle.font(30, bold=True)
        self.frame = 0

        width, height = self.screen.get_size()
        self.panel_rect = pygame.Rect(width // 2 - 220, height // 2 - 150, 440, 300)

    def draw(self, surface: pygame.Surface):
        self.frame += 1
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((60, 50, 70, 118))
        surface.blit(overlay, (0, 0))

        self._draw_confetti(surface)

        pulse = int(6 + 2 * math.sin(self.frame / 14.0))
        shadow_rect = self.panel_rect.move(0, pulse)
        pygame.draw.rect(surface, AppStyle.SHADOW, shadow_rect, border_radius=30)
        pygame.draw.rect(surface, AppStyle.CARD, self.panel_rect, border_radius=30)
        pygame.draw.rect(surface, AppStyle.ACCENT, self.panel_rect, 3, border_radius=30)

        title = self.title_font.render("You did it!", True, AppStyle.TITLE)
        title_rect = title.get_rect(center=(self.panel_rect.centerx, self.panel_rect.y + 52))
        surface.blit(title, title_rect)

        stats = [
            f"Time: {self.time_text}",
            f"Moves: {self.move_count}",
            f"Hints used: {self.hints_used}",
            "Press N for a new puzzle",
            "or ESC to close the game.",
        ]
        y = self.panel_rect.y + 110
        for line in stats:
            text = self.body_font.render(line, True, AppStyle.TEXT)
            text_rect = text.get_rect(center=(self.panel_rect.centerx, y))
            surface.blit(text, text_rect)
            y += 36

    def _draw_confetti(self, surface: pygame.Surface):
        colors = [
            AppStyle.ACCENT,
            AppStyle.SUCCESS,
            (255, 195, 131),
            (248, 164, 190),
            (129, 191, 223),
        ]
        for i in range(22):
            x = int((i * 79 + self.frame * 2) % (self.screen.get_width() + 40) - 20)
            y = int((i * 53 + self.frame * 3) % (self.screen.get_height() + 40) - 20)
            color = colors[i % len(colors)]
            pygame.draw.circle(surface, color, (x, y), 4 + (i % 3))
