from __future__ import annotations

import pygame

from src.ui.style import AppStyle


class InfoBox:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        title: str = "",
        text: str = "",
        font_size: int = 15,
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.text = text
        self.font = AppStyle.font(font_size)
        self.title_font = AppStyle.font(font_size + 2, bold=True)

    def set_content(self, title: str, text: str):
        self.title = title
        self.text = text

    def draw(self, surface: pygame.Surface):
        AppStyle.draw_shadowed_rect(
            surface=surface,
            rect=self.rect,
            color=(255, 252, 255),
            border_color=AppStyle.CARD_BORDER,
            radius=24,
            shadow_offset=4,
        )

        title_surf = self.title_font.render(self.title, True, AppStyle.TITLE)
        title_rect = title_surf.get_rect(midtop=(self.rect.centerx, self.rect.top + 14))
        surface.blit(title_surf, title_rect)

        lines = self.text.split("\n")
        y_offset = self.rect.top + 50
        for line in lines:
            text_surf = self.font.render(line, True, AppStyle.MUTED)
            text_rect = text_surf.get_rect(midtop=(self.rect.centerx, y_offset))
            surface.blit(text_surf, text_rect)
            y_offset += 22
