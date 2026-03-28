"""
Selector component - rounded switcher for option groups.
"""
from __future__ import annotations

from typing import Any, Callable, List, Optional

import pygame

from src.ui.style import AppStyle


class Selector:
    """Option selector with left/right controls."""

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
        font_size: int = 30,
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.options = options
        self.option_display = option_display
        self.current_index = initial_index
        self.on_change = on_change
        self.font = AppStyle.font(font_size, bold=True)
        self.small_font = AppStyle.font(max(20, font_size - 8))
        self.is_focused = False

        arrow_size = 42
        arrow_y = y + height // 2 - arrow_size // 2 + 6
        self.left_arrow_rect = pygame.Rect(x + 18, arrow_y, arrow_size, arrow_size)
        self.right_arrow_rect = pygame.Rect(x + width - arrow_size - 18, arrow_y, arrow_size, arrow_size)
        self.left_hovered = False
        self.right_hovered = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.left_hovered = self.left_arrow_rect.collidepoint(event.pos)
            self.right_hovered = self.right_arrow_rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.left_arrow_rect.collidepoint(event.pos) and self.current_index > 0:
                self.current_index -= 1
                if self.on_change:
                    self.on_change(self.options[self.current_index])
                return True

            if self.right_arrow_rect.collidepoint(event.pos) and self.current_index < len(self.options) - 1:
                self.current_index += 1
                if self.on_change:
                    self.on_change(self.options[self.current_index])
                return True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and self.current_index > 0:
                self.current_index -= 1
                if self.on_change:
                    self.on_change(self.options[self.current_index])
                return True
            if event.key == pygame.K_RIGHT and self.current_index < len(self.options) - 1:
                self.current_index += 1
                if self.on_change:
                    self.on_change(self.options[self.current_index])
                return True

        return False

    def get_current_option(self) -> Any:
        return self.options[self.current_index]

    def draw(self, surface: pygame.Surface):
        border = AppStyle.ACCENT if self.is_focused else AppStyle.CARD_BORDER
        card = AppStyle.ACCENT_SOFT if self.is_focused else AppStyle.CARD

        AppStyle.draw_shadowed_rect(
            surface=surface,
            rect=self.rect,
            color=card,
            border_color=border,
            radius=22,
            shadow_offset=4,
        )

        label_surf = self.small_font.render(self.label, True, AppStyle.MUTED)
        label_rect = label_surf.get_rect(midtop=(self.rect.centerx, self.rect.top + 10))
        surface.blit(label_surf, label_rect)

        current_option = self.options[self.current_index]
        value_text = self.option_display(current_option)
        value_surf = self.font.render(value_text, True, AppStyle.TEXT)
        value_rect = value_surf.get_rect(center=(self.rect.centerx, self.rect.centery + 8))
        surface.blit(value_surf, value_rect)

        self._draw_arrow(surface, left=True)
        self._draw_arrow(surface, left=False)

    def _draw_arrow(self, surface: pygame.Surface, left: bool):
        rect = self.left_arrow_rect if left else self.right_arrow_rect
        hovered = self.left_hovered if left else self.right_hovered
        enabled = self.current_index > 0 if left else self.current_index < len(self.options) - 1

        base = (255, 255, 255) if enabled else (247, 239, 244)
        border = AppStyle.ACCENT if hovered and enabled else AppStyle.CARD_BORDER
        pygame.draw.rect(surface, base, rect, border_radius=12)
        pygame.draw.rect(surface, border, rect, 2, border_radius=12)

        icon_color = AppStyle.ACCENT_HOVER if hovered and enabled else AppStyle.MUTED
        if not enabled:
            icon_color = (189, 181, 194)

        cx, cy = rect.center
        if left:
            points = [(cx + 4, cy - 9), (cx - 5, cy), (cx + 4, cy + 9)]
        else:
            points = [(cx - 4, cy - 9), (cx + 5, cy), (cx - 4, cy + 9)]
        pygame.draw.polygon(surface, icon_color, points)
