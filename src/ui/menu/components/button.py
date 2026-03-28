"""
Button component - rounded CTA with soft hover effects.
"""
from __future__ import annotations

from typing import Callable

import pygame

from src.ui.style import AppStyle


class Button:
    """Clickable rounded button used in menu screens."""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        callback: Callable,
        font_size: int = 32,
        color: tuple | None = None,
        hover_color: tuple | None = None,
        text_color: tuple | None = None,
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.color = color if color is not None else AppStyle.ACCENT
        self.hover_color = hover_color if hover_color is not None else AppStyle.ACCENT_HOVER
        self.text_color = text_color if text_color is not None else (255, 255, 255)
        self.font = AppStyle.font(font_size, bold=True)
        self.is_hovered = False
        self.is_focused = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()
                return True
        return False

    def draw(self, surface: pygame.Surface):
        current_color = self.hover_color if (self.is_hovered or self.is_focused) else self.color
        radius = max(14, self.rect.height // 2)

        shadow_rect = self.rect.move(0, 4 if not self.is_hovered else 2)
        pygame.draw.rect(surface, AppStyle.SHADOW, shadow_rect, border_radius=radius)
        pygame.draw.rect(surface, current_color, self.rect, border_radius=radius)

        border_color = AppStyle.TITLE if self.is_focused else (255, 255, 255)
        border_width = 3 if self.is_focused else 2
        pygame.draw.rect(surface, border_color, self.rect, border_width, border_radius=radius)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
