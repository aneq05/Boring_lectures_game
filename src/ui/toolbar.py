"""
Toolbar for gameplay actions.
"""
from __future__ import annotations

import pygame

from src.ui.style import AppStyle


class ToolbarButton:
    """Single rounded toolbar action."""

    def __init__(self, rect: pygame.Rect, label: str, action: str):
        self.rect = rect
        self.label = label
        self.action = action
        self.enabled = True
        self.hovered = False


class Toolbar:
    """Renders and handles gameplay action buttons."""

    def __init__(self, settings):
        self.settings = settings
        self.font = AppStyle.font(25, bold=True)
        self.small_font = AppStyle.font(19)
        self.buttons = self._create_buttons()

    def _create_buttons(self) -> list[ToolbarButton]:
        labels = [
            ("Undo", "undo"),
            ("Redo", "redo"),
            ("Hint", "hint"),
            ("Check", "check"),
            ("Reset", "reset"),
            ("New", "new_game"),
        ]
        buttons = []
        x = self.settings.grid_offset_x
        y = self.settings.toolbar_y
        width = 112
        gap = 12
        for index, (label, action) in enumerate(labels):
            rect = pygame.Rect(x + index * (width + gap), y, width, 48)
            buttons.append(ToolbarButton(rect=rect, label=label, action=action))
        return buttons

    def set_button_enabled(self, action: str, enabled: bool):
        for button in self.buttons:
            if button.action == action:
                button.enabled = enabled
                return

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.hovered = button.enabled and button.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button.enabled and button.rect.collidepoint(event.pos):
                    return button.action
        return None

    def draw(self, surface: pygame.Surface):
        for button in self.buttons:
            self._draw_button(surface, button)

        hint = self.small_font.render(
            "Left click: cycle | Right click: clear | U: undo | Y: redo | H: hint",
            True,
            AppStyle.MUTED,
        )
        surface.blit(hint, (self.settings.grid_offset_x + 3, self.settings.toolbar_y + 60))

    def _draw_button(self, surface: pygame.Surface, button: ToolbarButton):
        fill = (255, 255, 255) if button.enabled else (247, 238, 243)
        border = AppStyle.ACCENT if button.hovered else AppStyle.CARD_BORDER
        text_color = AppStyle.TITLE if button.enabled else (182, 173, 188)

        shadow_rect = button.rect.move(0, 3)
        pygame.draw.rect(surface, AppStyle.SHADOW, shadow_rect, border_radius=16)
        pygame.draw.rect(surface, fill, button.rect, border_radius=16)
        pygame.draw.rect(surface, border, button.rect, 2, border_radius=16)

        text = self.font.render(button.label, True, text_color)
        text_rect = text.get_rect(center=button.rect.center)
        surface.blit(text, text_rect)
