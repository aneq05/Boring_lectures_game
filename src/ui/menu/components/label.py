"""
Label component.
"""
from __future__ import annotations

import pygame

from src.ui.style import AppStyle


class Label:
    """Simple text label with consistent typography."""

    def __init__(
        self,
        x: int,
        y: int,
        text: str,
        font_size: int = 24,
        color: tuple | None = None,
        centered: bool = False,
        bold: bool = False,
    ):
        self.x = x
        self.y = y
        self.text = text
        self.font = AppStyle.font(font_size, bold=bold)
        self.color = color if color is not None else AppStyle.TEXT
        self.centered = centered

    def set_text(self, text: str):
        self.text = text

    def draw(self, surface: pygame.Surface):
        text_surf = self.font.render(self.text, True, self.color)
        if self.centered:
            text_rect = text_surf.get_rect(center=(self.x, self.y))
        else:
            text_rect = text_surf.get_rect(topleft=(self.x, self.y))
        surface.blit(text_surf, text_rect)
